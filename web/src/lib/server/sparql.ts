import { OXIGRAPH_URL } from '$env/static/private';
import type { SparqlResults } from '$lib/types.js';

const ENDPOINT = `${OXIGRAPH_URL}/query`;

const PREFIXES = `
PREFIX sioc: <http://rdfs.org/sioc/ns#>
PREFIX sioc_types: <http://rdfs.org/sioc/types#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX tg: <https://example.org/telegram/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
`;

/**
 * Execute a raw SPARQL SELECT query against Oxigraph.
 * Automatically prepends standard prefixes unless the query already declares them.
 */
export async function query(sparql: string): Promise<SparqlResults> {
	const fullQuery = sparql.trimStart().startsWith('PREFIX') ? sparql : PREFIXES + sparql;

	const res = await fetch(ENDPOINT, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/sparql-query',
			Accept: 'application/sparql-results+json'
		},
		body: fullQuery
	});

	if (!res.ok) {
		const text = await res.text();
		throw new Error(`SPARQL query failed (${res.status}): ${text}`);
	}

	return res.json();
}

/** Helper to extract a plain string value from a binding, or null if missing. */
export function val(binding: Record<string, { value: string }>, key: string): string | null {
	return binding[key]?.value ?? null;
}
