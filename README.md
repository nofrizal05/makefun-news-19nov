# makefun-news-19nov

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/nofrizal05/makefun-news-19nov/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/nofrizal05/makefun-news-19nov/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Day — 19 November 2026

One image that sums up the world news of Thursday 19 November 2026,
drawn as a newspaper front page. Six stories carry the day:

1. **GTA VI arrives** — after a 13-year wait, gamers step into Vice City as Rockstar's epic begins its global rollout.
2. **Trump, Xi and Putin meet in Shenzhen** — the three leaders sit down together for the first time, at the APEC summit.
3. **US–Iran strikes widen to Kuwait** — Iran hits a US base in Kuwait and Bahrain again, days after the US struck Qeshm Island.
4. **Jeffries set to be first Black Speaker** — Democrats nominate Hakeem Jeffries to lead the US House of Representatives.
5. **Cyclone Akvan nears India's coast** — the storm is set to cross between Machilipatnam and Puri, with railways on alert.
6. **Voyager 1 reaches one light-day from Earth** — NASA confirms the milestone, nearly 50 years after launch.

Also on the page: the EU's planned €45bn loan for Ukraine, Fed minutes pointing to more rate rises, and Nvidia halting H-series chips to China.

The picture itself is `entry.png` (1024×1024 PNG, under 1 MiB): a navy masthead naming the day, GTA VI as the lead story, four more stories in a two-by-two grid, a Voyager 1 strip, and an "Also" line for the day's other headlines. Every illustration was drawn in code — sunset skyline, summit table, Gulf radar, Capitol dome, cyclone spiral, deep-space probe — so the image stands on its own.

## How it runs

The grading sandbox has the Python standard library only and no network, so `main.py` does not draw anything at run time: it copies the shipped `entry.png` to the output directory, byte for byte. That is the simplest entry the rules allow, and it is fully deterministic — two runs write identical files. An earlier version of this program drew the page with Pillow, which the sandbox does not install; the copy keeps the same image while needing nothing beyond the standard library.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=31w76kz9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
