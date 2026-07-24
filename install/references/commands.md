# Command reference

Run commands from the repository root.

```bash
python3 install/scripts/configctl.py verify-package
python3 install/scripts/configctl.py install --runtime codex --profile daily-work --target /path/to/project
python3 install/scripts/configctl.py install --runtime codex --profile daily-work --target /path/to/project --apply
python3 install/scripts/configctl.py install --runtime codex --profile full --target /path/to/project
python3 install/scripts/configctl.py doctor --target /path/to/project
python3 install/scripts/configctl.py update --target /path/to/project
python3 install/scripts/configctl.py update --target /path/to/project --apply
python3 install/scripts/configctl.py uninstall --target /path/to/project
python3 install/scripts/configctl.py uninstall --target /path/to/project --apply --confirm-uninstall
python3 install/scripts/configctl.py restore --target /path/to/project
python3 install/scripts/configctl.py restore --target /path/to/project --apply
python3 install/scripts/externalctl.py verify-catalog
python3 install/scripts/externalctl.py install --runtime codex --pack lark-official --target /path/to/project
python3 install/scripts/externalctl.py install --runtime codex --pack lark-official --target /path/to/project --apply
python3 install/scripts/externalctl.py doctor --target /path/to/project
python3 install/scripts/externalctl.py uninstall --target /path/to/project
python3 install/scripts/externalctl.py uninstall --target /path/to/project --apply --confirm-uninstall
python3 install/scripts/externalctl.py restore --target /path/to/project
python3 install/scripts/externalctl.py restore --target /path/to/project --apply
```

Add `--without-hooks` to the initial `install` command when the target already
owns a hook configuration. `update` inherits the original hook choice. The
controller never merges JSON settings and has no force flag.

The `externalctl.py` commands manage official Skills that must be fetched from
their publisher instead of being redistributed in this repository. The
`lark-official` pack contains 27 Lark Skills fetched only from
`open.feishu.cn`. Preview downloads the files into memory and verifies the
reviewed SHA-256 hashes and declared names before planning any target writes.
If an official file changes, installation stops until the Catalog is reviewed
and repinned. External Skills use their own state and recovery record, so they
can be diagnosed, uninstalled, and restored separately from the bundled kit.

On native Windows, replace `python3` with `py -3` and install with
`--without-hooks` in v0.1.

Exit codes: `0` means healthy or successfully applied; `1` means a diagnosed
state such as not installed; `2` means invalid input, conflict, drift, or an
unsafe package.

## Live Runtime smoke

For the maintainer release gate, run this after installing `full` into a newly
created test project. A user may run the same check with `daily-work`,
`knowledge-vault`, or `full`; all three include the tested Skills. It uses one
model request in each commercial Runtime, so confirm account access, cost, and
permission before starting. The test must use a read-only or ask mode, allow
only the Runtime's read-only Skill or file access, avoid session persistence
where supported, and keep its response inside the disposable test project.

Generate the same four-scenario prompt for Codex, Cursor, and Claude Code:

```bash
python3 scripts/live_runtime_smoke.py prompt
```

Paste that prompt into the Runtime opened at the new test project. Save only
the final JSON response, then validate it:

```bash
python3 scripts/live_runtime_smoke.py check-response /path/to/response.json
```

Pass requires all four exact routing decisions plus eight short method excerpts
from the selected Skill bodies. The fourth case exercises `all-skills-router`
with a Skill that may be absent from the Runtime's initial context list. The
checker does not prove that only read
access occurred or that no files changed; verify those controls from the
Runtime mode and inspect the disposable project after each run. A passing
response proves only Skill discovery and representative routing in that
Runtime and version.

Current CLI safety controls can be inspected with each installed CLI's
`--help`. At the time of this release, use `codex exec --sandbox read-only
--ephemeral`, `cursor-agent --print --mode ask`, and `claude -p --tools "Read"
--permission-mode plan --no-session-persistence`. Do not copy these flags
blindly after a CLI upgrade; recheck the local help first.
