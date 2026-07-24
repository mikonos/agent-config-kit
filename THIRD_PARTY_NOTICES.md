# Third-party notices

The `knowledge-vault` pack is adapted from
`mikonos/zettelkasten-agent-skills`, published under the MIT License. Its
original license is retained inside that pack. Minor changes make YAML
standards-compliant, resolve a bundled validation script from the Skill
directory, and remove trailing whitespace; the workflows are otherwise unchanged.

No bundled source PDFs, transcripts, binaries, virtual environments, nested
Git repositories, credentials, or runtime state are redistributed.

The `product-management` pack is derived from
[`phuryn/pm-skills`](https://github.com/phuryn/pm-skills) at commit
`18468a95b427e70e258b51389796367c6f684e7d`, published under the MIT License.
The original license is retained inside that pack. The
`intended-vs-implemented` Skill includes an additional public-claim and demo
audit workflow; the remaining 67 Skill files match that pinned upstream
commit.

The `product-writing` pack contains the `prd` Skill from
[`github/awesome-copilot`](https://github.com/github/awesome-copilot) at
commit `786bdcfc65b669faee10803db460a7218858ad21`, published under the MIT
License. The original license is retained inside that pack.

The `media` pack contains the runtime files of the `watch` Skill from
[`bradautomates/claude-video`](https://github.com/bradautomates/claude-video)
at commit `83da59fa78c3eee9e20f515fe75c438bb5166efd`, published under the MIT
License. Packaging-only files are omitted; the original license is retained
inside that pack.

The `perspectives` pack contains ten licensed snapshot Skills attributed to
[`alchaincyf/nuwa-skill`](https://github.com/alchaincyf/nuwa-skill). The
snapshot hashes are recorded in `catalog/snapshot_imports.json`, and the MIT
License found with the installed collection is retained inside the pack.
Variants containing machine-specific paths are not included.

The `writing` pack contains the `khazix-writer` Skill and its two references
from [`KKKKhazix/khazix-skills`](https://github.com/KKKKhazix/khazix-skills).
The snapshot hashes are recorded in `catalog/snapshot_imports.json`, and the
MIT License found with the installed collection is retained inside the pack.

The engineering, productivity, personal, experimental, and legacy workflow
packs contain 34 Skills from
[`mattpocock/skills`](https://github.com/mattpocock/skills) at commit
`ed37663cc5fbef691ddfecd080dff42f7e7e350d`, published under the MIT License.
Each imported directory matches its Git tree hash, and the original license is
retained inside every affected pack. The upstream category labels
`in-progress` and `deprecated` are preserved as separate packs so they are not
mistaken for default recommendations.

The `skill-authoring` pack contains Anthropic's `skill-creator` Skill from
[`anthropics/skills`](https://github.com/anthropics/skills) at commit
`1f630fdf9259cec4a14913127dfd7c3b69ef72eb`, published under the Apache
License 2.0. Its Skill-level `LICENSE.txt` is retained in the pack. The
separately licensed `xlsx` Skill is not redistributed.

The `presentations` pack contains the `presenton` Skill from
[`besoeasy/open-skills`](https://github.com/besoeasy/open-skills) at commit
`3bc011321c9054238d207936dbb577aa4b7e0e4d`, published under the MIT License.
The original license is retained inside the pack.

The `obsidian` pack contains five Skills from
[`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills) at
commit `a1dc48e68138490d522c04cbf5822214c6eb1202`, published under the MIT
License. Each imported directory matches its pinned Git tree, and the original
license is retained inside the pack.

The `marketing` pack contains twenty-four Skills derived from
[`coreyhaines31/marketingskills`](https://github.com/coreyhaines31/marketingskills),
published under the MIT License. Seven imported directories match commit
`c21a984a56da10fb6085e6334f6f60929220a4da`. Seventeen legacy-name local
snapshots preserve reviewed installed variants derived from earlier project
versions. Their product-context lookup was made runtime-neutral for Codex,
Cursor, and Claude Code. Exact source and packaged hashes are recorded in
`catalog/snapshot_imports.json` and `catalog/portable_patches.json`. The
original license is retained inside the pack.

The `web-extraction` pack contains the `news-extractor` Skill from
[`nanmicoder/newscrawler`](https://github.com/nanmicoder/newscrawler) at
commit `e04c52870e579b5432e8991cd7d342e4fbdd7063`, published under
GPL-3.0-only. The complete imported Skill source and upstream GPL license are
retained without modification; its Python dependencies are installed
separately by the recipient with `uv`.

The `design` pack contains Anthropic's `frontend-design` Skill from
[`anthropics/skills`](https://github.com/anthropics/skills) at commit
`1f630fdf9259cec4a14913127dfd7c3b69ef72eb`, published under Apache-2.0.
Its Skill-level license and exact Git tree are retained.

The `design-intelligence` pack contains the `ui-ux-pro-max` Skill from
[`nextlevelbuilder/ui-ux-pro-max-skill`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
at commit `1307d97a72e6c1cda572cb65471ae5ce82995218`, published under the MIT
License. Its code, references, and data come from the pinned upstream Git tree.
Three text-only portability edits resolve the installed Skill directory without
assuming Claude Code's plugin directory and replace two example home paths with
generic absolute-path anti-patterns. Exact source and packaged hashes are
recorded in `catalog/portable_patches.json`.

The `planning-workflows` pack contains the `brainstorming` Skill from
[`obra/superpowers`](https://github.com/obra/superpowers) at commit
`d884ae04edebef577e82ff7c4e143debd0bbec99`, published under the MIT
License. The imported scripts and references match the pinned Git tree.

The same pack contains a portable Skill-only adaptation of
[`OthmanAdi/planning-with-files`](https://github.com/OthmanAdi/planning-with-files),
published under the MIT License. It retains the three-file planning workflow,
templates, examples, and cross-platform initialization/completion scripts.
Cursor-only hook claims and unavailable plugin surfaces are removed; exact
source and packaged hashes are recorded in `catalog/snapshot_imports.json` and
`catalog/portable_patches.json`.

The `release-management` pack contains the `release-skills` Skill from
[`JimLiu/baoyu-skills`](https://github.com/JimLiu/baoyu-skills) at commit
`6b7a2e417500561a5ecdd0b168332f4142584617`, published under the MIT License.
The exact pinned Skill tree and upstream license are retained. Its workflow
requires a preview and user confirmation before creating a release commit or
performing a remote push/publication.

The `github-automation` pack contains a portable adaptation of the `gh-issues`
Skill from [`openclaw/openclaw`](https://github.com/openclaw/openclaw) at
commit `9a3a5ae818503aa0cdd4a960c12f84f24849a834`, published under the MIT
License. The adaptation removes OpenClaw-specific credential lookup,
notifications, unattended cron mode, and the no-confirmation option. It uses
the current Runtime's subagent surface and project-local claim state; exact
source and packaged hashes are recorded in `catalog/portable_patches.json`.

The `skill-discovery` pack contains the `find-skills` Skill from
[`vercel-labs/skills`](https://github.com/vercel-labs/skills) at commit
`e173b8c88f2581cfdaa1b6767c6519a08155790e`, published under the MIT
License. The imported Skill matches the pinned Git tree.

The `macos-integrations` pack contains the `apple-reminders` Skill from
[`steipete/remindctl`](https://github.com/steipete/remindctl) at commit
`ac09a1ca0c61b1eefa12a92ee20f38a98cc897d3`, published under the MIT
License. Only the root `SKILL.md` is imported from the pinned repository tree;
the CLI source and build files are not bundled.

The `research-workflows` pack contains the `deep-research` Skill from
[`bytedance/deer-flow`](https://github.com/bytedance/deer-flow) at commit
`d4fdc2758e9b23c79b1c148351700b52725a4644`, published under the MIT
License. Only the exact pinned `skills/public/deep-research` Git tree is
redistributed.

The `summarization` pack contains the `summarize` Skill from
[`openclaw/openclaw`](https://github.com/openclaw/openclaw) at commit
`1781e2e8f7ca9a446dec21916b762a062157a360`, published under the MIT
License. Only the exact pinned `skills/summarize` Git tree is redistributed;
the separate `summarize` CLI is reported as a required dependency by doctor.

The `product-management-noncommercial` pack contains ten mutually referenced
Skills from
[`deanpeters/Product-Manager-Skills`](https://github.com/deanpeters/Product-Manager-Skills)
at commit `99710188c134acf590a02c0e4ee1f431e60004cf`, published under
CC BY-NC-SA 4.0. They are redistributed without modification as a dependency
closure. These Skills may be used and shared only for noncommercial purposes;
attribution and ShareAlike remain required. The original license is retained
inside the pack.

The `persona-authoring` pack contains the `huashu-nuwa` Skill from
[`alchaincyf/nuwa-skill`](https://github.com/alchaincyf/nuwa-skill) at commit
`72857dc720f4d1dd3e68a40a544341dfc65ea33e`, published under the MIT License.
Only the root Skill, three method references, and four helper scripts are
redistributed. The packaged Skill replaces Claude-specific install paths with
the active Runtime's project Skill root and replaces pirate-book sources with
lawful source options; exact source and packaged hashes are recorded in
`catalog/portable_patches.json`.

The `browser-automation` pack contains a maintainer-authored OpenCLI usage Skill
derived from the public documentation and tool behavior of
[`jackwener/opencli`](https://github.com/jackwener/opencli) at commit
`5256711a25458e537c5a63d2a6f9c7fd36d0d1eb`, published under Apache-2.0.
The upstream license is retained in the pack. Portability and safety edits
remove maintainer-machine state and require explicit confirmation before
external account mutations; exact hashes are recorded in
`catalog/portable_patches.json`.

The `browser-control` pack contains the `agent-browser` Skill from
[`vercel-labs/agent-browser`](https://github.com/vercel-labs/agent-browser) at
commit `b48700c36351aad959d05c5c9bba2fb2fc3f9705`, published under Apache-2.0.
The exact pinned Skill tree and upstream license are retained.

The `spec-driven-development` pack contains four Skills from
[`Fission-AI/OpenSpec`](https://github.com/Fission-AI/OpenSpec) at commit
`81d5109b86f16537deb99f84a772a83235dc9e09`, published under the MIT License.
Each imported Skill directory matches its pinned Git tree, and the upstream
license is retained inside the pack. The OpenSpec CLI is installed separately
by the recipient.

The `generated-domain-perspectives` pack contains twenty-five maintainer-created,
AI-generated simulations based on public sources. They are not affiliated with
or endorsed by the named people. The public pack retains the runtime Skill
files and the small routing or calibration references they actually load; full
research drafts, build checkpoints, and validation workpapers are not
redistributed. Two text-only portability edits replace Cursor-specific source
paths with runtime-neutral locations, with exact hashes recorded in
`catalog/portable_patches.json`.

The `original-workflows` pack contains eleven maintainer-created Skills selected
from the active project configuration. Runtime files and directly referenced
support material are imported by exact SHA-256 snapshot; test prompts and
internal build material are not redistributed.

The `experimental-self-improvement` pack contains the maintainer-created
`self-evolve` Skill. The public adaptation keeps experiment state inside the
user-selected project and removes unattended scheduling or background-loop
assumptions. Installing or updating dependencies or Skills, modifying Agent
configuration, Rules, Hooks, or schedules, running non-read-only commands,
deleting files, and writing to external systems all require separate explicit
user approval. Exact source and packaged hashes are recorded in
`catalog/snapshot_imports.json` and `catalog/portable_patches.json`.

The `lenny-product-workflows` pack contains locally adapted versions of
`defining-product-vision` and `measuring-product-market-fit` from
[`RefoundAI/lenny-skills`](https://github.com/RefoundAI/lenny-skills) at commit
`0123453c617e1114d3097380feffb09761ce824a`, published under the MIT License.
The product-vision adaptation adds an evidence gate and resolves its optional
JTBD reference without a Cursor-only path. The product-market-fit adaptation
uses a shorter routing description. The original source references and license
are retained, and exact source and packaged hashes are recorded in
`catalog/snapshot_imports.json` and `catalog/portable_patches.json`.

The `marketing` pack also contains a reviewed local snapshot of
`marketing-strategy-pmm`, attributed to Alireza Rezvani and derived from
[`alirezarezvani/claude-skills`](https://github.com/alirezarezvani/claude-skills),
published under the MIT License. Its exact installed source hash and the
upstream license hash are recorded in `catalog/snapshot_imports.json`.

The `financial-research` pack contains a reviewed local adaptation of
`chanlun-trading` from
[`noahnan-max/chanlun-trading-system`](https://github.com/noahnan-max/chanlun-trading-system),
published under the MIT License. It is for research and study only and does not
provide investment advice, direct buy or sell instructions, or return promises.
Three retained legacy installation references were made runtime-neutral; exact
source and packaged hashes are recorded in `catalog/snapshot_imports.json` and
`catalog/portable_patches.json`.

The `maintainer-advanced-workflows` pack contains sixteen maintainer-created
Skills from the active project configuration. The public adaptations remove
private Vault paths, mandatory personal-profile reads, and Cursor-only Skill
lookups while preserving the workflows. Independent review uses the active
Runtime's available surface, and worktree creation requires approval of the
exact repository, branch, and path. Exact source and packaged hashes are
recorded in `catalog/snapshot_imports.json` and
`catalog/portable_patches.json`; test prompts and private source notes are not
redistributed.

The `research-workflows` pack additionally contains three maintainer-created
JTBD review research Skills. The public snapshot excludes real customer-review
examples, private project paths, and test prompts. The optional automated batch
runner uses Cursor Agent's `agent` CLI; the research and audit procedures remain
usable without that backend. Exact source and packaged hashes are recorded in
`catalog/snapshot_imports.json` and `catalog/portable_patches.json`.

The `knowledge-vault` pack additionally contains four maintainer-created
Zettelkasten workflows. The public adaptations discover project conventions
instead of assuming private Vault paths, default to proposals before writes,
and require separate confirmation before file deletion. Exact source and
packaged hashes are recorded in `catalog/snapshot_imports.json` and
`catalog/portable_patches.json`; private test prompts are not redistributed.

The `marketing`, `media`, and `web-extraction` packs additionally contain the
maintainer-created `reddit-geo`, `rednote-caption-to-screenshots`,
`rednote-reader`, `short-video`, and `claude-system-prompt-anatomy` Skills.
Reddit automation and current platform
policy claims must be checked against official sources; spam, hidden
affiliation, vote manipulation, and terms-avoidance are outside the workflow.
Exact source and packaged hashes are recorded in
`catalog/snapshot_imports.json` and `catalog/portable_patches.json`.
The Rednote public snapshot intentionally excludes Markdown-to-card templates
derived from an upstream repository that does not currently include a license
file; it retains the independently authored HTML deck renderer and validator.

The `cultural-practices` pack contains the maintainer-created `liuyao` Skill.
It presents a traditional divination framework for cultural reflection and
structured discussion, not factual prediction or professional advice. Exact
source and packaged hashes are recorded in `catalog/snapshot_imports.json` and
`catalog/portable_patches.json`; internal research notes are not redistributed.
