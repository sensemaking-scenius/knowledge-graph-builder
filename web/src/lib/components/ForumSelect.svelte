<script lang="ts">
	import * as Select from '$lib/components/ui/select/index.js';
	import { getGraphContext } from '$lib/graph-context.svelte.js';

	interface Props {
		forums: { id: string; name: string }[];
	}

	let { forums }: Props = $props();
	const ctx = getGraphContext();

	let value = $state<string | undefined>(undefined);

	async function filterByForum(forumId: string | undefined) {
		value = forumId;
		await ctx.switchView(ctx.viewMode);
	}
</script>

<Select.Root
	type="single"
	name="selectedForum"
	bind:value
	onValueChange={(v) => filterByForum(v === '__all__' ? undefined : v)}
>
	<Select.Trigger>
		<span>{value ? (forums.find((f) => f.id === value)?.name ?? 'Forum') : 'All Forums'}</span>
	</Select.Trigger>
	<Select.Content>
		<Select.Item value="__all__">All Forums</Select.Item>
		{#each forums as forum (forum.id)}
			<Select.Item value={forum.id}>{forum.name}</Select.Item>
		{/each}
	</Select.Content>
</Select.Root>
