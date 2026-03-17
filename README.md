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
