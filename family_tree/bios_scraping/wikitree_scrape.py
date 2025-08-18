import argparse
import re
import time
from pathlib import Path

import pandas as pd
import requests

API = "https://api.wikitree.com/api.php"
APP_ID = "Scraper"
TIMEOUT = 30
SLEEP_BETWEEN_CALLS = 0.5
CHECKPOINT_EVERY = 200

WT_FIELDS = ",".join([
    "Id","Name","FirstName","MiddleName","LastNameAtBirth","LastNameCurrent",
    "Prefix","Suffix","ShortName","Gender",
    "BirthDate","BirthLocation","DeathDate","DeathLocation",
    "Derived.BirthName","Derived.LongName","Manager","Privacy",
    "DataStatus","Created","LastModified","IsLiving","IsPerson","Photo",
    "Mother","Father","Categories","Bio"
])

MONTHS = {
    "01":"January","02":"February","03":"March","04":"April","05":"May","06":"June",
    "07":"July","08":"August","09":"September","10":"October","11":"November","12":"December"
}

def api_get_profile(session, key):
    params = {
        "action": "getProfile",
        "key": str(key),
        "fields": WT_FIELDS,
        "bioFormat": "wiki",
        "appId": APP_ID,
    }
    r = session.get(API, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if not data or "profile" not in data[0]:
        return None
    return data[0]["profile"]

def year_from_date(d):
    if not isinstance(d, str) or len(d) < 4:
        return None
    y = d[:4]
    return int(y) if y.isdigit() else None

def format_date(d):
    if not isinstance(d, str) or len(d) < 4:
        return None
    y = d[:4] if d[:4].isdigit() else None
    m = d[5:7] if len(d) >= 7 else None
    day = d[8:10] if len(d) >= 10 else None
    if y and m and m != "00" and day and day != "00":
        mn = MONTHS.get(m, m)
        try:
            di = int(day)
            return f"{mn} {di}, {y}"
        except ValueError:
            return f"{mn} {day}, {y}"
    if y and m and m != "00":
        mn = MONTHS.get(m, m)
        return f"{mn} {y}"
    if y:
        return y
    return None

def wikitext_to_text(wiki):
    if not wiki:
        return ""
    text = wiki
    text = re.sub(r"<ref[^>/]*?>.*?</ref>", " ", text, flags=re.I|re.S)
    text = re.sub(r"<ref[^>]*/>", " ", text, flags=re.I)
    text = re.sub(r"\{\{.*?\}\}", " ", text, flags=re.S)
    text = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[https?://[^\s\]]+\s+([^\]]+)\]", r"\1", text)
    text = re.sub(r"^\s*=+[^=]+?=+\s*$", " ", text, flags=re.M)
    text = re.sub(r"\[\[Category:[^\]]+\]\]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def name_from_profile(p):
    return p.get("Derived.LongName") or p.get("ShortName") or p.get("Name") or ""

def basic_parent_line(session, cache, pid):
    if not pid:
        return (None, "")
    if pid in cache:
        pp = cache[pid]
    else:
        try:
            pp = api_get_profile(session, pid)
        except Exception:
            pp = None
        cache[pid] = pp
    if not pp:
        return (None, "")
    nm = name_from_profile(pp)
    by = year_from_date(pp.get("BirthDate"))
    dy = year_from_date(pp.get("DeathDate"))
    if by and dy:
        yrs = f"{by}–{dy}"
    elif by:
        yrs = f"{by}–"
    elif dy:
        yrs = f"–{dy}"
    else:
        yrs = ""
    return (nm, yrs)

def extract_extra_sentences(bio_text, pronoun="They"):
    t = bio_text.lower()
    out = []

    war_phrases = [
        "old french war", "french and indian war",
        "revolutionary war", "american revolution", "war of 1812",
        "militia", "captain", "lieutenant", "colonel", "ensign"
    ]
    hits = [w for w in war_phrases if w in t]
    if hits:
        phrase = "Old French War" if "old french war" in hits else (
            "French and Indian War" if "french and indian war" in hits else (
                "the American Revolution" if "revolutionary war" in hits or "american revolution" in hits else "militia service"
            )
        )
        out.append(f"{pronoun} served in {phrase}.")

    if "unmarried" in t or "never married" in t:
        out.append(f"{pronoun} died unmarried.")

    m_made = re.search(r"will (?:was )?made\s+([A-Za-z0-9 ,]+)", bio_text, flags=re.I)
    m_proved = re.search(r"proved\s+([A-Za-z0-9 ,]+)", bio_text, flags=re.I)
    if m_made or m_proved:
        if m_made and m_proved:
            out.append(f"Their will was made {m_made.group(1).strip()}, proved {m_proved.group(1).strip()}.")
        elif m_made:
            out.append(f"Their will was made {m_made.group(1).strip()}.")
        else:
            out.append(f"Their will was proved {m_proved.group(1).strip()}.")

    return out

def build_narrative(p, father, mother):
    gender = (p.get("Gender") or "").lower()
    subj = "He" if gender == "male" else ("She" if gender == "female" else "They")
    child_of = "son of" if gender == "male" else ("daughter of" if gender == "female" else "child of")

    name = name_from_profile(p)
    bdate = format_date(p.get("BirthDate"))
    bplace = p.get("BirthLocation")
    ddate = format_date(p.get("DeathDate"))
    dplace = p.get("DeathLocation")
    f_name, f_years = father if father else (None, "")
    m_name, m_years = mother if mother else (None, "")
    parts = []
    parts.append(f"{name} was born" + (f" on {bdate}" if bdate else "") + (f" in {bplace}" if bplace else "") + ".")
    if f_name and m_name:
        parts.append(f"{subj} was {child_of} {f_name} ({f_years}) and {m_name} ({m_years}).")
    elif f_name or m_name:
        who = f_name if f_name else m_name
        yrs = f_years if f_name else m_years
        parts.append(f"{subj} was the {child_of} {who}" + (f" ({yrs})" if yrs else "") + ".")

    if ddate or dplace:
        by = year_from_date(p.get("BirthDate"))
        dy = year_from_date(p.get("DeathDate"))
        age_str = ""
        if by and dy and dy >= by:
            age_str = f", aged {dy - by} years"
        parts.append(f"{subj} died" + (f" in {ddate}" if ddate and not dplace else (f" on {ddate}" if ddate else "")) +
                     (f" in {dplace}" if dplace else "") + (age_str if age_str else "") + ".")

    bio_text = wikitext_to_text(p.get("Bio"))
    extras = extract_extra_sentences(bio_text, pronoun=subj)
    parts.extend(extras)
    sent = " ".join(s.strip() for s in parts if s and s.strip())
    return sent

def fit_score(row, prof):
    score = 0
    birth_hint = row.get("birth_year")
    try:
        birth_hint = int(birth_hint)
    except Exception:
        birth_hint = None
    lo = row.get("range_lo"); hi = row.get("range_hi")
    try:
        lo = int(lo); hi = int(hi)
    except Exception:
        lo = hi = None
    p_by = year_from_date(prof.get("BirthDate"))

    if p_by:
        if birth_hint:
            diff = abs(p_by - birth_hint)
            score += max(0, 10 - min(diff, 10))
        elif lo and hi:
            score += 8 if (lo <= p_by <= hi) else 0

    state = str(row.get("state") or "")
    if state:
        for loc_field, weight in (("BirthLocation", 3), ("DeathLocation", 2)):
            loc = (prof.get(loc_field) or "").lower()
            if state.lower() in loc:
                score += weight
    return score

def main(inp, out, limit=None, checkpoint=None):
    df = pd.read_csv(inp)
    required = ["query_name","state","range_lo","range_hi","profile_key"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"Input is missing columns: {missing}")

    if limit is not None and limit > 0:
        df = df.head(limit).copy()

    rows = []
    cache = {}
    done_pairs = set()

    if checkpoint and Path(checkpoint).exists():
        prev = pd.read_csv(checkpoint)
        rows = prev.to_dict(orient="records")
        done_pairs = {(r.get("profile_key"), r.get("query_name")) for r in rows}

    with requests.Session() as s:
        processed = 0
        for _, row in df.iterrows():
            key = row.get("profile_key")
            qname = row.get("query_name")
            if pd.isna(key):
                continue
            if (key, qname) in done_pairs:
                continue

            rec = {
                "query_name": qname,
                "profile_key": key,
                "state": row.get("state"),
                "range_lo": row.get("range_lo"),
                "range_hi": row.get("range_hi"),
                "birth_year_hint": row.get("birth_year") if "birth_year" in df.columns else None,
                "birth_place_hint": row.get("birth_place") if "birth_place" in df.columns else None,
                "source_url": f"https://www.wikitree.com/wiki/{key}",
                "narrative": None,
                "fit_score": None,
                "status": "NOT_FOUND",
                "error": None
            }

            try:
                p = api_get_profile(s, key)
            except Exception as e:
                rec["error"] = str(e)
                p = None

            if p:
                f = m = None
                try:
                    f = basic_parent_line(s, cache, p.get("Father")) if p.get("Father") else None
                except Exception:
                    f = None
                try:
                    m = basic_parent_line(s, cache, p.get("Mother")) if p.get("Mother") else None
                except Exception:
                    m = None

                try:
                    rec["narrative"] = build_narrative(p, f, m)
                except Exception:
                    rec["narrative"] = None

                try:
                    rec["fit_score"] = fit_score(row, p)
                except Exception:
                    rec["fit_score"] = None

                rec["status"] = "OK"

            rows.append(rec)
            processed += 1

            if processed % 25 == 0:
                print(f"Processed {processed} rows ...")
            if checkpoint and processed % CHECKPOINT_EVERY == 0:
                pd.DataFrame(rows).to_csv(checkpoint, index=False)
                print(f"Checkpoint saved to {checkpoint}")

            time.sleep(SLEEP_BETWEEN_CALLS)

    out_df = pd.DataFrame(rows)
    out_df["group_rank"] = (
        out_df.sort_values(["query_name","fit_score"], ascending=[True, False])
              .groupby("query_name")
              .cumcount() + 1
    )
    out_df.to_csv(out, index=False)
    print(f"Wrote {len(out_df)} rows to {out}")
    print("Sample narrative:\n", (out_df["narrative"].dropna().head(1).tolist() or ["<none>"])[0])

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Produce narrative bios from WikiTree profile keys.")
    ap.add_argument("input_csv", help="task_1.csv (must have: query_name,state,range_lo,range_hi,profile_key)")
    ap.add_argument("output_csv", help="Output CSV path with narrative text")
    ap.add_argument("--limit", type=int, default=100, help="First N rows to process (0 = all)")
    ap.add_argument("--checkpoint", default=None, help="Optional checkpoint CSV for long runs")
    args = ap.parse_args()
    lim = None if args.limit is None else (None if args.limit == 0 else args.limit)
    main(args.input_csv, args.output_csv, limit=lim, checkpoint=args.checkpoint)
