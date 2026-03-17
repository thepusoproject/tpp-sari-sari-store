# TPP Py4E — Teacher / TA Runbook

Quick reference for onboarding students, reviewing modules, and keeping automations healthy.

## 1. Onboard a new student
1. Verify their repo name: `tpp-sari-sari-store-<name>` (public).
2. Check they added `thepusoproject` as collaborator (GitHub shows a notification—accept it).
3. Add them to `gradeboard/roster.json` with:
   ```json
   { "handle": "github-username", "repo": "owner/repo" }
   ```
4. (Optional) Ask them to run `git remote add upstream https://github.com/thepusoproject/tpp-sari-sari-store.git` so future template updates are easy.

## 2. Review a module PR
1. Confirm the PR title: `Module XX - <short title>`.
2. Check the **Module Grade** workflow result:
   - ✅ → merge.
   - ❌ → leave feedback; ask the student to push fixes and rerun.
3. After merging, ensure the follow-up push run succeeds (it should commit `chore: update gradebook`).
4. Pull `main` locally if you want to keep an archive or run spot checks.

## 3. Gradeboard + dashboards
- Roster changes or merges auto-trigger the **Gradeboard** workflow; it also runs nightly at 00:00 UTC.
- Output lives at `docs/grades.json` + `docs/index.html`. With GitHub Pages enabled (`main /docs`), the public URL is `https://thepusoproject.github.io/tpp-sari-sari-store/`.
- Search box lets you filter by name/handle; the “Last Push” column shows recent activity.

## 4. Stale PR reminders (workflow)
- `.github/workflows/stale-prs.yml` checks every student repo daily. If a module PR stays open >24h, the job fails and logs the repo/PR URL (GitHub emails the failure to repo maintainers).
- You can also trigger it manually via **Actions → Stale Module PR Reminder → Run workflow**.

## 5. Troubleshooting
| Symptom | Fix |
| --- | --- |
| `Module Grade` workflow missing on a student repo | They didn’t clone the latest template. Ask them to re-template or pull upstream. |
| Gradebook not updating after merge | Re-run the workflow from Actions or verify `python scripts/compute_grade.py` locally. |
| Collaborator invite not received | Have the student resend from **Settings → Collaborators**; accept from your notifications bell. |
| `git push` blocked in Hostinger container | Run `git config --global --add safe.directory <path>` for the repo or ensure `chown -R node:node <path>`. |

## 6. Future enhancements (parking lot)
- Add notifications to Slack/Discord from the stale PR workflow.
- Parse multiple modules per student once we store a history file per repo.
- Auto-file GitHub issues when a workflow fails repeatedly.
