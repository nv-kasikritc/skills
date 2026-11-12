<!-- SPDX-License-Identifier: Apache-2.0 AND CC-BY-4.0 -->

# sample-plugin

A placeholder-only [Agent Plugins 1.0.0](https://agent-plugins.org/specification)
package. It contains exactly **3 sample skills, 2 hooks, 4 MCP server entries,
and 1 subagent**. Each primitive is an example to replace with real content.

| Primitive | Placeholders | Location |
|---|---|---|
| Skills | `sample-skill-1`, `sample-skill-2`, `sample-skill-3` | `skills/<name>/SKILL.md` |
| Hooks | `sample-hook-1`, `sample-hook-2` | `com.example.client/hooks/hooks.json` |
| MCP servers | `sample-mcp-1` through `sample-mcp-4` | `mcp.json` |
| Subagent | `sample-subagent` | `com.example.client/agents/sample-subagent.md` |

## Package layout

```text
sample-plugin/
├── plugin.json
├── mcp.json
├── skills/
│   ├── sample-skill-1/SKILL.md
│   ├── sample-skill-2/SKILL.md
│   └── sample-skill-3/SKILL.md
├── com.example.client/
│   ├── hooks/hooks.json
│   └── agents/sample-subagent.md
├── .claude-plugin/plugin.json
├── .codex-plugin/plugin.json
├── .cursor-plugin/plugin.json
├── LICENSE-APACHE
├── LICENSE-CC-BY-4.0
└── README.md
```

## Standard format and client extensions

The root [`plugin.json`](plugin.json) targets the canonical Agent Plugins
1.0.0 schema. Skills are discovered from `skills/`, and the four server
configurations are declared in root [`mcp.json`](mcp.json), using the matching
1.0.0 MCP schema.

Agent Plugins 1.0.0 standardizes skills and MCP server configuration. Hooks and
subagents use the standard's
[client extension mechanism](https://agent-plugins.org/plugin-authors/client-extensions).
The illustrative `com.example.client` namespace holds their metadata and files.
Its `hooks`, `subagents`, `placeholder`, and `enabled` fields are example
client-owned data, not fields standardized by Agent Plugins. Replace this
namespace and map its contents to the selected client's actual extension
format before implementing behavior. Clients that do not implement this
example namespace ignore it.

The generated Claude, Codex, and Cursor manifests provide the repository's
usual skill metadata. They do not wire these example hooks, subagent, or MCP
entries into those clients' native formats; the portable MCP configuration
remains in `mcp.json`.

## Placeholder behavior

- Each skill replies that it is a placeholder and stops.
- Both hook records have `enabled: false` and contain placeholder commands.
- All four MCP entries use `stdio` with deliberately unimplemented executable
  names such as `sample-plugin-mcp-1-placeholder`. They provide no MCP tools
  and will fail to start until replaced with real server commands. The portable
  1.0.0 MCP schema has no `enabled` field, so no unsupported switch is added.
- The subagent prompt replies that it is a placeholder and stops. Its tool
  list is empty, and the example client extension is disabled.

The primitive definitions contain no service URLs, credentials, installation
steps, executable scripts, or NVIDIA catalog lookup behavior. Their placeholders
do not install anything, modify files, call services, or delegate tasks.

## Build and edit

The source definition is `plugins.d/sample-plugin.yml`. Skill source templates
live in `plugins.d/sample-plugin/skills/`, outside the production NVIDIA skills
catalog. Edit those templates and rebuild from the repository root:

```sh
python3 -m venv /tmp/sample-plugin-venv
/tmp/sample-plugin-venv/bin/python -m pip install pyyaml
/tmp/sample-plugin-venv/bin/python .github/scripts/build-plugins.py
```

The builder regenerates `plugin.json`, the three compatibility manifests, and
the packaged `skills/` directory. Extension metadata from the YAML is preserved
in the portable manifest. The root `mcp.json`, `com.example.client/` contents,
README, and license files are hand-maintained in this package and preserved
by the builder. The sample is excluded from all three marketplace listings.

After committing generated output, check the repository's build and version
policies:

```sh
/tmp/sample-plugin-venv/bin/python .github/scripts/build-plugins.py --check
/tmp/sample-plugin-venv/bin/python .github/scripts/version-plugins.py --check --base origin/main
```

## Validate

From the repository root, install author-time validators and download the two
published schemas:

```sh
/tmp/sample-plugin-venv/bin/python -m pip install jsonschema 'skills-ref==0.1.1'
curl --fail --location https://agent-plugins.org/schemas/1.0.0/plugin.schema.json \
  --output /tmp/sample-plugin.schema.json
curl --fail --location https://agent-plugins.org/schemas/1.0.0/mcp.schema.json \
  --output /tmp/sample-mcp.schema.json
/tmp/sample-plugin-venv/bin/python - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator

root = Path("plugins/sample-plugin")
for filename, schema_path in (
    ("plugin.json", "/tmp/sample-plugin.schema.json"),
    ("mcp.json", "/tmp/sample-mcp.schema.json"),
):
    schema = json.loads(Path(schema_path).read_text())
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(json.loads((root / filename).read_text()))
    print(f"Valid: {filename}")
PY
for skill in plugins/sample-plugin/skills/*; do
  /tmp/sample-plugin-venv/bin/agentskills validate "$skill"
done
```

These checks validate the portable manifest, MCP configuration, and skill
format. Hooks and the subagent are illustrative extension placeholders with
no claim of runtime compatibility with a specific client.

## License

`Apache-2.0 AND CC-BY-4.0`. Full license texts are bundled as
[`LICENSE-APACHE`](LICENSE-APACHE) and [`LICENSE-CC-BY-4.0`](LICENSE-CC-BY-4.0).
