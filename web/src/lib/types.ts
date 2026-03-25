// Types matching the SIOC/RDF schema for the knowledge graph

export interface Post {
	id: string;
	content: string | null;
	created: string;
	modified: string | null;
	creatorId: string | null;
	creatorName: string | null;
	containerId: string | null;
	containerName: string | null;
	replyOf: string | null;
}

export interface LinkedDoc {
	id: string;
	title: string | null;
	description: string | null;
	siteName: string | null;
	sharedBy: string | null;
	sharedAt: string | null;
}

export interface GraphNode {
	id: string;
	label: string;
	type: 'post' | 'user' | 'link';
	data?: Record<string, string>;
}

export interface GraphEdge {
	source: string;
	target: string;
	type: string;
}

export interface GraphData {
	nodes: GraphNode[];
	edges: GraphEdge[];
}

export interface SparqlBinding {
	type: 'uri' | 'literal' | 'bnode';
	value: string;
	datatype?: string;
	'xml:lang'?: string;
}

export interface SparqlResults {
	head: { vars: string[] };
	results: { bindings: Record<string, SparqlBinding>[] };
}
