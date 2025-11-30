import datetime
import io
import logging
from typing import override
import os
import aids_pb2
import aids_pb2_grpc
import grpc
import pandas as pd
from database_handler import DatabaseHandler, Dataset

from google.protobuf.empty_pb2 import Empty

import seaborn as sns
import matplotlib.pyplot as plt


class AidsServiceServicer(aids_pb2_grpc.AidsServiceServicer):
    """
    Provides methods that implement functionality of the aids server.
    """

    def __init__(self) -> None:
        self.db_handler: DatabaseHandler = DatabaseHandler()

    @override
    def UploadCsv(
        self, request: aids_pb2.Chunk, context: grpc.ServicerContext
    ) -> aids_pb2.UploadResponse:
        """
        Streams a CSV into the server.
        """

        file_content = request.content
        file_name = request.file_name
        file_date = datetime.datetime.now(datetime.timezone.utc)

        if not file_name:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("File name is required.")
            return aids_pb2.UploadResponse()

        try:
            file_path = self.db_handler.save_csv_file(file_content, file_name)

            dataset = Dataset(file_name=file_name, file_route=file_path, date=file_date)
            dataset_id = self.db_handler.add_dataset(dataset)

            return aids_pb2.UploadResponse(
                id=dataset_id, message=f"File '{file_name}' uploaded successfully."
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occurred: {e}")
            return aids_pb2.UploadResponse()

    @override
    def GetDatasetSummary(
        self, request: aids_pb2.DatasetRequest, context: grpc.ServicerContext
    ) -> aids_pb2.SummaryResponse:
        """
        Gets the summary of a dataset based on its file ID.
        """
        logging.info("Function GetDatasetSummary called")

        # Name of the operation for the cache. Dont touch.
        CACHE_OPERATION_NAME = "describe"

        dataset_id = request.id

        # Check cache first
        cached_summary = self.db_handler.get_cache(dataset_id, CACHE_OPERATION_NAME)
        if cached_summary:
            logging.info(
                f"Function GetDatasetSummary returned cached value {cached_summary}"
            )
            return aids_pb2.SummaryResponse(summary_data=cached_summary)

        file_route = self.db_handler.get_file_route(dataset_id)

        if not file_route or file_route == "":
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Dataset with id {dataset_id} not found.")

            logging.info(
                f"Function GetDatasetSummary failed with route value {file_route}"
            )
            return aids_pb2.SummaryResponse()

        try:
            df = pd.read_csv(file_route)
            summary = df.describe().to_json()

            # Add to cache
            self.db_handler.add_cache(dataset_id, CACHE_OPERATION_NAME, summary)

            logging.info(f"Function GetDatasetSummary returned value {summary}")
            return aids_pb2.SummaryResponse(summary_data=summary)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to generate summary: {e}")

            logging.error(
                f"Function GetDatasetSummary failed to generate summary with error: {e}"
            )

            return aids_pb2.SummaryResponse()

    @override
    def ListSavedDatasets(
        self, request: aids_pb2.DatasetListResponse, context: grpc.ServicerContext
    ) -> aids_pb2.DatasetListResponse:
        """
        Returns the list of all saved datasets to the server.
        """
        try:
            saved_files = self.db_handler.get_saved_files()
            datasets: list[aids_pb2.DatasetInfo] = []
            for file_id, file_name, created_at in saved_files:
                created_at_str = created_at.strftime("%Y-%m-%d %H:%M:%S")
                datasets.append(
                    aids_pb2.DatasetInfo(
                        id=file_id, name=file_name, created_at=created_at_str
                    )
                )

            return aids_pb2.DatasetListResponse(datasets=datasets)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to list datasets: {e}")
            return aids_pb2.DatasetListResponse()

    @override
    def DeleteDataset(
        self, request: aids_pb2.DatasetRequest, context: grpc.ServicerContext
    ) -> Empty:
        """
        Function for deleting a dataset in the backend.
        """

        try:
            # check if the dataset exists before attempting to delete
            file_route = self.db_handler.get_file_route(request.id)
            if file_route is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Dataset with id {request.id} not found.")
                return Empty()

            self.db_handler.remove_dataset(request.id)

            # delete the actual file from the disk
            if os.path.exists(file_route):
                os.remove(file_route)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to delete dataset: {e}")
            return Empty()

        return Empty()

    @override
    def DownloadDataset(
        self, request: aids_pb2.DatasetRequest, context: grpc.ServicerContext
    ) -> aids_pb2.Chunk:
        dataset_id = request.id
        file_route = self.db_handler.get_file_route(dataset_id)
        try:
            if not file_route:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Dataset with id {dataset_id} not found.")
                return aids_pb2.Chunk()

            # get file name from the file_route
            file_name = os.path.basename(file_route)

            with open(file_route, "rb") as f:
                file_content = f.read()

            return aids_pb2.Chunk(content=file_content, file_name=file_name)

        except FileNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"File not found at {file_route}.")
            return aids_pb2.Chunk()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to download dataset: {e}")
            return aids_pb2.Chunk()

    @override
    def GetChart(
        self, request: aids_pb2.ChartRequest, context: grpc.ServicerContext
    ) -> aids_pb2.ChartResponse:
        logging.info("Function GetChart called")

        file_id = request.id
        x_axis = request.x_axis
        y_axis = request.y_axis

        CACHE_OPERATION_NAME = "getchart"
        CACHE_OPERATION_FULLN = f"{CACHE_OPERATION_NAME}_{x_axis}_{y_axis}"

        cached_svg = self.db_handler.get_cache(file_id, CACHE_OPERATION_FULLN)
        if cached_svg:
            logging.info(f"Function GetChart returned with cached value: {cached_svg}")
            return aids_pb2.ChartResponse(svg=cached_svg)

        file_route = self.db_handler.get_file_route(file_id)

        try:
            if file_route is None or file_route == "":
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Dataset with id {request.id} not found.")
                logging.info(
                    f"Function GetChart failed with file_route value: {file_route}"
                )
                return aids_pb2.ChartResponse()

            df = pd.read_csv(file_route)
            # df = pd.read_csv(file_route, usecols=[x_axis, y_axis])

            svg_buffer = io.StringIO()

            sns.set_theme(style="whitegrid")
            plot = sns.scatterplot(x=x_axis, y=y_axis, data=df)
            plot.set_xlabel(x_axis)
            plot.set_ylabel(y_axis)

            plt.savefig(svg_buffer, format="svg")
            plt.close()

            svg = svg_buffer.getvalue()

            self.db_handler.add_cache(file_id, CACHE_OPERATION_FULLN, svg)

            logging.info(f"Function GetChart returned with value: {svg}")
            return aids_pb2.ChartResponse(svg=svg)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to get/generate chart: {e}")
            logging.error(f"Function GetChart failed with error: {e}")
            return aids_pb2.ChartResponse()
