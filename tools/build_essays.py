"""Build the essay pages from the Obsidian vault.

Reads every note in vault/Essays/. A note is published only if its front
matter says `publish: true`; everything else is a draft and is skipped.
Writes essays/<slug>.html for each published note and essays/index.html,
and copies any images the notes embed into essays/media/.

Run from the repository root:  python tools/build_essays.py
"""
from __future__ import annotations

import datetime as dt
import html
import re
import shutil
import sys
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
ESSAYS_IN = VAULT / "Essays"
ATTACH = VAULT / "Attachments"
OUT = ROOT / "essays"
MEDIA = OUT / "media"

AUTHOR = "Rehan Krishnan"
EMAIL = "rkrish23@jh.edu"


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "essay"


def split_front_matter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        parts = text.split("\n---", 1)
        if len(parts) == 2:
            meta = yaml.safe_load(parts[0][3:]) or {}
            body = parts[1].lstrip("\n")
            if not isinstance(meta, dict):
                raise ValueError("front matter must be a set of key: value lines")
            return meta, body
    return {}, text


def as_date(value) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str) and value.strip():
        return dt.date.fromisoformat(value.strip())
    return None


def obsidian_to_markdown(body: str, slugs: dict[str, str], used_media: set[str]) -> str:
    """Turn Obsidian-only syntax into plain Markdown."""
    # ![[image.png]] or ![[image.png|alt]]  -> image from the Attachments folder
    def embed(m: re.Match) -> str:
        target, _, alt = m.group(1).partition("|")
        name = Path(target.strip()).name
        used_media.add(name)
        return f"![{alt.strip() or ''}](media/{name})"

    body = re.sub(r"!\[\[([^\]]+)\]\]", embed, body)

    # ![alt](file.svg): a standard Markdown image pointing at a file in Attachments
    def md_image(m: re.Match) -> str:
        alt, target = m.group(1), m.group(2).strip()
        if re.match(r"^[a-z]+://", target) or target.startswith("/"):
            return m.group(0)                      # web images are left as they are
        name = Path(target.split("#")[0]).name
        used_media.add(name)
        return f"![{alt}](media/{name})"

    body = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", md_image, body)

    # [[Other essay]] or [[Other essay|label]] -> link if it is published, else plain text
    def wikilink(m: re.Match) -> str:
        target, _, label = m.group(1).partition("|")
        target = target.split("#")[0].strip()
        label = (label or target).strip()
        slug = slugs.get(target.lower())
        return f"[{label}]({slug}.html)" if slug else label

    body = re.sub(r"(?<!!)\[\[([^\]]+)\]\]", wikilink, body)
    # %% Obsidian comments %% are private notes: drop them
    body = re.sub(r"%%.*?%%", "", body, flags=re.S)
    return drop_empty_sections(body)


def drop_empty_sections(body: str) -> str:
    """Leave out a ## or ### heading that has nothing written under it yet.

    A section that only holds %% prompts %% (already removed) is a slot still
    to be written, so it stays off the site until there is text in it.
    Footnote definitions do not count as text, and are always kept.
    """
    lines = body.split("\n")
    keep = [True] * len(lines)
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,3})\s", line)
        if not m:
            continue
        level, has_text = len(m.group(1)), False
        for nxt in lines[i + 1:]:
            h = re.match(r"^(#{1,6})\s", nxt)
            if h and len(h.group(1)) <= level:
                break
            if nxt.strip() and not re.match(r"^\[\^[^\]]+\]:", nxt):
                has_text = True
                break
        keep[i] = has_text
    return "\n".join(l for l, k in zip(lines, keep) if k)


STYLE = """
@font-face{font-family:"CMU Serif";font-style:normal;font-weight:500;src:url("../assets/fonts/cmu-serif-500-roman.woff2") format("woff2")}
@font-face{font-family:"CMU Serif";font-style:italic;font-weight:500;src:url("../assets/fonts/cmu-serif-500-italic.woff2") format("woff2")}
@font-face{font-family:"CMU Serif";font-style:normal;font-weight:700;src:url("../assets/fonts/cmu-serif-700-roman.woff2") format("woff2")}
@font-face{font-family:"CMU Serif";font-style:italic;font-weight:700;src:url("../assets/fonts/cmu-serif-700-italic.woff2") format("woff2")}
:root{--paper:#FCFCF9;--ink:#141517;--grey:#6B6E73;--faint:#D9DAD6;--accent:#9E2A2B}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#15161A;--ink:#E9E7E1;--grey:#9A9CA1;--faint:#33353B;--accent:#E07A6B}}
:root[data-theme="dark"]{--paper:#15161A;--ink:#E9E7E1;--grey:#9A9CA1;--faint:#33353B;--accent:#E07A6B}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:500 19px/1.6 "CMU Serif","Latin Modern Roman","Computer Modern",Georgia,serif;font-kerning:normal}
a{color:inherit;text-decoration:none;border-bottom:1px solid var(--faint)}
a:hover{border-bottom-color:var(--ink)}
main{max-width:700px;margin:0 auto;padding:28px 24px 48px}
.back{font-size:15px;font-style:italic;color:var(--grey);border:0}
.back:hover{color:var(--ink)}
h1{font-size:34px;line-height:1.15;margin:34px 0 6px;font-weight:700;text-align:center}
.sub{text-align:center;font-style:italic;font-size:19px;margin:0 0 6px}
.by{text-align:center;color:var(--grey);font-size:16px;margin:0 0 30px}
.abstract{font-size:17px;margin:0 auto 30px;max-width:600px}
.abstract b{font-variant:small-caps;letter-spacing:.5px}
.body{counter-reset:sec}
.body h2{font-size:21px;margin:36px 0 10px;font-weight:700}
.body h2::before{counter-increment:sec;content:counter(sec);margin-right:12px}
.body h3{font-size:18px;margin:26px 0 8px;font-weight:700}
p{margin:0 0 14px;text-align:justify;hyphens:auto}
blockquote{margin:16px 0;padding:0 0 0 18px;border-left:2px solid var(--faint);color:var(--grey)}
img{max-width:100%;height:auto;display:block;margin:18px auto}
code{font-size:.9em}
hr{border:0;border-top:1px solid var(--faint);margin:28px 0}
sup a, .footnote-ref{border:0;color:var(--accent);font-size:13px;padding:0 1px}
.footnote{margin-top:40px}
.footnote::before{content:"References";display:block;font-weight:700;font-size:21px;margin:0 0 12px}
.footnote hr{display:none}
.footnote ol{padding-left:26px;margin:0}
.footnote li{font-size:15.5px;line-height:1.45;margin:0 0 10px;padding-left:6px}
.footnote li p{text-align:left;margin:0}
.footnote-backref{border:0;color:var(--grey);margin-left:4px}
.footnote li:target{background:var(--faint)}
.note{font-size:15px;color:var(--grey);border-top:1px solid var(--faint);margin-top:36px;padding-top:12px}
.list{list-style:none;padding:0;margin:24px 0 0}
.list li{margin:0 0 22px}
.list .t{font-size:21px;font-weight:700}
.list .m{color:var(--grey);font-size:15px}
.list .s{font-style:italic;margin-top:2px}
@media (max-width:640px){body{font-size:17px}main{padding:18px 16px 36px}h1{font-size:27px}.sub{font-size:17px}p{text-align:left}}
"""


def page(title: str, description: str, inner: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<link rel="preload" href="../assets/fonts/cmu-serif-500-roman.woff2" as="font" type="font/woff2" crossorigin>
<style>{STYLE}</style>
</head>
<body>
<main>
{inner}
</main>
</body>
</html>
"""


def build() -> int:
    if not ESSAYS_IN.is_dir():
        print(f"no folder {ESSAYS_IN}", file=sys.stderr)
        return 1
    notes = []
    for path in sorted(ESSAYS_IN.glob("*.md")):
        meta, body = split_front_matter(path.read_text(encoding="utf-8"))
        title = str(meta.get("title") or path.stem)
        notes.append({"path": path, "meta": meta, "body": body, "title": title,
                      "slug": slugify(str(meta.get("slug") or title))})

    published = [n for n in notes if meta_true(n["meta"].get("publish"))]
    slugs = {}
    for n in published:
        slugs[n["path"].stem.lower()] = n["slug"]
        slugs[n["title"].lower()] = n["slug"]
    seen = {}
    for n in published:
        if n["slug"] in seen:
            raise SystemExit(f'two published essays share the slug "{n["slug"]}": '
                             f'{seen[n["slug"]]} and {n["path"].name}; set a different `slug:` in one')
        seen[n["slug"]] = n["path"].name

    # Start clean so an essay that is unpublished or deleted also leaves the site.
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    used_media: set[str] = set()
    for n in published:
        meta = n["meta"]
        md = markdown.Markdown(extensions=["footnotes", "tables", "fenced_code", "sane_lists", "smarty"],
                               extension_configs={"footnotes": {"BACKLINK_TEXT": "↩"}})
        body_html = md.convert(obsidian_to_markdown(n["body"], slugs, used_media))
        date = as_date(meta.get("date"))
        n["date"] = date
        bits = [f'<a class="back" href="./">← Essays</a> &nbsp; <a class="back" href="../">Rehan Krishnan</a>',
                f'<h1>{html.escape(n["title"])}</h1>']
        if meta.get("subtitle"):
            bits.append(f'<p class="sub">{html.escape(str(meta["subtitle"]))}</p>')
        by = AUTHOR + (f" · {date:%B %Y}" if date else "")
        bits.append(f'<p class="by">{by}</p>')
        if meta.get("abstract"):
            bits.append(f'<p class="abstract"><b>Abstract.</b> {html.escape(str(meta["abstract"]).strip())}</p>')
        bits.append(f'<div class="body">{body_html}</div>')
        bits.append(f'<p class="note">Questions, corrections or disagreements are welcome: '
                    f'<a href="mailto:{EMAIL}">{EMAIL}</a>.</p>')
        desc = str(meta.get("description") or meta.get("subtitle") or n["title"])
        (OUT / f'{n["slug"]}.html').write_text(page(n["title"], f"{desc} An essay by {AUTHOR}.", "\n".join(bits)),
                                               encoding="utf-8")
        print(f'published  {n["path"].name}  ->  essays/{n["slug"]}.html')

    for n in notes:
        if n not in published:
            print(f'draft      {n["path"].name}  (add `publish: true` to publish it)')

    missing = []
    if used_media:
        MEDIA.mkdir(exist_ok=True)
        for name in sorted(used_media):
            src = ATTACH / name
            if src.is_file():
                shutil.copy2(src, MEDIA / name)
            else:
                missing.append(name)
    if missing:
        raise SystemExit("embedded images not found in vault/Attachments: " + ", ".join(missing))

    published.sort(key=lambda n: (n["date"] or dt.date.min, n["title"]), reverse=True)
    items = []
    for n in published:
        when = f'{n["date"]:%B %Y}' if n["date"] else ""
        sub = n["meta"].get("subtitle")
        items.append(f'<li><a class="t" href="{n["slug"]}.html">{html.escape(n["title"])}</a>'
                     + (f'<div class="s">{html.escape(str(sub))}</div>' if sub else "")
                     + (f'<div class="m">{when}</div>' if when else "") + "</li>")
    listing = "<ul class=\"list\">" + "".join(items) + "</ul>" if items else \
        '<p class="by">No essays are published yet.</p>'
    (OUT / "index.html").write_text(page(f"Essays · {AUTHOR}", f"Essays by {AUTHOR}.",
                                         f'<a class="back" href="../">← Rehan Krishnan</a>\n<h1>Essays</h1>\n{listing}'),
                                    encoding="utf-8")
    print(f"{len(published)} published, {len(notes) - len(published)} drafts")
    return 0


def meta_true(value) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() in {"true", "yes"})


if __name__ == "__main__":
    sys.exit(build())
