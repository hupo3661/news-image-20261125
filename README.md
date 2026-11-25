# news-image-20261125 — The World in One Day

A newspaper front page summing up the world's news of **Wednesday
25 November 2026** in a single 1024×1024 image, for the make.fun
competition `news-image-20261125`.

## The image

* Masthead: **THE WORLD IN ONE DAY — Wednesday · 25 November 2026**
* Top story: China opens an anti-graft investigation into Politburo
  member and Shanghai party chief Chen Jining.
* Six more stories, each verified as first reported on 25 November 2026:
  1. US jury convicts Huawei of stealing trade secrets (AP)
  2. Nvidia's Jensen Huang says he is in therapy, a day after being
     reinstated as CEO, as shares slide (SCMP)
  3. Trump pardons the Thanksgiving turkeys at the White House (AP)
  4. Gunmen take 25 hostage at a supermarket in Colombia (AP)
  5. Saudi Arabia condemns a "terrorist attack" after the Riyadh PIF
     skyscraper is hit twice in a week (SCMP)
  6. Five women killed every hour by relatives in 2025, the UN says

## How it is built

`render.py` draws the front page with Pillow from the fonts on the
machine — every word is real text, nothing is baked into a generated
picture — and writes `entry.png`. `main.py` only validates that PNG
(1024×1024, whole file) and copies it to `/output/entry.png`
(`MAKEFUN_OUTPUT_DIR` outside the grader). Nothing talks to the
network, and both runs write the same bytes.

## Run it

```sh
python3 render.py          # rebuild entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
