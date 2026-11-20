#!/usr/bin/env python3
"""Detecta si el Pleno del Congreso está en vivo en YouTube y actualiza la página En vivo.

Lee la lista de transmisiones del canal oficial del Congreso, elige la transmisión EN VIVO cuyo título
contiene «Sesión del Pleno» y reemplaza EV_LIVE y EV_LIVE_T en build.py. No toca nada si no hay Pleno en vivo
o si no logra interpretar la página. Solo usa la biblioteca estándar.
"""
import json, re, sys, urllib.request
from pathlib import Path

CHANNEL = "UC9HLcODpEZuBRLSKXZx5igw"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
URL = f"https://www.youtube.com/channel/{CHANNEL}/streams"
BUILD = Path(__file__).resolve().parent.parent / "build.py"


def fetch():
    req = urllib.request.Request(URL, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept-Language": "es-PE,es;q=0.9",
        "Cookie": "CONSENT=YES+1; SOCS=CAI",
    })
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def streams(html):
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        return None
    data = json.loads(m.group(1))
    out = []

    def walk(o):
        if isinstance(o, list):
            for x in o:
                walk(x)
        elif isinstance(o, dict):
            v = o.get("lockupViewModel")
            if isinstance(v, dict) and v.get("contentId"):
                s = json.dumps(v, ensure_ascii=False)
                title = (((v.get("metadata") or {}).get("lockupMetadataViewModel") or {}).get("title") or {}).get("content", "")
                live = bool(re.search(r"watching|viendo", s, re.I))
                out.append((v["contentId"], title, live))
            for x in o.values():
                walk(x)

    walk(data)
    return out


def main():
    try:
        items = streams(fetch())
    except Exception as e:  # red, bloqueo, cambio de formato
        print("No se pudo leer YouTube:", e)
        return 0
    if not items:
        print("Sin resultados interpretables; no se cambia nada.")
        return 0
    pleno = [(i, t) for i, t, live in items if live and re.search(r"sesi[oó]n del pleno", t, re.I)]
    if not pleno:
        print("No hay Pleno en vivo ahora; no se cambia nada.")
        return 0
    vid, title = pleno[0]
    d = re.search(r"(\d{2})/(\d{2})/(\d{4})", title)
    fecha = f"{int(d.group(1))} de {MESES[int(d.group(2)) - 1]} de {d.group(3)}" if d else ""
    nuevo_t = "Sesión del Pleno del Congreso de la República" + (f", {fecha}" if fecha else "")
    src = BUILD.read_text(encoding="utf-8")
    m = re.search(r'EV_LIVE = "([\w-]{11})"', src)
    if not m:
        print("No se encontró EV_LIVE en build.py")
        return 0
    if m.group(1) == vid:
        print("Ya está actualizado:", vid)
        return 0
    src = re.sub(r'EV_LIVE = "[\w-]{11}"', f'EV_LIVE = "{vid}"', src, count=1)
    src = re.sub(r'EV_LIVE_T = ".*?"\n', lambda _: f'EV_LIVE_T = "{nuevo_t}"\n', src, count=1)
    BUILD.write_text(src, encoding="utf-8")
    print("Actualizado a", vid, "-", nuevo_t)
    return 0


if __name__ == "__main__":
    sys.exit(main())
