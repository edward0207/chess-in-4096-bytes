# chess-in-4096-bytes

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/edward0207/chess-in-4096-bytes/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/edward0207/chess-in-4096-bytes/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 4,096 bytes of Python, standard library only.

The board is 64 characters, `0=a8 .. 63=h1`, and UPPERCASE is always the side to
move. Every ply the board is mirrored vertically (`i^56`) and case-swapped, so move
generation only ever handles one colour and the castling squares stay at 56/60/63.
Mirroring, not the usual 180-degree rotation, is what keeps files fixed.

Search is negamax alpha-beta with a quiescence search over captures, MVV-LVA move
ordering and iterative deepening under a fixed node budget. No clock and no
randomness, so a replay plays the same moves. An iteration cut short by the budget
is discarded rather than used. When a position recurs, the move played there last
time is excluded, which breaks shuffling draws.

Move generation is **perft-verified to depth 5** against the published counts:
4,865,609 from the start position and 4,085,603 on Kiwipete, plus four more
positions covering en passant, castling rights, promotion and pins.

## Run it

```sh
MAKEFUN_ENV_URL=http://store:8080 python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=s5f3fzer&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
