<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex flex-col h-screen">
    <header class="flex items-center justify-between p-4 bg-gray-800 text-white">
        <div class="text-2xl font-bold">
            AIDS
        </div>
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Upload Dataset
        </button>
    </header>
    <main class="flex-1 flex overflow-hidden">
        {@render children?.()}
    </main>
</div>
