# WePix — Instagram insights

Maintained by the weekly run. Learnings drive posting times, hashtags, layouts and topic mix (see PLAYBOOK → Learning loop). Metric: score = likes + 3 × comments (reach/saves/shares aren't readable through Zapier).

## Current decisions
- 2026-10-05 — Starting defaults. Slots: Tue 12:00, Thu 12:00, Sat 10:00. Hashtag set A. Layout mix: rotate photo / phone / card. The account was idle from 2026-03-31 to now, so early numbers may be low while it warms up — don't change anything before ≥ 6 new posts.
- 2026-10-06 — Weekly run #1. Only 1 post with data (multimoeda, <3 days old: 5 likes, 1 comment, preliminary score 8) and followers flat at 817 → too little data, no time/topic changes. Still rotating within defaults: hashtag set **B** goes live on Tue chat-tempo-real and Sat feriadão (so B reaches 2 posts next week); layouts this week cover phone (Tue), card (Thu), photo (Sat). Experimental slot: Sat uses a seasonal hook (feriadão 12/10), following the baseline lesson that local/seasonal situations drove comments. Reach insights still blocked ((#10) permission error, retried 2026-10-06).
- 2026-10-12 — Weekly run #2. Data (read 2026-10-12): multimoeda 7/1 → 10, chat-tempo-real 6/0 → 6, quarto-maior 1/0 → 1, feriadão 1/0 → 1 (preliminary, 2 days old). Followers 817 → 814 (−3). Still < 6 automated posts, so slots stay at defaults. Signals so far: zero comments since the first post; the two Engajamento posts (card on Thu, photo on Sat) got 1 like each — but the holiday-weekend Sat post and a 4-day-old card are too few to blame the format yet. Changes this week (2 variables): (1) **no card layout** this week (weakest score) → phone (Tue) + photo + photo; (2) hashtag set **C** goes live on Thu and Sat (C revised before first use: #Churrasco/#Republica swapped for #Galera/#ContaDoBar so it fits non-churras topics). Tue uses set A (A gets its 3rd post). No Novidade: no new release since v1.3.0. Experimental slot: Sat festival/ingresso (new situation, tag-a-friend hook). Reach insights still blocked ((#10), retried 2026-10-12).
- 2026-10-19 — Weekly run #3. Data (read 2026-10-19): multimoeda 7/1 → 10, chat-tempo-real 6/0 → 6, quarto-maior 1/0 → 1, feriadão 1/0 → 1, conta-restaurante 3/0 → 3, ingresso-festival 2/0 → 2 (preliminary, 2 days old). Followers 814 → 813 (−1; −4 since automation started). 6 automated posts now: **zero comments on all 5 slot posts**. By type: Você sabia? avg 8 (n=2) vs Engajamento avg 1.75 (n=4). By layout: phone 6 (n=1), photo avg 3.5, card 1. By set (score/post): A 5.5, B 3.5, C 2.5 — but A/B are confounded with the Você sabia? posts. Times: no same-day comparison possible (every post in a slot ran at the default hour) → slots unchanged. Changes this week (2 variables): (1) **topic mix shifts toward Você sabia?** — Tue (convidar-galera, already prepared) + Thu (Pix Copia e Cola, phone) are both Você sabia?; Sat stays Engajamento as the experimental slot (noite de jogo/pizza, a new indoor situation, photo). (2) **Hashtag set C retired** (worst per post); both new posts use set **A** + topic tag. Next week: if Você sabia? keeps winning, test a second phone post vs a photo Você sabia? to separate type from layout. Reach insights still blocked ((#10), retried 2026-10-19).

## Baseline (posts before automation, read 2026-10-05)
16 posts, 2026-01-09 → 2026-03-31, 817 followers. Best scores: launch post "Chegou o WePix!" (37 likes, 11 comments → 70), churrasco (21/7 → 42), launch video (23/4 → 35), Carnaval Recife/Olinda carousel (20/3 → 29). Weakest: humour-only posts without a situation people recognise ("amigo que sumiu", 7/0) and generic travel captions (8–14 likes, 0 comments).
Takeaways: concrete, relatable group situations (churrasco, Carnaval) with a question beat abstract slogans; local/seasonal hooks (Recife, Carnaval) worked. Topics already used — avoid repeating soon: churrasco, road trip, piquenique, Carnaval, "amigo que some", "detetive", "jeito brasileiro", generic "viagem com amigos".

## Followers
| Date | Followers |
| :-- | --: |
| 2026-10-05 | 817 |
| 2026-10-06 | 817 |
| 2026-10-12 | 814 |
| 2026-10-19 | 813 |

## Hashtag sets
- **A**: #WePix #DividirContas #ViagemEmGrupo #ViagemComAmigos #FinançasPessoais #Pix + topic tag
- **B** (to test): #WePix #DividirDespesas #RachaConta #Amigos #ControleFinanceiro #AppDeFinanças + topic tag
- **C** (retired 2026-10-19 — weakest score/post; live 2026-10-15 → 2026-10-17): #WePix #Pix #Rolê #Galera #ContaDoBar #VidaDeEstudante + topic tag

## Results
| Publish | Weekday | Hour | Layout | Type | Topic | Set | Likes | Comments | Score |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | --: | --: | --: |
| 2026-10-05 | Mon | 16:18 | photo | Você sabia? | Multimoeda (test post, off-slot) | A | 7 | 1 | 10 |
| 2026-10-06 | Tue | 12:00 | phone | Você sabia? | Chat em tempo real | B | 6 | 0 | 6 |
| 2026-10-08 | Thu | 12:00 | card | Engajamento | Dividir apê / quarto maior | A | 1 | 0 | 1 |
| 2026-10-10 | Sat | 10:00 | photo | Engajamento | Feriadão 12/10 casa de praia | B | 1 | 0 | 1 |
| 2026-10-13 | Tue | 12:00 | phone | Você sabia? | Convidar pelos recentes/contatos (moved to 2026-10-20) | A | | | |
| 2026-10-15 | Thu | 12:00 | photo | Engajamento | Conta do restaurante: racha igual? | C | 3 | 0 | 3 |
| 2026-10-17 | Sat | 10:00 | photo | Engajamento | Ingresso do festival / amigo cobrador | C | 2* | 0* | 2* |
| 2026-10-22 | Thu | 12:00 | phone | Você sabia? | Pix Copia e Cola com valor certinho | A | | | |
| 2026-10-24 | Sat | 10:00 | photo | Engajamento | Noite de jogo: quem pagou a pizza? | A | | | |

\* preliminary (post < 3 days old when read on 2026-10-19); re-read next run.
