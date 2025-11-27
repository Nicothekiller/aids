from collections.abc import Iterator
from typing import override
import aids_pb2
import aids_pb2_grpc
import grpc
import pandas as pd
from database_handler import DatabaseHandler, Dataset


class AidsServiceServicer(aids_pb2_grpc.AidsServiceServicer):
    """
    Provides methods that implement functionality of the aids server.
    """

    def __init__(self) -> None:
        self.db_handler: DatabaseHandler = DatabaseHandler()

    @override
    def UploadCsv(
        self, request_iterator: Iterator[aids_pb2.Chunk], context: grpc.ServicerContext
    ) -> aids_pb2.UploadResponse:
        """
        Streams a CSV into the server.
        """
        file_content = b""
        file_name = ""
        for chunk in request_iterator:
            if chunk.file_name:
                file_name = chunk.file_name
            file_content += chunk.content

        if not file_name:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("File name is required.")
            return aids_pb2.UploadResponse()

        try:
            file_path = self.db_handler.save_csv_file(file_content, file_name)

            dataset = Dataset(file_name=file_name, file_route=file_path)
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
        # Name of the operation for the cache. Dont touch.
        CACHE_OPERATION_NAME = "describe"

        dataset_id = request.id

        # Check cache first
        cached_summary = self.db_handler.get_cache(dataset_id, CACHE_OPERATION_NAME)
        if cached_summary:
            return aids_pb2.SummaryResponse(summary_data=cached_summary)

        file_route = self.db_handler.get_file_route(dataset_id)

        if not file_route:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Dataset with id {dataset_id} not found.")
            return aids_pb2.SummaryResponse()

        try:
            df = pd.read_csv(file_route)
            summary = df.describe().to_json()

            # Add to cache
            self.db_handler.add_cache(dataset_id, CACHE_OPERATION_NAME, summary)

            return aids_pb2.SummaryResponse(summary_data=summary)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to generate summary: {e}")
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
