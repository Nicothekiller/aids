// src/lib/api.ts
import { GrpcWebFetchTransport } from '@protobuf-ts/grpcweb-transport';
import { AidsServiceClient } from './protos/aids.client';
import {
	Chunk,
	DatasetInfo,
	DatasetListResponse,
	DatasetRequest,
	SummaryResponse,
	UploadResponse,
	ChartRequest,
	ChartResponse
} from './protos/aids';
import { Empty } from './protos/google/protobuf/empty';

import { browser } from '$app/environment';

// Define the RPC client
const transport = new GrpcWebFetchTransport({
	baseUrl: browser ? window.location.origin : ''
});

// Instantiate the gRPC client
export const aidsClient = new AidsServiceClient(transport);

// Function to delete a dataset
export async function deleteDataset(id: bigint): Promise<void> {
	const request = DatasetRequest.create({ id });
	await aidsClient.deleteDataset(request);
}

// Function to download a dataset
export async function downloadDataset(id: bigint): Promise<Chunk> {
	const request = DatasetRequest.create({ id });
	const call = aidsClient.downloadDataset(request);
	const response = await call.response;
	return response;
}

export async function getChart(id: bigint, xAxis: string, yAxis: string): Promise<ChartResponse> {
	const request = ChartRequest.create({ id, xAxis, yAxis });
	const call = aidsClient.getChart(request);
	const response = await call.response;
	return response;
}

// Export message types for convenience
export {
	Chunk,
	UploadResponse,
	DatasetRequest,
	SummaryResponse,
	DatasetInfo,
	DatasetListResponse,
	Empty,
	ChartRequest,
	ChartResponse
};
