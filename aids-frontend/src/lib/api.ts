// src/lib/api.ts
import { GrpcWebFetchTransport } from '@protobuf-ts/grpcweb-transport';
import { AidsServiceClient } from './protos/aids.client';
import {
	Chunk,
	DatasetInfo,
	DatasetListResponse,
	DatasetRequest,
	SummaryResponse,
	UploadResponse
} from './protos/aids';
import { Empty } from './protos/google/protobuf/empty';

// Define the RPC client
const transport = new GrpcWebFetchTransport({
	baseUrl: 'http://127.0.0.1:8080'
});

// Instantiate the gRPC client
export const aidsClient = new AidsServiceClient(transport);

// Export message types for convenience
export {
	Chunk,
	UploadResponse,
	DatasetRequest,
	SummaryResponse,
	DatasetInfo,
	DatasetListResponse,
	Empty
};
