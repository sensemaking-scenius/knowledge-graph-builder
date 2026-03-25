<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import { getGraphContext } from '$lib/graph-context.svelte.js';

	const ctx = getGraphContext();
</script>

<div class="absolute right-4 bottom-4 left-4 z-10 flex items-center justify-between">
	<div
		class="rounded-md border border-zinc-700 bg-zinc-900/90 px-3 py-1.5 text-xs text-zinc-400 backdrop-blur"
	>
		{ctx.graphData.nodes.length} nodes &middot; {ctx.graphData.edges.length} edges
	</div>
	<Button
		variant="outline"
		size="sm"
		class="border-zinc-700 bg-zinc-900/90 text-xs text-zinc-300 backdrop-blur"
		onclick={() => (ctx.sparqlOpen = true)}
	>
		SPARQL
	</Button>
</div>
