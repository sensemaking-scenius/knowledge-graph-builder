import { json } from '@sveltejs/kit';
import { getThreadGraph, getLinkGraph, getUserPostGraph } from '$lib/server/graph-service.js';
import type { RequestHandler } from './$types.js';

export const GET: RequestHandler = async ({ url }) => {
	const view = url.searchParams.get('view') ?? 'threads';
	const forum = url.searchParams.get('forum') ?? undefined;

	switch (view) {
		case 'links':
			return json(await getLinkGraph());
		case 'users':
			return json(await getUserPostGraph());
		case 'threads':
		default:
			return json(await getThreadGraph({ forumId: forum }));
	}
};
