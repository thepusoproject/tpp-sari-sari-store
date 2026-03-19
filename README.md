# TPP Sari-Sari Store (CLI) — Student Project

This is the evolving case study project for the Programming para sa Lahat track.

## How to run
- `python main.py` (or `python3 main.py`)

## Modules
Implement requirements module-by-module. Your instructor will grade via Pull Requests.

## Student quick start
1. Clone your repo and create a virtualenv:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the starter app: `python main.py`
3. Run the tests before every PR: `pytest`
4. Add the template as `upstream` (see section below) so you can pull updates anytime.
5. Invite `thepusoproject` as a collaborator so grading + reviews work smoothly.

## Concept checks (bagong requirement)
- Bawat module folder (`modules/module_XX/CONCEPT.md`) may Taglish prompts. Palitan ang `{{ISULAT_DITO}}` placeholders gamit ang sariling paliwanag (≥ 2 sentences bawat tanong).
- Tuwing magbubukas ka ng PR, isang bot ang magpo-post ng 2 random na tanong mula sa module na iyon. Sagutin ang thread bago mag-request ng review.
- Lahat ito ay kasama sa iisang PR kasama ng code changes mo, kaya isang submission lang per module.

## Optional AI helpers (M01–M02)
Need to showcase “smart” feedback? Export your OpenAI key (or set it as a repo secret) and flip the feature flags below. Every prompt is capped to short Taglish sentences so token usage stays tiny.

| Feature | How to run | Env flags | Output |
| --- | --- | --- | --- |
| Concept triage | `AI_CONCEPT_TRIAGE=1 python scripts/check_concepts.py --ai-report ai_concepts.md` | `OPENAI_API_KEY`, optional `AI_MODEL` | ≤40-word verdict per module (also printed to stdout). |
| Receipt mentor hints | `python scripts/ai_receipt_hint.py grade_report.json --output ai_hint.txt` | `AI_RECEIPT_HINTS=1` to enable LLM fallback | One Taglish hint when pytest fails (uses heuristics before AI). |
| Adaptive badge | `AI_BADGES=1 python scripts/ai_badges.py` | `AI_BADGES=1` to call the model | `badges/latest.json` with metrics + ≤30-word badge text. |

If the env var is unset, each script stays deterministic (no API call) so you can keep costs at zero until you actually want the AI narrative.

On GitHub Actions, set the repo secret `OPENAI_API_KEY` and the Module Grade workflow (pull_request events only) will automatically run the same triage/hint/badge scripts—artifacts are attached to each run while pushes stay deterministic.


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
The teacher repo ships with a simple dashboard under `docs/`. Features:
- Search/filter by student name or handle (client-side search box).
- Student names auto-pull from GitHub profiles (unless you override `displayName`).
- Shows latest module, score, grade timestamp, and last push time.

How to enable it:
1. Ask each student to open the **Roster signup** issue template in this repo so you get their handle/repo details.
2. Copy their info into `gradeboard/roster.json` (handle, optional display name, repo URL). If `displayName` is omitted, the GitHub profile name is pulled automatically.
3. GitHub Actions workflow **Gradeboard** fetches each repo’s `grades/latest.json` and writes `docs/grades.json`.
4. Enable GitHub Pages → **Settings → Pages → Deploy from branch → main /docs**.
5. Share the Pages URL (`https://<org>.github.io/tpp-sari-sari-store/`) to show the live grade table.

The workflow runs on every roster change, manual dispatch, and at midnight UTC, so the dashboard always reflects the latest merges.
