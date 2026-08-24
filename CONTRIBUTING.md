# How to add a paper

This is a collection of **papers**. Software repositories are not included,
even when they have an associated paper: we document the paper, not the tool.

That rule is about what gets a record, not about what a paper may be *about*.
A paper describing a framework is perfectly welcome — that is what
`type: framework` is for. AutoGen and MetaGPT are both in the collection as
papers; their repositories are not. Benchmarks likewise count as papers, and
belong to the `evaluation` area like anything else.

New here? [Suggest a paper](#suggest-a-paper) is a one-minute job and needs no
setup. Everything below that is for people filling records in by hand.

## The model, in short

A paper is classified on two axes:

- `area` — exactly one. Answers *"what is the contribution?"*.
- `topics` and the facets (<!-- gen:facet-names -->`about`, `scale`, `infra`, `type`, `domain`<!-- /gen:facet-names -->) —
  as many as apply. They answer *"what is it about?"* and cross areas freely.

To contribute through an issue you only need three fields: `area`, `scale` and
`type`. The rest are optional and get filled in later, while reading the paper.

## Two paths

Which path you take depends on what you want to do:

| | Who | How | Resulting status |
|---|---|---|---|
| Suggest a paper | Anyone | Issue with 3 fields → reviewed PR | `triaged` — visible on the site |
| Add and read | Anyone willing to clone | Edit the `.yml` and open a pull request | `read` — includes `tldr` and `notes` |

### Suggest a paper

1. Go to **Issues** → **New Issue** → **Add a Paper**.
2. Paste the link to the paper. If it is an arXiv link, that is all the
   metadata we need — title, authors and year are fetched automatically. For
   any other source, paste the **BibTeX** too (most publisher pages have a
   "Cite" or "Export citation" button).
3. Pick **`area`** (see [below](#how-to-pick-the-area)), **`scale`** and
   **`type`**. Each option in the form carries a one-line description.
4. An automated process reads the metadata, generates the `.yml` file, checks
   that the site still builds and that the tests pass, and opens a **pull
   request** for a maintainer to review. Nothing is merged automatically.

You do not need to clone the repository or run anything locally.

If you are unsure about the classification, pick the closest option. The pull
request is reviewed before it is merged; a debatable area beats a paper nobody
suggested.

The submission is validated before any pull request is opened: if the year is
missing, the link is invalid, the paper is already in the collection (we
compare the arXiv id and the title, not just the filename), or a value is not
part of the taxonomy, the process stops. The site is then built with the new
record and the test suite is run; the pull request is only opened if both
succeed.

**If something fails, the reason is posted as a comment on your issue** and it
gets labelled `needs-fix` — you do not have to open CI logs. Fix the issue and
close/reopen it to retry.

### Add and read

The issue path reaches `triaged`: it has no `tldr`, `notes`, `topics` or
`about`, because those come from reading the paper. To add them, edit the
`.yml` file directly and open a pull request. You do not need to be a
maintainer to do this — it just needs a clone, since the issue form
deliberately does not ask for fields you can only fill in after reading.

See the [local workflow](./TAXONOMY.md#local-workflow) and the
[fields of a record](./TAXONOMY.md#fields-of-a-record).

## How to pick the area

The areas are grouped into layers. The criterion for picking one is not the
paper's general topic but its **main contribution**.

<!-- gen:areas-table -->
| Layer | Areas |
|---|---|
| Overview | `foundations` |
| What an agent can do | `reasoning-planning`, `memory`, `tools-context`, `learning-evolution` |
| How it is built | `architectures`, `coordination`, `interoperability`, `engineering` |
| How it is judged and controlled | `evaluation`, `safety` |
<!-- /gen:areas-table -->

Each area with the rule for picking it:

<!-- gen:areas-detail -->
| Area | Layer | Pick it when |
|---|---|---|
| `foundations` | Overview | A general view of the field: surveys, taxonomies, position papers. |
| `reasoning-planning` | What an agent can do | What happens between the input and the action: reasoning, planning, self-critique. |
| `memory` | What an agent can do | What the agent remembers and how it retrieves it. Vocabulary taken from CoALA. |
| `tools-context` | What an agent can do | How the agent acts on the world and where it gets context from. |
| `learning-evolution` | What an agent can do | Changes that persist BETWEEN tasks: skills, experience, tuning. If the learning is discarded when the task ends, it is self-correction and belongs in reasoning-planning. |
| `architectures` | How it is built | The complete loop of an agent. If the contribution is ONE component (memory, planning, tools), it belongs to that component instead. |
| `coordination` | How it is built | The mechanisms by which several agents divide work and communicate. Having several agents does NOT put a paper here: that is what scale: multi-agent says. This area is for papers whose contribution IS the coordination mechanism. |
| `interoperability` | How it is built | Standards that let agents and tools discover each other and talk. |
| `engineering` | How it is built | The runtime substrate around the model, and how it is operated. A harness does not make the model smarter: it makes its output reliable. |
| `evaluation` | How it is judged and controlled | How an agent or a multi-agent system is measured. |
| `safety` | How it is judged and controlled | Risk, security, trust and control. |
<!-- /gen:areas-detail -->

Every area also has its description on
[`/areas`](https://juliodosreis.github.io/awesome-agenticsystems/areas).

Two rules that resolve most ambiguous cases:

- **Scale does not define the area.** A multi-agent system does not
  automatically belong to `coordination`; that is what `scale: [multi-agent]`
  says. `coordination` is for work whose central contribution is the
  coordination mechanism itself. A paper on shared memory, for example, goes
  to `memory` with `scale: [multi-agent]`.
- **`architectures` means the whole loop.** If the contribution is one
  component (memory, planning, tool use), it belongs to that component.

## A paper is never blocked

You do not have to read a paper in full to record it. The schema implements
three states:

<!-- gen:status-table -->
| status | Requires | Effect |
|---|---|---|
| `captured` | metadata only | Kept in git, not visible on the site. |
| `triaged` | `area`, `scale`, `type` | Visible in the index. |
| `read` | `tldr`, `topics`, `about` | Works as a summary on the site. |
<!-- /gen:status-table -->

An issue lands the paper in `triaged`, which is enough for it to appear on the
site, and it can stay there indefinitely. That is deliberate: the cost of
suggesting a paper should be close to zero.

Enforcement through the schema means strict validation: declaring
`status: read` without a `tldr` breaks the build, with a message saying that
this state requires that field and suggesting you drop back to `triaged`.

## Where to ask

- **Something is misclassified?** Open an issue with the *Fix a
  classification* template. Disagreeing about an area is useful signal, not a
  complaint.
- **A term is missing from the vocabulary?** Use the *Propose a taxonomy
  change* template. Adding topics is cheap and expected; see the criteria in
  [TAXONOMY.md](./TAXONOMY.md#changing-the-taxonomy).
- **Anything else?** Open a regular issue. Questions from people new to the
  field are welcome — if a guide left you guessing, that is a bug in the guide.

Participation is covered by the [Code of Conduct](./CODE_OF_CONDUCT.md).

## Further reading

- **[TAXONOMY.md](./TAXONOMY.md)** — The rest of the fields, how topics and
  facets work, the criteria for changing the taxonomy, and the bibliography
  behind it. Read this before filling records in by hand or proposing changes
  to the vocabulary.
- **[`/taxonomy`](https://juliodosreis.github.io/awesome-agenticsystems/taxonomy)** — The complete vocabulary. Terms nobody
  uses yet are shown in grey and are still valid.
