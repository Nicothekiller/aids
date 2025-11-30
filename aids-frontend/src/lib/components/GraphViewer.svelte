<script lang="ts">
	import type { DatasetInfo } from '$lib/api';
	import { getChart, ChartRequest } from '$lib/api';

	export let parsedSummaryData: Array<[string, Record<string, string>]> | null = null;
	export let selectedDataset: DatasetInfo | null = null;

	let fields: string[] = [];
	let selectedX: string | null = null;
	let selectedY: string | null = null;
	let svgContent: string | null = null;
	let loading: boolean = false;

	$: fields = parsedSummaryData?.map(([fieldName]) => fieldName) ?? [];

	$: {
		if (fields.length > 0) {
			if (!selectedX || !fields.includes(selectedX)) {
				selectedX = fields[0];
			}
			if (!selectedY || !fields.includes(selectedY)) {
				selectedY = fields[1] || fields[0]; // Fallback to first field if only one
			}
		}
	}

	async function generateGraph() {
		if (!selectedDataset || !selectedX || !selectedY) {
			return;
		}

		loading = true;
		svgContent = null;

		try {
			const response = await getChart(selectedDataset.id, selectedX, selectedY);
			console.log(response.svg);
			svgContent = response.svg;
		} catch (error) {
			console.error('Error generating chart:', error);
			svgContent = '<p>Error generating chart.</p>';
		} finally {
			loading = false;
		}
	}

	function downloadSVG() {
		if (!svgContent || !selectedX || !selectedY) {
			return;
		}

		const blob = new Blob([svgContent], { type: 'image/svg+xml' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `${selectedX}-${selectedY}.svg`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}
</script>

<div class="mt-8">
	<h3 class="text-lg font-semibold">Graph Viewer</h3>
	{#if fields.length > 0}
		<div class="mt-4 flex items-center space-x-4">
			<div>
				<label for="x-axis-select" class="block text-sm font-medium text-gray-700"
					>X-Axis:</label
				>
				<select
					id="x-axis-select"
					bind:value={selectedX}
					class="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
				>
					{#each fields as field}
						<option value={field}>{field}</option>
					{/each}
				</select>
			</div>
			<div>
				<label for="y-axis-select" class="block text-sm font-medium text-gray-700"
					>Y-Axis:</label
				>
				<select
					id="y-axis-select"
					bind:value={selectedY}
					class="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm"
				>
					{#each fields as field}
						<option value={field}>{field}</option>
					{/each}
				</select>
			</div>
			<button
				onclick={generateGraph}
				disabled={loading || !selectedX || !selectedY}
				class="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50"
			>
				{#if loading}
					Generating...
				{:else}
					Generate Graph
				{/if}
			</button>
			<button
				onclick={downloadSVG}
				disabled={!svgContent}
				class="inline-flex items-center rounded-md border border-transparent bg-green-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50"
			>
				Download SVG
			</button>
		</div>
	{/if}

	{#if svgContent}
		<div class="mt-4 rounded-lg bg-white p-4 shadow-md">
			{@html svgContent}
		</div>
	{/if}
</div>
