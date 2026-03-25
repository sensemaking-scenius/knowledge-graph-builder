<script lang="ts">
	import {
		Drawer,
		DrawerContent,
		DrawerHeader,
		DrawerTitle
	} from '$lib/components/ui/drawer/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import QueryEditor from '$lib/components/QueryEditor.svelte';
	import { getGraphContext } from '$lib/graph-context.svelte.js';

	interface Props {
		queryLibrary: { name: string; sparql: string }[];
	}

	let { queryLibrary }: Props = $props();
	const ctx = getGraphContext();
</script>

<Drawer bind:open={ctx.sparqlOpen}>
	<DrawerContent class="max-h-[85vh]">
		<DrawerHeader class="pb-2">
			<DrawerTitle>SPARQL Playground</DrawerTitle>
		</DrawerHeader>
		<div class="flex flex-col gap-3 overflow-y-auto px-4 pb-4">
			<div class="flex flex-wrap gap-2">
				<Select.Root
					type="single"
					onValueChange={(v) => {
						const q = queryLibrary.find((q) => q.name === v);
						if (q) ctx.sparqlQuery = q.sparql;
					}}
				>
					<Select.Trigger class="h-8 w-52 text-xs">
						<span>Load pre-built query...</span>
					</Select.Trigger>
					<Select.Content>
						{#each queryLibrary as q (q)}
							<Select.Item value={q.name}>
								{q.name}
							</Select.Item>
						{/each}
					</Select.Content>
				</Select.Root>

				{#if ctx.savedQueries.length > 0}
					<Select.Root
						type="single"
						onValueChange={(v) => {
							const q = ctx.savedQueries.find((q) => q.name === v);
							if (q) ctx.sparqlQuery = q.sparql;
						}}
					>
						<Select.Trigger class="h-8 w-44 text-xs">
							<span>Saved queries...</span>
						</Select.Trigger>
						<Select.Content>
							{#each ctx.savedQueries as q (q)}
								<Select.Item value={q.name}>
									{q.name}
								</Select.Item>
							{/each}
						</Select.Content>
					</Select.Root>
				{/if}

				<Button variant="outline" size="sm" onclick={ctx.saveQuery}>Save</Button>
			</div>

			<QueryEditor bind:value={ctx.sparqlQuery} onrun={ctx.runSparql} />

			{#if ctx.sparqlRunning}
				<p class="animate-pulse text-sm text-muted-foreground">Running query...</p>
			{/if}

			{#if ctx.sparqlError}
				<pre
					class="overflow-x-auto rounded-md bg-red-950/50 p-3 text-xs text-red-400">{ctx.sparqlError}</pre>
			{/if}

			{#if ctx.sparqlResults}
				<div class="max-h-64 overflow-auto rounded-md border">
					<table class="w-full text-xs">
						<thead class="sticky top-0 bg-muted">
							<tr>
								{#each ctx.sparqlResults.head.vars as v (v)}
									<th class="px-3 py-2 text-left font-medium">{v}</th>
								{/each}
							</tr>
						</thead>
						<tbody>
							{#each ctx.sparqlResults.results.bindings as row (row)}
								<tr class="border-t border-border">
									{#each ctx.sparqlResults.head.vars as v (v)}
										<td class="max-w-xs truncate px-3 py-2">{row[v]?.value ?? ''}</td>
									{/each}
								</tr>
							{/each}
						</tbody>
					</table>
					<p class="border-t px-3 py-2 text-xs text-muted-foreground">
						{ctx.sparqlResults.results.bindings.length} results
					</p>
				</div>
			{/if}
		</div>
	</DrawerContent>
</Drawer>
