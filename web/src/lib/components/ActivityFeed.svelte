<script lang="ts">
	import {
		Collapsible,
		CollapsibleContent,
		CollapsibleTrigger
	} from '$lib/components/ui/collapsible/index.js';
	import { formatDate, truncate } from '$lib/graph-context.svelte.js';
	import type { Post } from '$lib/types.js';

	interface Props {
		posts: Post[];
	}

	let { posts }: Props = $props();
	let open = $state(false);
</script>

<Collapsible bind:open>
	<CollapsibleTrigger
		class="flex w-full items-center justify-between rounded-lg border border-border bg-card px-4 py-3 text-left transition-colors hover:bg-accent"
	>
		<span class="text-sm font-medium">Activity Feed</span>
		<span class="text-xs text-muted-foreground">{open ? '−' : '+'}</span>
	</CollapsibleTrigger>
	<CollapsibleContent>
		<div class="max-h-80 overflow-y-auto rounded-b-lg border border-t-0 border-border p-4">
			{#each posts as post (post.id)}
				<div class="border-b border-border py-3 last:border-b-0">
					<div class="mb-1 flex items-center gap-2">
						<span class="text-sm font-medium">{post.creatorName ?? 'Unknown'}</span>
						{#if post.containerName}
							<span class="text-xs text-muted-foreground">in {post.containerName}</span>
						{/if}
					</div>
					<p class="text-sm text-muted-foreground">{truncate(post.content)}</p>
					<p class="mt-1 text-xs text-muted-foreground">{formatDate(post.created)}</p>
				</div>
			{/each}
		</div>
	</CollapsibleContent>
</Collapsible>
