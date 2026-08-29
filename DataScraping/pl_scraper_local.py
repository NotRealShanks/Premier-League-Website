"""
LOCAL-FILE scraper for the (finished, static) 2025-26 Premier League season.
Instead of Python fetching pages from fbref (which Cloudflare blocks for any
automated tool -- requests, cloudscraper, Playwright, patchright, all of
them), YOU save the pages from your own normal browser, and this script just
parses the saved files. Cloudflare never sees anything automated this way.

This is a ONE-TIME pull, not something you need to re-run on a schedule --
the 2025-26 season is over and its stats won't change again. Once you've
loaded the resulting CSV into Supabase, you're done; there's no ongoing
automation needed for this data.

--- HOW TO USE ---

STEP 1: Save the league page
    1. In Chrome/Edge, go to:
           https://fbref.com/en/comps/9/2025-2026/2025-2026-Premier-League-Stats
    2. Press Ctrl+S, choose "Webpage, HTML Only", save it as exactly:
           league.html
       in the SAME FOLDER as this script.

STEP 2: Get the list of team pages to save
    Run:
        python pl_scraper_local.py links
    This reads league.html and prints the 20 team page URLs + the exact
    filename to save each one as. It also writes them to team_urls.txt.

STEP 3: Save each team page
    Open each URL printed in Step 2 in your browser, Ctrl+S -> "Webpage,
    HTML Only" -> save it with the exact filename shown, into a
    subfolder called "teams" (create that folder first).

STEP 4: Build the CSV
    Once all 20 files are saved in teams/, run:
        python pl_scraper_local.py build
    This produces player_stats_latest.csv, with columns already matching
    your Supabase player_stats table. Since this is a finished season, this
    table_data should already include real xG/xAG values -- no backfill
    script needed.

STEP 5: Load into Supabase
    Supabase dashboard -> Table Editor -> player_stats -> delete existing
    rows -> Insert -> Import data from CSV -> upload player_stats_latest.csv.

Only needs: pip install beautifulsoup4 pandas html5lib
"""

import sys
import os
from io import StringIO
from bs4 import BeautifulSoup, Comment
import pandas as pd

COLUMN_MAP = {
    "Player": "player_name",
    "Nation": "nation",
    "Pos": "position",
    "Age": "age",
    "MP": "matches_played",
    "Starts": "starts",
    "Min": "minutes_played",
    "Gls": "goals",
    "Ast": "assists",
    "PK": "penalties_scored",
    "CrdY": "yellow_cards",
    "CrdR": "red_cards",
    "xG": "expected_goals",
    "xAG": "expected_assists",
    "Team": "team_name",
}
FINAL_COLUMNS = list(COLUMN_MAP.values())


def _table_has_expected_cols(table):
    """Quick check: does this table's header row contain 'Gls' (goals)?
    That's a reliable signal it's the Standard Stats table and not
    Goalkeeping/Shooting/Passing/etc."""
    header_text = table.get_text()
    return "Gls" in header_text and ("xG" in header_text or "Player" in header_text)


def find_stats_table(soup, label):
    candidates = []
    tables = soup.find_all("table", class_="stats_table")
    candidates.extend(tables)
    comments = soup.find_all(string=lambda t: isinstance(t, Comment))
    for c in comments:
        csoup = BeautifulSoup(c, "html.parser")
        candidates.extend(csoup.find_all("table", class_="stats_table"))

    if not candidates:
        raise RuntimeError(f"No stats_table found in {label}. Did you save the full page (not just visible viewport)?")

    # Prefer a table whose id mentions 'standard' (fbref's standard-stats table id
    # is usually like 'stats_standard_9').
    for t in candidates:
        if "standard" in (t.get("id") or "").lower():
            return t
    # Otherwise, prefer one that actually has a Gls column (i.e. player stats,
    # not goalkeeping/misc tables).
    for t in candidates:
        if _table_has_expected_cols(t):
            return t
    # Fall back to the very first candidate, same as before.
    return candidates[0]


def cmd_links():
    if not os.path.exists("league.html"):
        print("league.html not found. See STEP 1 in the file header -- save the league page first.")
        return

    with open("league.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    table = find_stats_table(soup, "league.html")
    links = [a.get("href") for a in table.find_all("a")]
    links = [l for l in links if l and "/squads/" in l]
    # de-dupe while keeping order
    seen = set()
    team_urls = []
    for l in links:
        full = f"https://fbref.com{l}"
        if full not in seen:
            seen.add(full)
            team_urls.append(full)

    os.makedirs("teams", exist_ok=True)

    lines = []
    print(f"\nFound {len(team_urls)} teams. Open each URL, Ctrl+S -> HTML Only, save into teams/ with this filename:\n")
    for url in team_urls:
        team_name = url.split("/")[-1].replace("-Stats", "")
        filename = f"teams/{team_name}.html"
        print(f"  {url}\n    -> save as: {filename}\n")
        lines.append(f"{url}\t{filename}")

    with open("team_urls.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("(Also written to team_urls.txt for reference.)")


def cmd_cols(filename):
    if not os.path.exists(filename):
        print(f"{filename} not found.")
        return
    with open(filename, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Show ALL stats_table candidates, not just the first one, so we can see
    # which one is actually the "Standard Stats" table with xG/xAG in it.
    found_any = False
    for source_label, soup_to_use in [("visible DOM", soup)] + [
        (f"HTML comment #{i}", BeautifulSoup(c, "html.parser"))
        for i, c in enumerate(soup.find_all(string=lambda t: isinstance(t, Comment)))
    ]:
        tables = soup_to_use.find_all("table", class_="stats_table")
        for j, t in enumerate(tables):
            df = pd.read_html(StringIO(str(t)), flavor="html5lib")[0]
            if isinstance(df.columns, pd.MultiIndex):
                cols = list(df.columns.get_level_values(-1))
            else:
                cols = list(df.columns)
            table_id = t.get("id", "no-id")
            print(f"[{source_label}] table #{j} id={table_id} columns:\n  {cols}\n")
            found_any = True

    if not found_any:
        print("No stats_table elements found at all in this file.")


def cmd_build():
    if not os.path.exists("team_urls.txt"):
        print("team_urls.txt not found. Run 'python pl_scraper_local.py links' first.")
        return

    with open("team_urls.txt", encoding="utf-8") as f:
        entries = [line.split("\t") for line in f.read().splitlines() if line.strip()]

    all_teams = []
    missing = []

    for url, filename in entries:
        if not os.path.exists(filename):
            missing.append(filename)
            continue

        team_name = url.split("/")[-1].replace("-Stats", "")
        with open(filename, encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        stats = find_stats_table(soup, filename)
        team_data = pd.read_html(StringIO(str(stats)), flavor="html5lib")[0]

        if isinstance(team_data.columns, pd.MultiIndex):
            team_data.columns = team_data.columns.get_level_values(-1)

        # FBref's Standard Stats table repeats column names (Gls, Ast, G+A, G-PK)
        # for a "Per 90 Minutes" section later in the same table. Keep only the
        # FIRST occurrence of each name (the season-totals section).
        team_data = team_data.loc[:, ~team_data.columns.duplicated()]

        team_data["Team"] = team_name
        all_teams.append(team_data)
        print(f"  parsed {filename} ({len(team_data)} rows)")

    if missing:
        print(f"\nWARNING: {len(missing)} team file(s) not found, skipped:")
        for m in missing:
            print(f"  {m}")

    if not all_teams:
        print("No team files parsed -- nothing to write.")
        return

    stat_df = pd.concat(all_teams)
    stat_df = stat_df.rename(columns=COLUMN_MAP)

    missing = [c for c in FINAL_COLUMNS if c not in stat_df.columns]
    if missing:
        print(f"\nWARNING: these expected columns were not found in the parsed tables, filling with blank: {missing}")
        print("Run 'python pl_scraper_local.py cols teams/<SomeTeam>.html' to see what columns ARE present.")
        for c in missing:
            stat_df[c] = ""

    stat_df = stat_df[FINAL_COLUMNS]
    stat_df.to_csv("player_stats_latest.csv", index=False)
    print(f"\nDone. Wrote {len(stat_df)} rows to player_stats_latest.csv")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "cols":
        cmd_cols(sys.argv[2])
    elif len(sys.argv) != 2 or sys.argv[1] not in ("links", "build"):
        print("Usage:\n  python pl_scraper_local.py links          (after saving league.html)\n  python pl_scraper_local.py build          (after saving all team pages)\n  python pl_scraper_local.py cols teams/Arsenal.html   (debug: show columns found)")
    elif sys.argv[1] == "links":
        cmd_links()
    else:
        cmd_build()