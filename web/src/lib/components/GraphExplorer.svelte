<script lang="ts">
	import { untrack } from 'svelte';
	import type { GraphData } from '$lib/types.js';

	let {
		data,
		onselect
	}: {
		data: GraphData;
		onselect?: (node: { id: string; data?: Record<string, string> }) => void;
	} = $props();

	let container: HTMLDivElement;
	let cy: import('cytoscape').Core | null = null;

	$effect(() => {
		if (!container) return;

		const currentData = untrack(() => data);

		let mounted = true;

		import('cytoscape').then(({ default: cytoscape }) => {
			if (!mounted) return;

			cy = cytoscape({
				container,
				elements: graphDataToElements(currentData),
				style: [
					{
						selector: 'node[type="post"]',
						style: {
							'background-color': '#6366f1',
							label: 'data(label)',
							'font-size': '10px',
							'text-wrap': 'ellipsis',
							'text-max-width': '120px',
							color: '#e2e8f0',
							width: 20,
							height: 20
						}
					},
					{
						selector: 'node[type="user"]',
						style: {
							'background-color': '#22c55e',
							label: 'data(label)',
							'font-size': '12px',
							color: '#e2e8f0',
							width: 30,
							height: 30,
							shape: 'diamond'
						}
					},
					{
						selector: 'node[type="link"]',
						style: {
							'background-color': '#f59e0b',
							label: 'data(label)',
							'font-size': '9px',
							'text-wrap': 'ellipsis',
							'text-max-width': '100px',
							color: '#e2e8f0',
							width: 16,
							height: 16,
							shape: 'round-rectangle'
						}
					},
					{
						selector: 'edge',
						style: {
							width: 1,
							'line-color': '#475569',
							'target-arrow-color': '#475569',
							'target-arrow-shape': 'triangle',
							'curve-style': 'bezier',
							'arrow-scale': 0.6
						}
					},
					{
						selector: 'node:selected',
						style: {
							'border-width': 2,
							'border-color': '#f8fafc'
						}
					}
				],
				layout: {
					name: 'cose',
					animate: false,
					nodeOverlap: 20,
					idealEdgeLength: () => 80,
					nodeRepulsion: () => 8000
				},
				minZoom: 0.1,
				maxZoom: 5
			});

			cy.on('tap', 'node', (evt) => {
				const node = evt.target;
				onselect?.({
					id: node.id(),
					data: node.data()
				});
			});
		});

		return () => {
			mounted = false;
			cy?.destroy();
			cy = null;
		};
	});

	// Update graph data when it changes externally (e.g. view switch, filter)
	$effect(() => {
		const d = data;
		if (!cy) return;

		cy.elements().remove();
		cy.add(graphDataToElements(d));
		cy.layout({
			name: 'cose',
			animate: true,
			animationDuration: 500,
			nodeOverlap: 20,
			idealEdgeLength: () => 80,
			nodeRepulsion: () => 8000
		}).run();
	});

	function graphDataToElements(gd: GraphData): cytoscape.ElementDefinition[] {
		const nodes = gd.nodes.map((n) => ({
			data: { id: n.id, label: n.label, type: n.type, ...n.data }
		}));
		const edges = gd.edges.map((e, i) => ({
			data: { id: `e${i}`, source: e.source, target: e.target, type: e.type }
		}));
		return [...nodes, ...edges];
	}
</script>

<div bind:this={container} class="h-full w-full rounded-lg border bg-zinc-950"></div>
