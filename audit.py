#!/usr/bin/env python3
"""Auditoría SEO técnica del sitio generado. Uso: python3 audit.py"""
import json
import os
import re
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {"vista-previa.html", "404.html"}
problems, warns = [], []

pages = {}
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".html") and f not in SKIP:
            rel = os.path.relpath(os.path.join(dp, f), ROOT)
            pages[rel] = open(os.path.join(dp, f), encoding="utf-8").read()

titles, descs = defaultdict(list), defaultdict(list)
links = defaultdict(set)

for rel, s in pages.items():
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', s, re.S)
    h1 = re.findall(r"<h1[ >]", s)
    if not t:
        problems.append((rel, "sin <title>"))
    else:
        tl = len(re.sub(r"&amp;|&quot;", "x", t.group(1)))
        if tl > 60:
            warns.append((rel, f"title de {tl} caracteres (>60)"))
        titles[t.group(1)].append(rel)
    if not d:
        problems.append((rel, "sin meta description"))
    else:
        dl = len(d.group(1))
        if dl > 160 or dl < 70:
            warns.append((rel, f"description de {dl} caracteres (ideal 70–160)"))
        descs[d.group(1)].append(rel)
    if len(h1) != 1:
        problems.append((rel, f"h1 = {len(h1)}"))
    if '<link rel="canonical"' not in s:
        problems.append((rel, "sin canonical"))
    if 'name="robots"' not in s:
        problems.append((rel, "sin meta robots"))
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(blk)
        except Exception as e:  # noqa: BLE001
            problems.append((rel, f"JSON-LD inválido: {e}"))
    for img in re.findall(r"<img [^>]*>", s):
        if "alt=" not in img:
            problems.append((rel, "imagen sin alt"))
    here = os.path.dirname(os.path.join(ROOT, rel))
    for h in re.findall(r'href="([^"]+)"', s):
        if re.match(r"(https?:|#|mailto:)", h) or h.endswith((".xml", ".css")):
            continue
        target = os.path.normpath(os.path.join(here, h.split("#")[0]))
        if not os.path.exists(target):
            problems.append((rel, f"enlace roto: {h}"))
        else:
            links[rel].add(os.path.relpath(target, ROOT))

for k, v in titles.items():
    if len(v) > 1:
        problems.append((", ".join(v), "title duplicado"))
for k, v in descs.items():
    if len(v) > 1:
        problems.append((", ".join(v), "description duplicada"))

# Huérfanas y profundidad de clics desde el inicio
inbound = defaultdict(int)
for src, tg in links.items():
    for t in tg:
        if t != src:
            inbound[t] += 1
for rel in pages:
    if rel != "index.html" and inbound[rel] == 0:
        problems.append((rel, "página huérfana (nadie enlaza a ella)"))
dist = {"index.html": 0}
q = deque(["index.html"])
while q:
    cur = q.popleft()
    for n in links.get(cur, ()):
        if n in pages and n not in dist:
            dist[n] = dist[cur] + 1
            q.append(n)
for rel in pages:
    if rel not in dist:
        problems.append((rel, "inalcanzable desde el inicio"))
    elif dist[rel] > 3:
        warns.append((rel, f"a {dist[rel]} clics del inicio (ideal ≤3)"))

# Sitemap vs. páginas indexables
sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
locs = set(re.findall(r"<loc>(.*?)</loc>", sm))
for rel, s in pages.items():
    can = re.search(r'<link rel="canonical" href="(.*?)">', s).group(1)
    noidx = "noindex" in s
    if "noindex" not in s and can not in locs:
        problems.append((rel, "indexable pero falta en sitemap"))
    if re.search(r'content="noindex, follow"', s) and can in locs:
        problems.append((rel, "noindex pero aparece en sitemap"))

draft = all("noindex" in s for s in pages.values())
print(f"Páginas auditadas: {len(pages)} | URLs en sitemap: {len(locs)} | modo borrador (todo noindex): {draft}")
print(f"Clics máximos desde el inicio: {max(dist.values())}")
for r, m in warns:
    print(f"  AVISO  {r}: {m}")
for r, m in problems:
    print(f"  ERROR  {r}: {m}")
print("RESULTADO:", "sin errores" if not problems else f"{len(problems)} error(es)")
sys.exit(1 if problems else 0)
