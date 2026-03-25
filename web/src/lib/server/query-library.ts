import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';

export interface PrebuiltQuery {
	name: string;
	description: string;
	sparql: string;
}

const QUERIES_DIR = join(import.meta.dirname, 'queries');

/**
 * Load all pre-built .sparql files from the queries directory.
 * Files should start with `## Title` and `## Description` comment lines.
 */
export async function loadQueryLibrary(): Promise<PrebuiltQuery[]> {
	const files = await readdir(QUERIES_DIR);
	const sparqlFiles = files.filter((f) => f.endsWith('.sparql')).sort();

	const queries: PrebuiltQuery[] = [];

	for (const file of sparqlFiles) {
		const content = await readFile(join(QUERIES_DIR, file), 'utf-8');
		const lines = content.split('\n');

		// Parse ## comment headers for name and description
		const name = lines[0]?.startsWith('##') ? lines[0].replace('##', '').trim() : file.replace('.sparql', '');
		const description = lines[1]?.startsWith('##') ? lines[1].replace('##', '').trim() : '';

		// Strip comment headers to get clean SPARQL
		const sparql = lines
			.filter((l) => !l.startsWith('##'))
			.join('\n')
			.trim();

		queries.push({ name, description, sparql });
	}

	return queries;
}
