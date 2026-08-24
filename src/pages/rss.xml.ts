import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { listPapers, formatAuthors } from '../lib/papers';
import { taxonomy } from '../lib/taxonomy';

/**
 * A feed of papers, newest addition first.
 *
 * There was no way to hear about a new paper short of watching the repository.
 * The comparable collections are followed through releases or a newsletter;
 * this is the cheap equivalent, and it costs one file because the data is
 * already structured.
 *
 * Ordered by `added` (when it entered the collection) and not by `year`: a
 * subscriber wants to know what is new here, not what is new in the field.
 */
export async function GET(context: APIContext) {
  const papers = await listPapers();

  const sorted = papers.sort(
    (a, b) => new Date(b.data.added).getTime() - new Date(a.data.added).getTime()
  );

  return rss({
    title: 'Awesome Agentic Systems',
    description:
      'Papers on agentic AI systems, classified by contribution. New additions to the collection.',
    site: context.site!,
    items: sorted.map((paper) => {
      const area = taxonomy.areas[paper.data.area];
      return {
        title: paper.data.title,
        // The link points at our record rather than the paper: that page has
        // the summary, the classification and the reading path around it.
        link: `${import.meta.env.BASE_URL.replace(/\/$/, '')}/papers/${paper.data.id}`,
        pubDate: new Date(paper.data.added),
        description:
          paper.data.tldr ||
          `${formatAuthors(paper.data.authors)} (${paper.data.year}). Filed under ${area.label}.`,
        categories: [paper.data.area, ...paper.data.topics],
      };
    }),
    customData: '<language>en</language>',
  });
}
