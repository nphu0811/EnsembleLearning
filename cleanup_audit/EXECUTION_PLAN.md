# Approved cleanup and documentation rename execution

Spec: user approval of group B deletion, F renaming and Git synchronization, together with original immutable research constraints. Use writing-plans and verification-before-completion guidance; execute inline in current workspace on codex/workspace-cleanup-20261019 to avoid copying local datasets/environments.

- [x] Record pre-cleanup HEAD, exact four PDF SHA-256/size/path approvals and dirty diff. Preserve unknown untracked Word lock.
- [x] Create cleanup branch and fast-forward to live origin/main; four PDF deletions inherited from existing upstream commits, no duplicate git rm of absent files.
- [x] Rename the 53 task-labelled human documentation files from rename_plan.json with git mv; preserve scientific code/data/models/results/config/notebook, templates, environments, frozen evidence snapshots and presentation binaries.
- [x] Update current human navigation and the sole executable documentation consumer p19_safe_review_draft.py. Leave historical manifests/reviewer reports/packet snapshots unchanged; provide explicit old/new path and before/after hashes, and a resolver for current resume auditing that never makes changed hashes pass.
- [x] Validate canonical V7, frozen protocol, five-seed P21, scientific source/result byte identity, mapping uniqueness/existence and current consumer references. No training, prediction or test-data evaluation.
- [x] Measure before/after logical sizes, record actual four deletions and all rename/reference changes; distinguish removed file bytes from net workspace size and Git history.
- [ ] Commit only reviewed explicit changes, compact evidence and audit reports (large local environment inventory excluded from staging); safe push cleanup branch. Main merge awaits concrete final change approval.

Ruling: “rename all” applies to task-labelled human documents where scientific paths are not changed. Frozen notebook protocols, results/source names and copied snapshots keep legacy identifiers because the original user request prohibits changing completed train/TEST data and scientific provenance. No core information is discarded.
