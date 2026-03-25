import { createContext } from 'svelte';
import type { GraphData, SparqlResults } from '$lib/types.js';

export type ViewMode = 'threads' | 'links' | 'users';

export interface GraphContext {
	viewMode: ViewMode;
	selectedNode: { id: string; data?: Record<string, string> } | null;
	graphData: GraphData;
	graphOverride: GraphData | null;
	loadingGraph: boolean;
	sparqlOpen: boolean;
	sparqlQuery: string;
	sparqlResults: SparqlResults | null;
	sparqlError: string | null;
	sparqlRunning: boolean;
	savedQueries: { name: string; sparql: string }[];
	switchView: (mode: ViewMode) => Promise<void>;
	runSparql: (query: string) => Promise<void>;
	saveQuery: () => void;
}

export const [getGraphContext, setGraphContext] = createContext<GraphContext>();

export function createGraphContext(getServerGraphData: () => GraphData): GraphContext {
	let viewMode: ViewMode = $state('threads');
	let selectedNode: { id: string; data?: Record<string, string> } | null = $state(null);
	let graphOverride: GraphData | null = $state(null);
	let loadingGraph = $state(false);
	let sparqlOpen = $state(false);
	let sparqlQuery = $state('');
	let sparqlResults: SparqlResults | null = $state(null);
	let sparqlError: string | null = $state(null);
	let sparqlRunning = $state(false);
	let savedQueries: { name: string; sparql: string }[] = $state([]);

	// Load saved queries from localStorage
	if (typeof window !== 'undefined') {
		const stored = localStorage.getItem('scenius-saved-queries');
		if (stored) savedQueries = JSON.parse(stored);
	}

	const ctx: GraphContext = {
		get viewMode() {
			return viewMode;
		},
		set viewMode(v) {
			viewMode = v;
		},
		get selectedNode() {
			return selectedNode;
		},
		set selectedNode(v) {
			selectedNode = v;
		},
		get graphData() {
			return graphOverride ?? getServerGraphData();
		},
		get graphOverride() {
			return graphOverride;
		},
		set graphOverride(v) {
			graphOverride = v;
		},
		get loadingGraph() {
			return loadingGraph;
		},
		set loadingGraph(v) {
			loadingGraph = v;
		},
		get sparqlOpen() {
			return sparqlOpen;
		},
		set sparqlOpen(v) {
			sparqlOpen = v;
		},
		get sparqlQuery() {
			return sparqlQuery;
		},
		set sparqlQuery(v) {
			sparqlQuery = v;
		},
		get sparqlResults() {
			return sparqlResults;
		},
		set sparqlResults(v) {
			sparqlResults = v;
		},
		get sparqlError() {
			return sparqlError;
		},
		set sparqlError(v) {
			sparqlError = v;
		},
		get sparqlRunning() {
			return sparqlRunning;
		},
		set sparqlRunning(v) {
			sparqlRunning = v;
		},
		get savedQueries() {
			return savedQueries;
		},
		set savedQueries(v) {
			savedQueries = v;
		},

		async switchView(mode: ViewMode) {
			viewMode = mode;
			loadingGraph = true;
			try {
				const params = new URLSearchParams({ view: mode });
				const res = await fetch(`/api/graph?${params}`);
				graphOverride = await res.json();
			} catch (e) {
				console.error('Failed to load graph:', e);
			} finally {
				loadingGraph = false;
			}
		},

		async runSparql(query: string) {
			sparqlRunning = true;
			sparqlError = null;
			sparqlResults = null;
			try {
				const res = await fetch('/api/sparql', {
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ query })
				});
				if (!res.ok) {
					sparqlError = await res.text();
					return;
				}
				sparqlResults = await res.json();
			} catch (e) {
				sparqlError = String(e);
			} finally {
				sparqlRunning = false;
			}
		},

		saveQuery() {
			if (!sparqlQuery.trim()) return;
			const name = prompt('Query name:');
			if (!name) return;
			savedQueries = [...savedQueries, { name, sparql: sparqlQuery }];
			localStorage.setItem('scenius-saved-queries', JSON.stringify(savedQueries));
		}
	};

	return ctx;
}

export function formatDate(iso: string): string {
	return new Date(iso).toLocaleDateString('en-US', {
		month: 'short',
		day: 'numeric',
		year: 'numeric',
		hour: 'numeric',
		minute: '2-digit'
	});
}

export function truncate(text: string | null, len = 200): string {
	if (!text) return '';
	return text.length > len ? text.slice(0, len) + '...' : text;
}
