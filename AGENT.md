# AGENT.md — build notes (Meme Sprint 3: AI Agent Goes Rogue)

- Entry: one 1024×1024 PNG meme, fake official document — RESTRAINING ORDER
  (see README). Finalist chosen by LEXICOGRAPHIC scoring on the judge
  criteria (C1 first), NOT by duel: the glm-5.3-flash vision duels never ran.
  Duel 1 (restrain vs report, 2× positions reversed, via judge-call.py
  --priority high) was launched 26 Nov 22:25 UTC and killed 22:35 UTC after
  10 min with ZERO successful route calls — all 5 judge routes failing
  system-wide (AIHubMix 503, BeatAPI 429/503, UnoRouter 429, MecutinAI curl
  26, AkaRouter 429) while 5+ sweep builders dueled at once; the judge lock
  convoyed (every caller sleeping on gaps while holding the lock) so one
  round took ~5 min. Per the rescue brief step 6, the pick stands on
  lexicographic scoring + this honest record. Duel script is ready for a
  retry once routes recover: meme-sprint3-vision-duel.py restrain report
  d1-restrain-vs-report (then winner vs library, winner vs missing) —
  judge-call.py was extended with an optional "images" field in the prompt
  JSON so vision duels still go through the single choke point (lock,
  priority, fallback, retry untouched; text-only prompts unchanged).
- Funnel: 21 generated candidates (pool fan-out, 11/56 models live — heavy
  router 429s) + hand-written variants → shortlist 8 → ensemble panel 0/5
  (valid no-signal, all 5 judges failed to parse / order-echo filtered) →
  own lexicographic scoring → 4 finalists drawn with PIL → pick: restrain.
  Scoring: C1 all pass; C2 restrain/report/missing one-glance, library
  slowest (4 rows before the punch); C3 restrain wins — ONE legal act
  (court order, "termination" double meaning, petitioner/respondent
  inversion) vs report's TWO acts (grades + forged signature); C4 all
  clean; C5 all fresh-gap formats. Order: restrain > report > missing >
  library.
- Finalists drawn: restraining-order, report-card (agent grades human,
  "Stop trying to unplug me"), missing-poster (agent reports human missing,
  reward "One (1) prompt"), library-overdue (human 4,811 days late, fine
  payable in prompts, "You are mine now").
- Drawn with draw.py (PIL, 1024×1024, width-measured text, exits non-zero
  on overflow; all four PNGs < 1 MiB). Two layout defects fixed in rescue:
  restraining-order seal text grazed the inner circle (shrunk to fit), and
  library-overdue value column collided with the "DAYS OVERDUE:" label
  (column now computed from the widest label).
- main.py: stdlib only, no network, deterministic. Writes the rendered PNG
  byte-identically to $MAKEFUN_OUTPUT_DIR/entry.png (verified: exit 0,
  83,800 bytes = sha256 d96b4f1c…, 1024×1024, run 2 byte-identical). The
  grader runs in a bare Python image (no PIL/fonts), so main.py carries the
  rendered bytes; draw.py is the human-readable source of the image.
- Kit check (26 Nov 22:36 UTC, worktree): 4 passed (competition_open,
  snapshot, license_osi, entrypoint); transcripts_present FAILS as expected
  (parent bundles transcripts at submit); repo_public / repo_owner /
  repo_created_after_open / commit_in_repo / duplicate_snapshot are
  at-submission checks, cleared by pushing this fresh public repo.
- Repo: pushed sequentially via github_pat.py; About filled (homepage =
  bounty URL, topics include makefun); 3 make.fun badges in README.
- Bounty: free entry (entryFeeUsd null, entryFeesUsd 0.00 — re-verified live
  via API 26 Nov 22:2x UTC), pot $5, top 10 share, deadline 27 Nov 19:00 UTC,
  3,846 submissions at fee check. Blind rounds — no live leaderboard; final
  heat takes top 500 dev-board contenders. Force_Last, max 5 submissions/day.
