<script lang="ts">
	import {
		Collapsible,
		CollapsibleContent,
		CollapsibleTrigger
	} from '$lib/components/ui/collapsible/index.js';
	import { formatDate, truncate } from '$lib/graph-context.svelte.js';
	import type { LinkedDoc } from '$lib/types.js';

	interface Props {
		links: LinkedDoc[];
	}

	let { links }: Props = $props();
	let open = $state(false);
</script>

<Collapsible bind:open>
	<CollapsibleTrigger
		class="flex w-full items-center justify-between rounded-lg border border-border bg-card px-4 py-3 text-left transition-colors hover:bg-accent"
	>
		<span class="text-sm font-medium">Shared Links</span>
		<span class="text-xs text-muted-foreground">{open ? '−' : '+'}</span>
	</CollapsibleTrigger>
	<CollapsibleContent>
		<div class="max-h-80 overflow-y-auto rounded-b-lg border border-t-0 border-border p-4">
			{#each links as link (link)}
				<div class="border-b border-border py-3 last:border-b-0">
					<a
						href={link.id}
						target="_blank"
						rel="noopener noreferrer"
						class="text-sm font-medium text-blue-400 hover:underline"
					>
						{link.title ?? link.id}
					</a>
					{#if link.siteName}
						<span class="text-xs text-muted-foreground"> &middot; {link.siteName}</span>
					{/if}
					{#if link.description}
						<p class="mt-1 text-sm text-muted-foreground">{truncate(link.description, 120)}</p>
					{/if}
					<p class="mt-1 text-xs text-muted-foreground">
						Shared by {link.sharedBy ?? 'Unknown'}{#if link.sharedAt}
							&middot; {formatDate(link.sharedAt)}{/if}
					</p>
				</div>
			{/each}
		</div>
	</CollapsibleContent>
</Collapsible>
