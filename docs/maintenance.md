# Maintenance

Use evidence from actual, private use to improve shared artifacts without copying private content into the repository.

## Monthly checklist

- [ ] Review parked idea titles and safe summaries; archive stale candidates.
- [ ] Re-score candidates whose constraints materially changed.
- [ ] Check whether the current hatchling remains the smallest useful version.
- [ ] Capture confusing prompt or template wording as an abstract issue.
- [ ] Add a synthetic eval for any repeated failure mode.
- [ ] Run `python scripts/validate_scaffold.py`.
- [ ] Review ignored files and staged changes for privacy leakage.

Update prompts and templates only after observed use shows a repeatable gap. Prefer one small rule plus an eval case over adding a large process.

## CI validation

CI runs `python scripts/validate_scaffold.py` on pull requests and pushes to `main`. The validator reads only repository and local generated test files, requires no secrets, and should be run locally before opening a pull request.

## Taxonomy handoff notes

When Hatching Ground produces reusable artifact lessons, capture them as public-safe handoff notes before proposing changes to the separate taxonomy repo. See `docs/ui-harness-taxonomy-notes.md` for the UI harness artifact lessons.

## Future issues

Open one issue per concrete problem. Include a synthetic reproduction, desired behavior, affected artifacts, acceptance criteria, and explicit non-goals. Do not paste real cards, logs, memory, state, screenshots, or machine paths. Runtime or integration proposals must explain why the file-first workflow is insufficient and identify privacy, permission, and human-approval requirements.
