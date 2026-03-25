<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import ForumSelect from '$lib/components/ForumSelect.svelte';
	import { getGraphContext, type ViewMode } from '$lib/graph-context.svelte.js';

	interface Props {
		forums: { id: string; name: string }[];
	}

	let { forums }: Props = $props();
	const ctx = getGraphContext();

	const modes: { value: ViewMode; label: string }[] = [
		{ value: 'threads', label: 'Threads' },
		{ value: 'links', label: 'Links' },
		{ value: 'users', label: 'Users' }
	];
</script>

<div class="absolute top-4 left-4 z-10 flex items-center gap-2">
	<div class="flex gap-1 rounded-md border border-zinc-700 bg-zinc-900/90 p-1 backdrop-blur">
		{#each modes as mode (mode.value)}
			<Button
				variant={ctx.viewMode === mode.value ? 'secondary' : 'ghost'}
				size="xs"
				class="text-xs {ctx.viewMode === mode.value ? '' : 'text-zinc-400'}"
				onclick={() => ctx.switchView(mode.value)}
			>
				{mode.label}
			</Button>
		{/each}
	</div>

	<ForumSelect {forums} />
</div>
