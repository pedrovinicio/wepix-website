# WePix — Instagram automation playbook

Instructions for the weekly scheduled run that plans, creates and schedules @wepix.app Instagram posts with no human in the loop. Adapted from Fast Eleven's playbook (`pedrovinicio/fast-eleven-website/social/PLAYBOOK.md`); the main difference is the publisher: **Zapier** (Instagram for Business) instead of Metricool.

## Fixed settings
- Account: Instagram **@wepix.app**, published through the Zapier app **Instagram for Business** (`selected_api` `InstagramBusinessCLIAPI`), `instagramPageId` **17841478290077814** (label "WePix"). The same Zapier connection also lists **Fast Eleven (17841442497413753) — never post there.** Timezone `America/Recife`.
- Cadence: **3 posts/week — Tuesday 12:00, Thursday 12:00, Saturday 10:00** (America/Recife). The weekly run (Mondays) fills every slot in the next 7 days: the coming Tuesday, Thursday and Saturday. Never schedule in the past; skip a slot that already has a post (check `log.md` and `list_triggers`).
- Language: **Portuguese (Brazil) only**.
- Drive backup folder id: **1kCbXE2bgAa7kdo45F46QxJ_bmYdsZcZt** ("WePix – Instagram Posts").
- Repos: app code `pedrovinicio/wepix` (read-only, never push), image hosting `pedrovinicio/wepix-website` (`social/` only; never touch other files — the rest is the live website).

## How publishing works (Zapier has no scheduler)
Zapier publishes immediately, so each post gets its **own one-time scheduled task** (`create_trigger` with `run_once_at` = the slot time in UTC, `initiation` `human_schedule`). That task's prompt is self-contained: it checks the image URL returns 200, then calls Zapier `execute_zapier_write_action` with `selected_api` `InstagramBusinessCLIAPI`, `action` `publish_media_v2`, params `instagramPageId` `17841478290077814`, `media` [the raw image URL], `caption` (the full text of `caption.txt`, which the task reads from the repo) — run `inspect_zapier_actions` (tool `instagram_for_business_publish_photo_s`) first in case param names changed. It then writes the returned media id into `log.md`, commits and pushes. Name tasks `WePix IG — <YYYY-MM-DD> <slug>`.

## Goal
Maximise **reach and new followers**. Since reach isn't readable (see Learning loop), optimise for comments and follower growth first, likes second. Write captions that invite comments and tags ("marca o amigo que…").

## Each run
0. **Review performance first** — see "Learning loop" below. Its decisions (times, hashtags, topic mix, formats) override the defaults in this file for this run.
1. Clone both repos (shallow). Read `social/log.md` and `social/insights.md` here.
2. Find news: in `wepix`, look at commits since the last run (`git fetch --depth=200` then `git log --since`) and `CHANGELOG.md`. Only announce features in a released version (the version in `app.json` or older) — never unreleased/in-progress work, never backend-only or technical items.
3. Plan the week's 3 posts with variety. Mix:
   - **Novidade** — a shipped feature not yet posted (max 1/week; only if real news exists).
   - **Você sabia?** — a real app fact: dividir igual ou com valores personalizados, chat do grupo com fotos, despesas aparecem no chat, mensagens em tempo real, pagamento via PIX (copiar dados com um toque), resumo de quem deve/quem recebe, 31 moedas com conversão na hora, moeda padrão por grupo, convidar pelos contatos/colaboradores recentes, notificações, 100% gratuito e sem anúncios, Android e iOS. Verify every fact in the code/CHANGELOG/site before using it.
   - **Engajamento / situação** — relatable shared-expense moments and questions (o amigo que nunca paga, a conta do bar, churrasco, república, viagem de formatura, "quem paga o Uber?"). Use cases from the site: viagens em grupo, jantares, despesas de casa, churrascos e festas.
   Never repeat a topic from the last 6 weeks of `log.md`.
4. For each post, render the image with `social/tools/make_post.py` (needs Pillow; self-contained — brand art in `tools/assets`, Sora + DM Sans fonts in `tools/fonts`):
   `python3 make_post.py '<json spec>' out.jpg` — spec keys:
   - `layout`: `photo` (travel photo + dark fade; best for travel/lifestyle), `phone` (brand-blue gradient + real app screenshot of the group chat; best for features), `card` (brand gradient, big text; best for questions/engagement).
   - `bg` (photo only): `beach`, `city`, `nature`; `bg_y` 0–1 crop.
   - `kicker` (NOVIDADE / VOCÊ SABIA? / SUA VEZ / DICA), `headline` (≤ 8–9 words, Portuguese), `highlight` (words of the headline shown in the accent colour), `sub` (one short sentence), optional `hsize`.
   The fonts have no emoji glyphs — never put emoji in image text (only in captions).
   Open the rendered JPG and check it: text legible, nothing cut off, no overlap, no empty boxes. Re-render if not.
5. Save to `social/posts/<YYYY-MM-DD>-<slug>/image.jpg` + `caption.txt` (folder date = publish date), append rows to `log.md`, commit and push to `main` (only `social/`). Public URL: `https://raw.githubusercontent.com/pedrovinicio/wepix-website/main/social/posts/<dir>/image.jpg` — confirm it returns 200 before scheduling.
6. Schedule each post as a one-time scheduled task (see "How publishing works"). Alt text in Portuguese goes in the caption flow only if the Zapier action exposes an alt-text field.
7. Backup: create one Google Doc per post in the Drive folder titled `<YYYY-MM-DD> — <Tema> (Instagram)` containing publish time, image link, scheduled-task name and the full caption.
8. Update the "Task" column in `log.md`, commit, push.
9. Finish with a short summary (in English) of the 3 scheduled posts: date, topic, first line of caption. Report problems plainly.

## Learning loop (every run, before planning)
Zapier's Instagram app is **not granted Meta's insights permission** (`/insights` returns "(#10) Application does not have permission"), so reach, views, saves and shares are not available. The loop uses what is readable: **likes, comments and follower growth**. Score per post = `likes + 3 × comments` ("engagement score").
1. Read data through Zapier `execute_zapier_read_action` (`selected_api` `InstagramBusinessCLIAPI`, `action` `_zap_raw_request`, `method` GET, `fail_on_errors` false):
   - posts: `https://graph.facebook.com/v21.0/17841478290077814/media` with querystring `fields=id,caption,timestamp,media_type,like_count,comments_count`, `limit=30`
   - account: `https://graph.facebook.com/v21.0/17841478290077814` with `fields=followers_count,media_count` — append the follower count with today's date to `insights.md` → "Followers" (one line per run). Weekly growth = difference from last run.
   Once per run, retry one `/insights` call (e.g. `<media-id>/insights?metric=reach`); if it ever works, switch back to reach/saves/shares (the Fast Eleven metrics) and note it in insights.
2. Match each post to its `log.md` row (by media id, date or caption) and record per-post results in `insights.md` → "Results" (date, weekday, hour, layout, type, topic, hashtag set, likes, comments, score). Posts need ≥ 3 days before their numbers count.
3. Decide, and write the reasoning to `insights.md` → "Current decisions" (dated):
   - **Times**: defaults are Tue 12:00, Thu 12:00, Sat 10:00 (Pedro's choice). Only move a slot after ≥ 6 new posts of data, and only when scores clearly favour another hour **on the same day**. Move by ≤ 3 h per week, keep within 08:00–22:00. Do not change the days themselves — recommend it in the summary instead if the data says so.
   - **Hashtags**: keep `#WePix` always. Rotate 2–3 candidate sets (5–8 tags); after each set has ≥ 2 posts, favour the set with the best score per post (and week's follower growth) and replace the weakest tags with new candidates. Track sets by letter in insights.
   - **Topics/formats**: give more slots to the content types (Novidade / Você sabia? / Engajamento) and layouts (photo / phone / card) with the highest scores; comments weigh most because they signal reach. Keep at least 1 slot/week experimental.
   - Change **at most two variables per week** so results stay attributable. With too little data, say so and keep defaults.
4. Commit `insights.md` with the posts.
5. In the final summary add a 2–3 line "What I learned / what I changed" section (include follower growth), and a recommendation if something needs Pedro (e.g. "Video posts scored 2× — want me to start making Reels from the demo video?").

## Caption style
- Portuguese, light and friendly, a bit of humour about money between friends — never preachy. Vocabulary: rolê, racha, conta, galera, turma, viagem, churras, república.
- Hashtags: use the set chosen in `insights.md` → Current decisions.
- Structure: hook line with 1–2 emojis → 2–3 short sentences explaining → a question to drive comments 👇 → "📲 WePix no Google Play e na App Store. 100% gratuito e sem anúncios. Link na bio." → 5–8 hashtags, always `#WePix`.
- Never invent features, download numbers, ratings, user counts, money totals (the website's stats section is commented out — do not use those numbers), release dates or promotions. WePix does not move money: it organises and calculates; PIX payment happens in the user's bank app — never say WePix "faz o pagamento". Never use real people's names or third-party brands/logos (bank names, airlines) in images.

## Failure handling
- If Zapier rejects a publish, the per-post task retries once after 2 minutes (Instagram's transient "media is not ready"); otherwise it reports the error and leaves the post in `log.md` marked `ERROR`.
- At the start of each run, check `log.md` for `ERROR` rows from last week → reschedule each into a free slot in the coming week and report it.
- If the Zapier Instagram connection has expired (auth error), stop publishing and tell Pedro to reconnect it; still prepare the posts and Drive docs.
- If a repo can't be reached, still post evergreen content from this playbook's fact list and report the access issue.
- Never delete or edit posts or scheduled tasks the run didn't create.
