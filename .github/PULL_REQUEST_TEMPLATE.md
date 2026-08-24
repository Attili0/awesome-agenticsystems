<!--
Auto-generated pull requests from the "Add a Paper" issue form already carry
their own checklist — you can delete this one. This template is for pull
requests opened by hand.
-->

## What this changes

<!-- One or two sentences. If it closes an issue, write "Closes #123". -->

## Checklist

Tick what applies. An unticked box is fine — it tells the reviewer where to
look, it does not block the merge.

**If you added or edited a paper:**

- [ ] `area` describes the paper's **contribution**, not the topic it talks
      about. (Multiple agents alone means `scale: [multi-agent]`, not
      `area: coordination`.)
- [ ] `scale` reflects the scale of the system studied.
- [ ] It is not already in the collection under a different title.
- [ ] `id` matches the filename.
- [ ] If `status: read`, it has `tldr`, `topics` and `about`. If not, it is
      `triaged` — which is perfectly fine.
- [ ] `relates_to` is declared in **one direction only** (newer paper points at
      the older one). The reverse link is computed automatically.

**If you changed `src/data/taxonomy.yml`:**

- [ ] I ran `npm run docs` and committed the regenerated blocks. (CI fails
      otherwise — the guides and the issue form are generated from that file.)
- [ ] A new topic is something you would filter by *today*. A new area has at
      least one paper to live in it, and an argument from the literature in
      [TAXONOMY.md](../TAXONOMY.md#bibliographic-basis).

**Everyone:**

- [ ] `npm run build` passes locally. (CI runs it too, so this is only to save
      yourself a round trip.)
- [ ] If you changed anything under `scripts/`, `npm test` passes and any new
      behaviour has a test. That directory runs unsupervised — its failures
      reach contributors as issue comments.

<!--
New to the project? Say so — reviewers will walk you through anything above
rather than just asking for changes.
-->
