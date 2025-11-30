// src/lib/stores.ts
import { writable } from 'svelte/store';
import { aidsClient, DatasetInfo, Empty } from './api';

export const datasets = writable<DatasetInfo[]>([]);

export async function fetchDatasets() {
	try {
		const call = aidsClient.listSavedDatasets(Empty.create());
		const response = await call.response;
		datasets.set(response.datasets);
	} catch (error) {
		console.error('Error fetching datasets for store:', error);
	}
}
