<script lang="ts">
	import GraphExplorer from '$lib/components/GraphExplorer.svelte';
	import NodeDetail from '$lib/components/NodeDetail.svelte';
	import ViewSwitcher from '$lib/components/ViewSwitcher.svelte';
	import GraphStatusBar from '$lib/components/GraphStatusBar.svelte';
	import ActivityFeed from '$lib/components/ActivityFeed.svelte';
	import LinksFeed from '$lib/components/LinksFeed.svelte';
	import SparqlDrawer from '$lib/components/SparqlDrawer.svelte';
	import { createGraphContext, setGraphContext } from '$lib/graph-context.svelte.js';

	let { data } = $props();

	const ctx = createGraphContext(() => data.graphData);
	setGraphContext(ctx);
</script>

<div class="flex h-full flex-col gap-3 p-4">
	<!-- Graph Explorer (hero) -->
	<section class="relative min-h-0 flex-1">
		<ViewSwitcher forums={data.forums} />

		{#if ctx.loadingGraph}
			<div class="flex h-full items-center justify-center rounded-lg border bg-zinc-950">
				<p class="animate-pulse text-sm text-muted-foreground">Loading graph...</p>
			</div>
		{:else}
			<GraphExplorer
				data={ctx.graphData}
				onselect={(n: { id: string; data?: Record<string, string> }) => (ctx.selectedNode = n)}
			/>
		{/if}

		<NodeDetail node={ctx.selectedNode} onclose={() => (ctx.selectedNode = null)} />

		<GraphStatusBar />
	</section>

	<!-- Collapsible Panels -->
	<div class="grid grid-cols-1 gap-3 md:grid-cols-2">
		<ActivityFeed posts={data.posts} />
		<LinksFeed links={data.links} />
	</div>

	<SparqlDrawer queryLibrary={data.queryLibrary} />
</div>
