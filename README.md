# TPP Sari-Sari Store (CLI) — Student Project

This is the evolving case study project for the Taglish Py4E track.

## How to run
- `python main.py` (or `python3 main.py`)

## Modules
Implement requirements module-by-module. Your instructor will grade via Pull Requests.

## Automated grading
Every push/merge to `main` runs the **Module Grade** GitHub Action:
- Executes the module-specific pytest suite in `tests/`
- Writes the latest score to `grades/latest.json`
- Updates `GRADEBOOK.md` (committed on `main` after a merge)

Check the PR checks tab to see whether you passed before merging.

## Keeping your repo in sync with the template
When we publish fixes or new modules, pull them into your student repo without recloning:
1. Run once after creating your repo:
   ```bash
   git remote add upstream https://github.com/thepusoproject/tpp-sari-sari-store.git
   ```
2. Whenever we announce an update:
   ```bash
   git fetch upstream
   git merge upstream/main   # or: git rebase upstream/main
   ```
3. Resolve conflicts if Git shows them (usually only in files you’ve edited).

This keeps your local copy up to date with new modules, tests, or grading tweaks while preserving your own commits.

## Give your instructor access
To let grading and code review work smoothly:
1. Go to your repo on GitHub → **Settings → Collaborators & teams**.
2. Add `thepusoproject` as a collaborator with **Write** access.
3. Accept the invite (GitHub will show a banner). Once accepted, your instructor can review PRs and push feedback branches if needed.

## Gradeboard (GitHub Pages)
The teacher repo ships with a simple dashboard under `docs/`. To use it:
1. List all student repos in `gradeboard/roster.json` (handle, optional display name, repo URL). If `displayName` is omitted, the GitHub profile name is pulled automatically.
2. GitHub Actions workflow **Gradeboard** fetches each repo’s `grades/latest.json` and writes `docs/grades.json`.
3. Enable GitHub Pages → **Settings → Pages → Deploy from branch → main /docs**.
4. Share the Pages URL (`https://<org>.github.io/tpp-sari-sari-store/`) to show the live grade table.

The workflow runs on every roster change, manual dispatch, and at midnight UTC, so the dashboard always reflects the latest merges.
