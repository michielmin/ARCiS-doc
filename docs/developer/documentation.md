# Writing documentation

This site is built with [MkDocs](https://www.mkdocs.org/) and the
[Material theme](https://squidfunk.github.io/mkdocs-material/). The sources are Markdown
files in `docs/`, the configuration is `mkdocs.yml` in the repository root.

## Building locally

```bash
pip install -r docs/requirements.txt
mkdocs serve        # live preview at http://127.0.0.1:8000
mkdocs build        # static site in site/
```

!!! note "MkDocs version"
    `docs/requirements.txt` pins MkDocs below 2.0: MkDocs 2.0 is incompatible with the
    Material theme.

## The keyword reference is generated

The [Keyword reference](../reference/keywords.md) and the
[Molecule list](../reference/molecules.md) are generated from the source code, so they
always show the keywords, aliases and defaults of the current code:

```bash
python docs/scripts/extract_keywords.py   # parse Init.f and Modules.f → docs/reference/keywords.json
python docs/scripts/gen_reference.py      # merge with descriptions → keywords.md, molecules.md
```

`extract_keywords.py` reads the `select case` blocks in `ReadAndSetKey`, `ReadCloud`,
`ReadObsSpec`, `ReadRetrieval`, … and the defaults in `SetDefaults`. The descriptions
are kept by hand in `docs/reference/keyword_descriptions.yml`:

```yaml
sections:
  - title: Planet and star
    keys:
      rp: {desc: "Planet radius at pressure `Pp`.", unit: "R<sub>Jup</sub>"}
      mykey: {desc: "What it does.", review: true}
```

* Use the **primary** (first) name of the keyword from the `case(...)` statement, in
  lower case.
* `review: true` marks a description that still needs checking (shown as ✎).
* Keywords in the code without a description end up in a *Not yet described* section;
  descriptions of keywords that were removed from the code produce a warning.
* Keywords whose value is never used in the code are automatically marked
  <span class="unused">no effect</span>.

**After adding or changing a keyword in `Init.f`, rerun both scripts** and commit the
regenerated files.

## Publishing

The simplest option is GitHub Pages:

```bash
mkdocs gh-deploy
```

This builds the site and pushes it to the `gh-pages` branch. To do this automatically
on every push, add a GitHub Actions workflow, e.g. `.github/workflows/docs.yml`:

```yaml
name: docs
on:
  push:
    branches: [master]
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - run: pip install -r docs/requirements.txt
      - run: python docs/scripts/extract_keywords.py
      - run: python docs/scripts/gen_reference.py
      - run: mkdocs gh-deploy --force
```

## Conventions

* Keywords and file names in backticks: `` `cloud1:tau` ``.
* Equations with `\( … \)` (inline) and `\[ … \]` (display); they are rendered with
  MathJax.
* Open questions for the developers in a `!!! question "To review"` box.
