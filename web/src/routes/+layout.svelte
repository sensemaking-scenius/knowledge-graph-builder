<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="flex h-screen flex-col overflow-hidden">
	<header class="border-border flex items-center justify-between border-b px-6 py-3">
		<h1 class="text-foreground text-lg font-semibold tracking-tight">Scenius Knowledge Graph</h1>
		<div class="text-muted-foreground text-sm">
			<!-- Auth placeholder -->
		</div>
	</header>
	<main class="flex-1 overflow-y-auto">
		{@render children()}
	</main>
</div>
