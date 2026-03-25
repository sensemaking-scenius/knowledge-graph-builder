<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';

	let {
		node,
		onclose
	}: {
		node: { id: string; data?: Record<string, string> } | null;
		onclose?: () => void;
	} = $props();
</script>

{#if node}
	<div class="border-border bg-card absolute right-4 top-4 z-10 w-80 rounded-lg border p-4 shadow-lg">
		<div class="mb-2 flex items-center justify-between">
			<span class="text-muted-foreground text-xs font-medium uppercase tracking-wide">
				{node.data?.type ?? 'Node'}
			</span>
			<Button variant="ghost" size="icon-xs" class="text-muted-foreground hover:text-foreground" onclick={() => onclose?.()}>
				&times;
			</Button>
		</div>

		{#if node.data?.creator}
			<p class="text-sm font-medium">{node.data.creator}</p>
		{/if}

		{#if node.data?.created}
			<p class="text-muted-foreground mb-2 text-xs">
				{new Date(node.data.created).toLocaleString()}
			</p>
		{/if}

		{#if node.data?.content}
			<p class="text-foreground max-h-48 overflow-y-auto text-sm leading-relaxed">
				{node.data.content}
			</p>
		{:else if node.data?.label}
			<p class="text-foreground text-sm">{node.data.label}</p>
		{/if}

		<p class="text-muted-foreground mt-2 truncate text-xs">{node.id}</p>
	</div>
{/if}
