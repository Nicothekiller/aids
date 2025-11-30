<script lang="ts">
	import type { DatasetInfo } from '$lib/api';
	import GraphViewer from '$lib/components/GraphViewer.svelte';

	export let selectedDataset: DatasetInfo | null = null;
	export let loadingAction: boolean = false;
	export let loadingSummary: boolean = false;
	export let parsedSummaryData: Array<[string, Record<string, string>]> | null = null;

	export let onDelete: () => void;
	export let onDownload: () => void;
</script>

<div class="flex justify-between mt-4 pb-4">
	<h2 class="mb-4 text-xl font-bold">Selected Dataset</h2>
	{#if selectedDataset}
		<div class="flex space-x-4">
			<button
				onclick={onDelete}
				disabled={loadingAction}
				class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50"
			>
				{#if loadingAction}Deleting...{:else}Delete Dataset{/if}
			</button>
			<button
				onclick={onDownload}
				disabled={loadingAction}
				class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
			>
				{#if loadingAction}Downloading...{:else}Download Dataset{/if}
			</button>
		</div>
	{/if}
</div>
{#if selectedDataset}
	<div class="rounded-lg bg-white p-4 shadow-md">
		<p><strong>Name:</strong> {selectedDataset.name}</p>
		<p><strong>ID:</strong> {selectedDataset.id}</p>
		<p><strong>Created At:</strong> {selectedDataset.createdAt}</p>
		<h3 class="mt-4 text-lg font-semibold">Summary:</h3>
		{#if loadingSummary}
			<p>Loading summary...</p>
		{:else if parsedSummaryData}
			{#each parsedSummaryData as [fieldName, fieldContent]}
				<h4 class="mt-3 text-md font-semibold">{fieldName}</h4>
				<ul class="list-disc pl-5">
					{#each Object.entries(fieldContent) as [key, value]}
						<li><strong>{key}:</strong> {value}</li>
					{/each}
				</ul>
			{/each}
		{:else}
			<p>No summary available.</p>
		{/if}
	</div>
	<GraphViewer {selectedDataset} {parsedSummaryData} />
{:else}
	<div class="rounded-lg bg-white p-4 shadow-md">
		<p>Select a dataset to view its details.</p>
	</div>
{/if}
