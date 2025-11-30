<script lang="ts">
	import { onMount } from 'svelte';
	import { datasets, fetchDatasets } from '$lib/stores';
	import { aidsClient, DatasetInfo, DatasetRequest, deleteDataset, downloadDataset } from '$lib/api';
	import DataViewer from '$lib/components/DataViewer.svelte';

	let selectedDataset: DatasetInfo | null = null;
	let summaryData: string | null = null;
	let loadingSummary: boolean = false;
	let loadingAction: boolean = false; // New loading state for actions
	let parsedSummaryData: Array<[string, Record<string, string>]> | null = null;

	$: if (summaryData) {
		try {
			parsedSummaryData = Object.entries(JSON.parse(summaryData));
		} catch (error) {
			console.error('Error parsing summary data:', error);
			parsedSummaryData = null;
		}
	} else {
		parsedSummaryData = null;
	}

	async function selectDataset(dataset: DatasetInfo) {
		selectedDataset = dataset;
		summaryData = null; // Clear previous summary
		loadingSummary = true;

		try {
			const request = DatasetRequest.create({ id: BigInt(dataset.id) }); // Convert number to BigInt
			const call = aidsClient.getDatasetSummary(request);
			const response = await call.response;
			summaryData = response.summaryData;
		} catch (error) {
			console.error('Error fetching dataset summary:', error);
			summaryData = 'Error loading summary.';
		} finally {
			loadingSummary = false;
		}
	}

	async function handleDelete() {
		if (!selectedDataset) return;
		if (!confirm(`Are you sure you want to delete dataset "${selectedDataset.name}"?`)) return;

		loadingAction = true;
		try {
			await deleteDataset(BigInt(selectedDataset.id));
			alert('Dataset deleted successfully!');
			selectedDataset = null; // Clear selected dataset
			summaryData = null; // Clear summary
			fetchDatasets(); // Refresh the list of datasets
		} catch (error) {
			console.error('Error deleting dataset:', error);
			alert('Failed to delete dataset.');
		} finally {
			loadingAction = false;
		}
	}

	async function handleDownload() {
		if (!selectedDataset) return;

		loadingAction = true;
		try {
			const chunk = await downloadDataset(BigInt(selectedDataset.id));

			const contentArray = new Uint8Array(chunk.content);
			const blob = new Blob([contentArray], { type: 'text/csv' });
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = chunk.fileName || `${selectedDataset.name}.csv`;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);
			alert('Dataset downloaded successfully!');

		} catch (error) {
			console.error('Error downloading dataset:', error);
			alert('Failed to download dataset.');
		} finally {
			loadingAction = false;
		}
	}

	onMount(() => {
		fetchDatasets();
	});
</script>

<div class="flex h-full w-full">
	<div class="w-1/4 overflow-y-auto bg-gray-200 p-4">
		<h2 class="mb-4 text-xl font-bold">Datasets</h2>
		<ul>
			{#each $datasets as dataset (dataset.id)}
				<li
					class="mt-2 cursor-pointer rounded p-0 {selectedDataset?.id === dataset.id ? 'bg-blue-200' : 'hover:bg-gray-300'}"
				>
					<button onclick={() => selectDataset(dataset)} class="w-full h-full text-left p-2">
						{dataset.id})  {dataset.name} 
					</button>
				</li>
			{:else}
				<li>No datasets found.</li>
			{/each}
		</ul>
	</div>
	<div class="w-3/4 overflow-y-auto p-4">
		<DataViewer
			{selectedDataset}
			{loadingAction}
			{loadingSummary}
			{parsedSummaryData}
			onDelete={handleDelete}
			onDownload={handleDownload}
		/>
	</div>
</div>


