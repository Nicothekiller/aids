<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { aidsClient, Chunk } from '$lib/api';
	import { fetchDatasets } from '$lib/stores'; // Import fetchDatasets from the store

	let { children } = $props();
	let fileInput: HTMLInputElement;

	async function handleFileUpload(event: Event) {
		const target = event.target as HTMLInputElement;
		const file = target.files?.[0];

		if (!file) {
			return;
		}

		if (!file.name.endsWith('.csv')) {
			return;
		}

		try {
			const fileContent = await file.arrayBuffer();
			const fileName = file.name;

			const chunk = Chunk.create({ content: new Uint8Array(fileContent), fileName: fileName });
			const call = aidsClient.uploadCsv(chunk);
			await call.response; // Await the response, but no alert needed

			fetchDatasets(); // Call fetchDatasets to refresh the list
		} catch (error) {
			console.error('Error uploading file:', error);
		}
	}

	function triggerFileInput() {
		if (fileInput) {
			fileInput.click();
		}
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex h-screen flex-col">
	<header class="flex items-center justify-between bg-gray-800 p-4 text-white">
		<button class="rounded bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700" onclick={triggerFileInput}>
			Upload Dataset
		</button>
		<div class="text-2xl font-bold">AIDS</div>
	</header>
	<main class="flex flex-1 overflow-hidden">
		{@render children?.()}
	</main>
	<input type="file" accept=".csv" bind:this={fileInput} onchange={handleFileUpload} class="hidden" />
</div>
