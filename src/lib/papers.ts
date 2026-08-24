import fs from 'node:fs';
import path from 'node:path';
import { getCollection, type CollectionEntry } from 'astro:content';

export type Paper = CollectionEntry<'papers'>;

/** A classified paper: `area` is guaranteed by the schema. */
export type ClassifiedPaper = Paper & {
  data: Paper['data'] & { area: string };
};

const PAPERS_DIR = path.join(process.cwd(), 'src/content/papers');

const isClassified = (p: Paper): p is ClassifiedPaper => p.data.status !== 'captured';

/**
 * The `id` field of a record has to match its filename.
 *
 * Nothing guaranteed that: `relates_to`, `evaluated_on` and the /papers/[id]
 * routes all use `data.id`, while the file itself is found by its name. When
 * they diverge the paper is published at one URL and referenced from another,
 * and the build says nothing. We compare against the directory rather than
 * against the id the loader assigns, so that a .yml that failed to load shows
 * up here too.
 */
function assertIdsMatchFilenames(papers: Paper[]): void {
  const onDisk = new Set(
    fs.readdirSync(PAPERS_DIR)
      .filter((f) => f.endsWith('.yml'))
      .map((f) => f.replace(/\.yml$/, ''))
  );

  const mismatched = papers
    .filter((p) => !onDisk.has(p.data.id))
    .map((p) => `id: "${p.data.id}" matches no file`);
  if (mismatched.length) {
    throw new Error(
      `src/content/papers: the id field must equal the filename. ` +
        mismatched.join('; ')
    );
  }
}

/**
 * The papers shown on the site.
 *
 * A `captured` paper is just a saved link: it has no area yet, so it cannot
 * appear in the index or have a page of its own. It lives in git until
 * somebody triages it. See CONTRIBUTING.md.
 */
export async function listPapers(): Promise<ClassifiedPaper[]> {
  const all = await getCollection('papers');
  assertIdsMatchFilenames(all);
  return all.filter(isClassified);
}

/**
 * Authors for the listing cards: the first `max` and "et al.".
 *
 * Some papers have 20+ authors (AgentBench) and took up three lines, pushing
 * the rest of the card down. The paper page shows all of them.
 */
export function formatAuthors(authors: string[], max = 3): string {
  if (authors.length <= max) return authors.join(', ');
  return `${authors.slice(0, max).join(', ')} et al.`;
}

/** How many papers are waiting for triage. The backlog should not be invisible. */
export async function countCaptured(): Promise<number> {
  return (await getCollection('papers')).filter((p) => p.data.status === 'captured').length;
}
