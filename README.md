# Cotizador INS Medical · Seguros Digitales SDI

Cotizador para los 3 productos de INS Medical:

- **INS Medical Regional** — Cobertura CR y Centroamérica · Suma Asegurada $200,000
- **INS Medical Internacional** — Cobertura mundial · Suma Asegurada $2,000,000
- **Grandes Deducibles** — Cobertura mundial con prima reducida vía deducibles altos · Suma Asegurada $2,000,000

## Estructura

| Archivo | Propósito |
|---|---|
| `index.html` | Aplicación completa (HTML + CSS + JS inline). |
| `primas.js` | Tarifas oficiales INS vigentes desde 01/12/2025 (`window.PRIMAS`). |
| `mockups/` | Mockups visuales originales A (Institucional Azul) y B (Medical Modern → elegido). |
| `scripts/` | Utilidades Python: extracción de tarifas del XLSX oficial. |
| `docs/` | (Pendiente) PDFs del producto para descarga del cliente. |

## Stack

- **HTML / CSS / JS vanilla** — un solo archivo, sin build step.
- **Plus Jakarta Sans** + **JetBrains Mono** desde Google Fonts.
- **Google Identity Services** (OAuth 2.0) para autenticación del agente.
- **Gmail API** para envío de cotizaciones desde la cuenta del agente.
- **localStorage** para draft + historial de cotizaciones.
- **Netlify** para hosting (deploy automático desde `main`).

## Vistas

| URL | Vista | Quién la ve |
|---|---|---|
| `/` | Login → Agente | Agente autorizado (whitelist). |
| `/?c=BASE64` | Cliente | Quien recibe el link, sin necesidad de login. |

## Productos · Datos clave

Las tarifas vienen del XLSX **PRIMAS 2025 AMP EPID Y PAND Dic 25.xlsx** del INS, vigentes desde el 01/12/2025.

- 100 edades (0–99) × 2 géneros (F/M) × 2 variantes (Con/Sin Reducción).
- Regional/Internacional: 6 deducibles ($0, $200, $300, $400, $500, $1000).
- Grandes Deducibles: 3 deducibles ($5000, $10000, $15000).

## Smoke tests

`runSmokeTests()` se ejecuta al cargar y valida:

- PRIMAS completo (3 productos × 2 secciones × 100 edades × deducibles × géneros).
- Lookups conocidos contra el XLSX.
- Cálculo de prima familiar.
- Codificación/decodificación de payloads base64URL.
- Recargos de forma de pago.
- Disparadores de documentos por edad (66–70 telesuscripción, 71+ exámenes).

## Comandos

```bash
# Servir localmente
npx serve . -p 8801

# Regenerar tarifas desde XLSX
py scripts/extract_primas.py
py scripts/build_primas_js.py
```

## Registro SUGESE

P16-35-A01-113 — Vigente.
