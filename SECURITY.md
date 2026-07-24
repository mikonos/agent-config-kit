# Security

Report suspected credential exposure privately to the repository owner before
opening a public issue.

The kit must not contain credentials, personal workspace state, transcripts,
absolute home-directory paths, private account identifiers, or enabled
external-service integrations. Public repository ownership and required
open-source attribution are allowed. Installation is dry-run by default and
fails on conflicts.

Hooks included in the default profile are local and read-only. Account access,
background workers, external writes, paid calls, and destructive actions are
outside the default distribution.

Apply, uninstall, and restore operations assume the target project is not being
concurrently mutated by another process running as the same operating-system
user. The controllers reject pre-existing symlinks and reparse points, stop on
conflicts, create fetched Skill files exclusively, and roll back handled
failures. They do not claim to defend against a same-account process replacing
an ancestor directory during the operation; such a process can also modify the
installer and its local state directly. Close editors, sync jobs, and other
installers that write the target while applying a plan.
