import { getRecentPosts, getRecentLinks, getThreadGraph, getForums, getTopics } from '$lib/server/graph-service.js';
import { loadQueryLibrary } from '$lib/server/query-library.js';
import type { PageServerLoad } from './$types.js';

export const load: PageServerLoad = async () => {
	const [posts, links, graphData, forums, topics, queryLibrary] = await Promise.all([
		getRecentPosts(30),
		getRecentLinks(30),
		getThreadGraph({ limit: 300 }),
		getForums(),
		getTopics(),
		loadQueryLibrary()
	]);

	return { posts, links, graphData, forums, topics, queryLibrary };
};
