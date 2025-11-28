<script lang="ts">
	import { onMount } from 'svelte';
	import { datasets, fetchDatasets } from '$lib/stores';
	import { aidsClient, DatasetInfo, DatasetRequest } from '$lib/api';

	let selectedDataset: DatasetInfo | null = null;
	let summaryData: string | null = null;
	let loadingSummary: boolean = false;

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
					class="mt-2 cursor-pointer rounded p-2 {selectedDataset?.id === dataset.id ? 'bg-blue-200' : 'hover:bg-gray-300'}"
				>
					<button onclick={() => selectDataset(dataset)}>
						{dataset.id})  {dataset.name} 
					</button>
				</li>
			{:else}
				<li>No datasets found.</li>
			{/each}
		</ul>
	</div>
	<div class="w-3/4 overflow-y-auto p-4">
		<h2 class="mb-4 text-xl font-bold">Selected Dataset</h2>
		{#if selectedDataset}
			<div class="rounded-lg bg-white p-4 shadow-md">
				<p><strong>Name:</strong> {selectedDataset.name}</p>
				<p><strong>ID:</strong> {selectedDataset.id}</p>
				<p><strong>Created At:</strong> {selectedDataset.createdAt}</p>
				<h3 class="mt-4 text-lg font-semibold">Summary:</h3>
				{#if loadingSummary}
					<p>Loading summary...</p>
				{:else if summaryData}
					<pre class="whitespace-pre-wrap text-sm">{summaryData}</pre>
				{:else}
					<p>No summary available.</p>
				{/if}
			</div>
		{:else}
			<div class="rounded-lg bg-white p-4 shadow-md">
				<p>Select a dataset to view its details.</p>
			</div>
		{/if}
	</div>
</div>


