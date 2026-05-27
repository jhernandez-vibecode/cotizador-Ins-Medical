"""Convierte primas_dump.json a primas.js (assignment a window) para inclusión directa."""
import json
from pathlib import Path

SRC = Path(r"C:\Users\segur\cotizador-Ins-Medical\scripts\primas_dump.json")
DST = Path(r"C:\Users\segur\cotizador-Ins-Medical\primas.js")

data = json.loads(SRC.read_text(encoding="utf-8"))

header = """// Tarifas INS Medical - vigentes desde 01/12/2025
// Fuente 1 (base): PRIMAS 2025 Dic 25.xlsx               (sin ampliación epidemias/pandemias)
// Fuente 2 (amp):  PRIMAS 2025 AMP EPID Y PAND Dic 25.xlsx (con ampliación epid/pand $200K)
// Generado por scripts/build_primas_js.py - NO EDITAR A MANO
// Estructura: PRIMAS[version][producto][seccion][edad][deducible][genero] = prima USD anual SIN IVA
//   version:    'base' | 'amp'   (base = sin ampliación, amp = con ampliación de epidemias)
//   producto:   'regional' | 'internacional' | 'grandes_deducibles'
//   seccion:    'con_reduccion' | 'sin_reduccion' (sin_reduccion aplica desde 70+ si JC elige)
//   edad:       '0' .. '99' (99 = "99 o más")
//   deducible:  REG/INT: '0'|'200'|'300'|'400'|'500'|'1000'
//               GD:      '5000'|'10000'|'15000'
//   genero:     'F' | 'M'
//
// IVA: las tarifas son SIN IVA. Para la prima final aplicar × 1.02 (IVA 2% seguros personas, Ley 9635).
"""

# Compact JSON (single line per age for readability of diffs)
out_lines = [header, "", "window.PRIMAS_VERSION = 'INS-MEDICAL-2025-12-01';", "", "window.PRIMAS_IVA = 0.02;  // IVA 2% (seguros de personas, Ley 9635 CR)", "", "window.PRIMAS = {"]
for vi, (ver_key, ver_data) in enumerate(data.items()):
    out_lines.append(f"  {json.dumps(ver_key)}: {{")
    for pi, (prod_key, prod_data) in enumerate(ver_data.items()):
        out_lines.append(f"    {json.dumps(prod_key)}: {{")
        for si, (sec_key, sec_data) in enumerate(prod_data.items()):
            out_lines.append(f"      {json.dumps(sec_key)}: {{")
            ages = sorted(sec_data.keys(), key=int)
            for ai, age in enumerate(ages):
                row = sec_data[age]
                row_compact = json.dumps(row, separators=(",", ":"), ensure_ascii=False)
                comma = "," if ai < len(ages) - 1 else ""
                out_lines.append(f"        {json.dumps(age)}: {row_compact}{comma}")
            comma = "," if si < len(prod_data) - 1 else ""
            out_lines.append(f"      }}{comma}")
        comma = "," if pi < len(ver_data) - 1 else ""
        out_lines.append(f"    }}{comma}")
    comma = "," if vi < len(data) - 1 else ""
    out_lines.append(f"  }}{comma}")
out_lines.append("};")
out_lines.append("")

DST.write_text("\n".join(out_lines), encoding="utf-8")
print(f"Escrito: {DST}")
print(f"Tamaño: {DST.stat().st_size:,} bytes  ({len(out_lines):,} líneas)")
