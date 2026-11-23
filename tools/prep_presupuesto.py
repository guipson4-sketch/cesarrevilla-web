#!/usr/bin/env python3
"""Convierte el Excel «Presupuesto 2027 <Región> por nivel y pliego» en data/presupuesto-2027-<region>.json.
Uso: python3 tools/prep_presupuesto.py <region-slug> <ruta.xlsx>   (ej. puno datos/Presupuesto_2027_Puno_por_Nivel_y_Pliego.xlsx)"""
import json
import os
import re
import sys

import openpyxl

SMALL = {"de", "del", "la", "las", "el", "los", "y", "en", "a", "para", "por", "con", "al", "e", "o", "u"}
KEEP = {"PNP", "IE", "I.E.", "EBR", "MINSA", "SENAMHI", "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "UGEL", "EE.SS.",
        "INPE", "ANA", "PELT", "SERNANP", "DIRESA", "RIS", "CAS", "CUI", "N°", "UNA", "UNAJ", "UNAP", "PRONIED", "I.E.P."}


def tc(s):
    if not s:
        return ""
    out = []
    for i, w in enumerate(re.split(r"(\s+)", s.strip())):
        if not w.strip():
            out.append(w)
            continue
        if w.upper() in KEEP:
            out.append(w.upper())
        elif i > 0 and w.lower() in SMALL:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:].lower())
    return "".join(out)


def main(region, xlsx):
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    det = [r for r in wb[[n for n in wb.sheetnames if n.startswith("Detalle")][0]].iter_rows(min_row=6, values_only=True) if r[0]]
    rows = []
    for r in det:
        prov = r[9] if r[9] and not str(r[9]).startswith("Ámbito") else "Ámbito regional o no precisado"
        fu = str(r[13] or "")
        fu = ("Anexo " + fu.replace("ANEXO ", "") + (f", pág. {r[14]}" if r[14] else "")) if fu.upper().startswith("ANEXO") else fu
        rows.append(dict(n=r[0], p=tc(re.sub(r"^\d+\s+", "", str(r[3]))), c=str(r[6]), i=tc(r[7]), pr=prov, d=r[10] or "", m=int(r[12]),
                         a=fu, inf=str(r[16] or "").startswith("Inferencia")))
    multi = []
    for r in wb["Multidepartamentales"].iter_rows(min_row=6, values_only=True):
        if r[0]:
            multi.append(dict(n=r[0], p=tc(re.sub(r"^\d+\s+", "", str(r[3]))), c=str(r[5]), i=tc(r[6]), m=int(r[8]), a=(r[9] or "").replace("ANEXO ", "")))
    res = {}
    for r in wb["Resumen"].iter_rows(values_only=True):
        if r[0] in ("Gobierno Nacional", "Gobierno Regional", "Gobierno Local") and isinstance(r[1], int):
            res[r[0]] = dict(n=r[1], m=int(r[2]))
    json.dump(dict(region=region, resumen=res, multi=multi, rows=rows), open(f"data/presupuesto-2027-{region}.json", "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    tot = sum(x["m"] for x in rows)
    assert tot == sum(v["m"] for v in res.values()), (tot, res)
    print(len(rows), tot)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
