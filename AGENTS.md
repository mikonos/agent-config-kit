# Agent Config Kit contributor contract

This repository distributes portable Agent rules, skills, and safe hooks.

## Source of truth

- `manifest.json` defines profiles, packs, runtime targets, and installed files.
- `packs/` contains portable source content.
- `adapters/` contains generated runtime projections. Regenerate them with
  `python3 scripts/build_adapters.py --apply`.
- `install/SKILL.md` is the only human-facing installation and maintenance entrypoint.

## Working rules

- Read the manifest and the target pack before editing behavior.
- Keep paths relative. Never add personal names, home-directory paths, credentials,
  session data, or private workspace state.
- Do not silently overwrite an existing target file. Conflicts must fail closed.
- Keep hooks local, read-only, fast, and disabled where the runtime has no supported hook surface.
- Add no dependency when the Python standard library is sufficient.
- Make surgical changes and preserve unrelated user work.

## Verification

Run before declaring work complete:

```bash
python3 scripts/build_adapters.py --check
python3 scripts/verify.py
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py install
```

