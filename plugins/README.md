# `plugins/` — generated plugin bundles

Each subdirectory here is a self-contained plugin built from a source
definition in [`plugins.d/`](../plugins.d/) by
[`.github/scripts/build-plugins.py`](../.github/scripts/build-plugins.py).

A plugin folder typically contains:

- `plugin.json` — portable [Agent Plugins 1.0.0](https://agent-plugins.org/) manifest
- `.claude-plugin/plugin.json` — Claude plugin manifest
- `.codex-plugin/plugin.json` — Codex plugin manifest
- `.cursor-plugin/plugin.json` — Cursor plugin manifest
- `skills/` — the bundled skills (real files or symlinks back into the
  top-level [`skills/`](../skills/) catalog, depending on `skill_files:`
  in the source yaml)
- `assets/` — optional logo and other hand-maintained assets

## Don't edit these files directly

With the exception of curated plugins (see below), everything under
`plugins/<name>/` is **regenerated on every build**. To change a
plugin's metadata or skill list, edit `plugins.d/<name>.yml` and re-run:

```sh
.github/scripts/build-plugins.sh
```

See [`plugins.d/README.md`](../plugins.d/README.md) for the full
authoring workflow.

## Sample plugin

[`sample-plugin/`](./sample-plugin/) is an Agent Plugins 1.0.0 scaffold with
three placeholder skills, two hooks, four MCP server entries, and one subagent.
Hooks and the subagent live in an illustrative client extension namespace.
The sample includes build and validation instructions and stays out of the
marketplace listings. Its source definition is
[`plugins.d/sample-plugin.yml`](../plugins.d/sample-plugin.yml).

## Curated plugins

A plugin folder that contains its own `.skills-manifest.yml` (instead of
having a matching `plugins.d/<name>.yml`) is **curated** — the build
script only refreshes its `skills/` links and leaves the manifests,
assets, and marketplace entries hand-edited. No plugins currently use
this mode: [`nvidia-skills/`](./nvidia-skills/) is catalog-driven, built
from [`plugins.d/nvidia-skills.yml`](../plugins.d/nvidia-skills.yml), and
ships to the official Anthropic (Claude), OpenAI (Codex), and Cursor
plugin marketplaces.
