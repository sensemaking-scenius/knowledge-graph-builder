import { json } from '@sveltejs/kit';
import { runQuery } from '$lib/server/graph-service.js';
import type { RequestHandler } from './$types.js';

export const POST: RequestHandler = async ({ request }) => {
	const { query } = await request.json();

	if (!query || typeof query !== 'string') {
		return new Response('Missing "query" field', { status: 400 });
	}

	try {
		const results = await runQuery(query);
		return json(results);
	} catch (e) {
		const msg = e instanceof Error ? e.message : String(e);
		return new Response(msg, { status: 500 });
	}
};
