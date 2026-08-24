import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import pagefind from 'astro-pagefind';

// https://astro.build/config
export default defineConfig({
  site: 'https://juliodosreis.github.io',
  base: '/awesome-agenticsystems',
  integrations: [
    sitemap(),
    // Pagefind indexes the built HTML after the build and serves a static
    // search bundle. It replaces the old per-page filter, which only searched
    // the home page: a query for an author or a topic from /areas found
    // nothing at all.
    pagefind(),
  ],
});
