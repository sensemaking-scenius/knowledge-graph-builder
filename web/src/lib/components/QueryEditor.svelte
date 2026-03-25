<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import { untrack } from 'svelte';
	import { EditorView, basicSetup } from 'codemirror';
	import { EditorState } from '@codemirror/state';
	import { sql } from '@codemirror/lang-sql';
	import { oneDark } from '@codemirror/theme-one-dark';

	let {
		value = $bindable(''),
		onrun
	}: {
		value?: string;
		onrun?: (query: string) => void;
	} = $props();

	let container: HTMLDivElement;
	let view: EditorView;
	let skipNextUpdate = false;

	// Initialize editor once when container is available
	$effect(() => {
		if (!container) return;

		const initialDoc = untrack(() => value);

		const state = EditorState.create({
			doc: initialDoc,
			extensions: [
				basicSetup,
				sql(),
				oneDark,
				EditorView.updateListener.of((update) => {
					if (update.docChanged) {
						skipNextUpdate = true;
						value = update.state.doc.toString();
					}
				}),
				EditorView.theme({
					'&': { height: '300px' },
					'.cm-scroller': { overflow: 'auto' }
				})
			]
		});

		view = new EditorView({ state, parent: container });

		return () => {
			view.destroy();
		};
	});

	// Sync external value changes into editor (e.g. loading a query from library)
	$effect(() => {
		const current = value;
		if (view && !skipNextUpdate && current !== view.state.doc.toString()) {
			view.dispatch({
				changes: { from: 0, to: view.state.doc.length, insert: current }
			});
		}
		skipNextUpdate = false;
	});
</script>

<div class="flex flex-col gap-2">
	<div bind:this={container} class="overflow-hidden rounded-md border"></div>
	{#if onrun}
		<div class="flex gap-2">
			<Button onclick={() => onrun?.(value)}>Run Query</Button>
		</div>
	{/if}
</div>
