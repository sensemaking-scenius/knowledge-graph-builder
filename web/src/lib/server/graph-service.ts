import { query, val } from './sparql.js';
import type { Post, LinkedDoc, GraphData, SparqlResults } from '$lib/types.js';

/**
 * Get recent posts with creator and container info.
 */
export async function getRecentPosts(limit = 50, offset = 0): Promise<Post[]> {
	const results = await query(`
		SELECT ?post ?content ?created ?modified ?creator ?creatorName ?container ?containerName
		WHERE {
			?post a sioc:Post ;
				dcterms:created ?created .
			OPTIONAL { ?post sioc:content ?content }
			OPTIONAL { ?post dcterms:modified ?modified }
			OPTIONAL {
				?post sioc:has_creator ?creator .
				OPTIONAL { ?creator sioc:name ?creatorName }
			}
			OPTIONAL {
				?post sioc:has_container ?container .
				OPTIONAL { ?container foaf:name ?containerName }
			}
		}
		ORDER BY DESC(?created)
		LIMIT ${limit}
		OFFSET ${offset}
	`);

	return results.results.bindings.map((b) => ({
		id: val(b, 'post')!,
		content: val(b, 'content'),
		created: val(b, 'created')!,
		modified: val(b, 'modified'),
		creatorId: val(b, 'creator'),
		creatorName: val(b, 'creatorName'),
		containerId: val(b, 'container'),
		containerName: val(b, 'containerName'),
		replyOf: null
	}));
}

/**
 * Get recently shared links with metadata and who shared them.
 */
export async function getRecentLinks(limit = 50, offset = 0): Promise<LinkedDoc[]> {
	const results = await query(`
		SELECT ?doc ?title ?description ?siteName ?creator ?created
		WHERE {
			?post a sioc:Post ;
				sioc:links_to ?doc ;
				dcterms:created ?created .
			OPTIONAL { ?doc dc:title ?title }
			OPTIONAL { ?doc dcterms:description ?description }
			OPTIONAL { ?doc tg:site_name ?siteName }
			OPTIONAL {
				?post sioc:has_creator ?creatorUri .
				?creatorUri sioc:name ?creator
			}
		}
		ORDER BY DESC(?created)
		LIMIT ${limit}
		OFFSET ${offset}
	`);

	return results.results.bindings.map((b) => ({
		id: val(b, 'doc')!,
		title: val(b, 'title'),
		description: val(b, 'description'),
		siteName: val(b, 'siteName'),
		sharedBy: val(b, 'creator'),
		sharedAt: val(b, 'created')!
	}));
}

/**
 * Get conversation thread graph: posts as nodes, reply_of as edges.
 * Optionally filter by forum/topic.
 */
export async function getThreadGraph(options?: {
	forumId?: string;
	limit?: number;
}): Promise<GraphData> {
	const limit = options?.limit ?? 500;
	const forumFilter = options?.forumId
		? `?post sioc:has_container <${options.forumId}> .`
		: '';

	const results = await query(`
		SELECT ?post ?content ?created ?creator ?creatorName ?replyOf
		WHERE {
			?post a sioc:Post ;
				dcterms:created ?created .
			${forumFilter}
			OPTIONAL { ?post sioc:content ?content }
			OPTIONAL {
				?post sioc:has_creator ?creator .
				OPTIONAL { ?creator sioc:name ?creatorName }
			}
			OPTIONAL { ?post sioc:reply_of ?replyOf }
		}
		ORDER BY DESC(?created)
		LIMIT ${limit}
	`);

	const nodeSet = new Set<string>();
	const nodes: GraphData['nodes'] = [];
	const edges: GraphData['edges'] = [];

	for (const b of results.results.bindings) {
		const postId = val(b, 'post')!;
		const replyOf = val(b, 'replyOf');
		const content = val(b, 'content') ?? '';
		const label = content.length > 80 ? content.slice(0, 80) + '...' : content;

		if (!nodeSet.has(postId)) {
			nodeSet.add(postId);
			nodes.push({
				id: postId,
				label: label || postId.split('/').pop()!,
				type: 'post',
				data: {
					content: val(b, 'content') ?? '',
					created: val(b, 'created') ?? '',
					creator: val(b, 'creatorName') ?? val(b, 'creator') ?? ''
				}
			});
		}

		if (replyOf) {
			// Ensure the target node exists (it may be outside our result window)
			if (!nodeSet.has(replyOf)) {
				nodeSet.add(replyOf);
				nodes.push({
					id: replyOf,
					label: replyOf.split('/').pop()!,
					type: 'post'
				});
			}
			edges.push({ source: postId, target: replyOf, type: 'reply_of' });
		}
	}

	return { nodes, edges };
}

/**
 * Get link sharing graph: users as nodes, shared URLs as edges between users.
 */
export async function getLinkGraph(limit = 300): Promise<GraphData> {
	const results = await query(`
		SELECT ?user ?userName ?doc ?title
		WHERE {
			?post a sioc:Post ;
				sioc:has_creator ?user ;
				sioc:links_to ?doc .
			?user sioc:name ?userName .
			OPTIONAL { ?doc dc:title ?title }
		}
		LIMIT ${limit}
	`);

	const nodeSet = new Set<string>();
	const nodes: GraphData['nodes'] = [];
	const edges: GraphData['edges'] = [];

	// Track which users shared which links
	const linkUsers = new Map<string, Set<string>>();

	for (const b of results.results.bindings) {
		const userId = val(b, 'user')!;
		const userName = val(b, 'userName') ?? userId.split('/').pop()!;
		const docId = val(b, 'doc')!;
		const docTitle = val(b, 'title') ?? docId;

		if (!nodeSet.has(userId)) {
			nodeSet.add(userId);
			nodes.push({ id: userId, label: userName, type: 'user' });
		}
		if (!nodeSet.has(docId)) {
			nodeSet.add(docId);
			nodes.push({ id: docId, label: docTitle, type: 'link' });
		}

		if (!linkUsers.has(docId)) linkUsers.set(docId, new Set());
		linkUsers.get(docId)!.add(userId);

		edges.push({ source: userId, target: docId, type: 'links_to' });
	}

	return { nodes, edges };
}

/**
 * Get user-post network: users and their posts as nodes.
 */
export async function getUserPostGraph(limit = 500): Promise<GraphData> {
	const results = await query(`
		SELECT ?user ?userName ?post ?content ?created
		WHERE {
			?post a sioc:Post ;
				sioc:has_creator ?user ;
				dcterms:created ?created .
			?user sioc:name ?userName .
			OPTIONAL { ?post sioc:content ?content }
		}
		ORDER BY DESC(?created)
		LIMIT ${limit}
	`);

	const nodeSet = new Set<string>();
	const nodes: GraphData['nodes'] = [];
	const edges: GraphData['edges'] = [];

	for (const b of results.results.bindings) {
		const userId = val(b, 'user')!;
		const userName = val(b, 'userName') ?? userId.split('/').pop()!;
		const postId = val(b, 'post')!;
		const content = val(b, 'content') ?? '';
		const label = content.length > 60 ? content.slice(0, 60) + '...' : content;

		if (!nodeSet.has(userId)) {
			nodeSet.add(userId);
			nodes.push({ id: userId, label: userName, type: 'user' });
		}
		if (!nodeSet.has(postId)) {
			nodeSet.add(postId);
			nodes.push({
				id: postId,
				label: label || postId.split('/').pop()!,
				type: 'post',
				data: {
					content,
					created: val(b, 'created') ?? ''
				}
			});
		}

		edges.push({ source: userId, target: postId, type: 'has_creator' });
	}

	return { nodes, edges };
}

/**
 * Execute a raw SPARQL query (for the playground).
 */
export async function runQuery(sparql: string): Promise<SparqlResults> {
	return query(sparql);
}

/**
 * Get all forums for filter dropdowns.
 */
export async function getForums(): Promise<{ id: string; name: string }[]> {
	const results = await query(`
		SELECT ?forum ?name
		WHERE {
			?forum a sioc:Forum .
			OPTIONAL { ?forum foaf:name ?name }
		}
		ORDER BY ?name
	`);

	return results.results.bindings.map((b) => ({
		id: val(b, 'forum')!,
		name: val(b, 'name') ?? val(b, 'forum')!.split('/').pop()!
	}));
}

/**
 * Get all concepts/topics for filter dropdowns.
 */
export async function getTopics(): Promise<{ id: string; label: string }[]> {
	const results = await query(`
		SELECT ?concept ?label
		WHERE {
			?concept a skos:Concept ;
				skos:prefLabel ?label .
		}
		ORDER BY ?label
	`);

	return results.results.bindings.map((b) => ({
		id: val(b, 'concept')!,
		label: val(b, 'label')!
	}));
}
