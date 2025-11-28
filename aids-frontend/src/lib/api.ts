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

import { browser } from '$app/environment';

// Define the RPC client
const transport = new GrpcWebFetchTransport({
	baseUrl: browser ? window.location.origin : ''
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
