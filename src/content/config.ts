import { z, defineCollection } from 'astro:content';

const paperCollection = defineCollection({
  type: 'data',
  schema: z.object({
    id: z.string(),
    title: z.string(),
    authors: z.array(z.string()),
    year: z.number(),
    venue: z.string().optional(),
    arxiv: z.string().optional(),
    links: z.object({
      paper: z.string().url(),
      code: z.string().url().optional()
    }),
    area: z.string(),
    topics: z.array(z.string()),
    capability: z.array(z.string()),
    level: z.array(z.string()),
    type: z.array(z.string()),
    infra: z.array(z.string()),
    domain: z.array(z.string()),
    status: z.enum(['captured', 'triaged', 'read']),
    tldr: z.string().optional(),
    notes: z.string().optional(),
    relates_to: z.array(z.string()).optional(),
    evaluated_on: z.array(z.string()).optional(),
    added: z.any() // string or Date
  })
});

export const collections = {
  'papers': paperCollection
};
