---
name: especialista-cotizador-ins-medical
description: ESPECIALISTA COTIZADOR INS MEDICAL — Cotizador de seguro de gastos médicos INS Medical del INS (SUGESE P16-35-A01-113), bajo marca Seguros Digitales SDI. Single-file HTML/CSS/JS vanilla en Netlify desde repo jhernandez-vibecode/cotizador-Ins-Medical. EN PROD en insmedical.appsegurosdigitales.com. Auth Google con whitelist AGENTES, envío de correos vía Gmail API directo (mismo Client ID que Cotizador Autos SDI y Vital 360). 3 productos: INS Medical Regional ($200K), INS Medical Internacional ($2M) y Grandes Deducibles ($2M con ded $5K/$10K/$15K). Tarifas oficiales INS Dic 2025 en 2 versiones (base sin AMP / amp con ampliación epidemias y pandemias) × 100 edades (0-99) × F/M × 2 secciones (Con/Sin Reducción a partir de 70 años). IVA 2% (Ley 9635) aplicado a todas las primas mostradas — cuadre bit-for-bit verificado con cotizador oficial INS. Toggle Ampliar epidemias/pandemias por cotización. Toggle Sin Reducción de Suma Asegurada auto-mostrado si hay asegurado ≥70. Coberturas con tooltips de Condiciones Generales. Historial localStorage. Plantilla de correo HTML con logo INS + 1-3 product cards + CTA al link cliente. Usar este skill cuando JC pida cualquier cambio o mejora al proyecto Cotizador INS Medical.
---

# Especialista Cotizador INS Medical

Contexto completo del proyecto para retomar trabajo sin perder contexto. Leer COMPLETO antes de tocar código.

## Qué es

Cotizador online del **Seguro INS Medical** del INS (gastos médicos), operado por Seguros Digitales SDI bajo whitelist Google. Producto registrado bajo norma **SUGESE P16-35-A01-113**. La aplicación cubre el ciclo agente → cliente:

1. **Vista agente** (con auth): cotiza los 3 productos (Regional, Internacional, Grandes Deducibles), selecciona deducible por producto, marca recomendado, envía al cliente por email/WhatsApp/link.
2. **Vista cliente** (stateless, vía link `?c=BASE64URL`): hero con logo INS, price cards de productos cotizados, tabla comparativa con tooltips, opciones de pago, períodos de espera, documentos de emisión, material informativo, CTA WhatsApp, footer SDI.

## Estado actual (27 jul 2026)

- **EN PROD:** [insmedical.appsegurosdigitales.com](https://insmedical.appsegurosdigitales.com) (auto-deploy desde `main`)
- **URL Netlify:** [cotizador-ins-medical.netlify.app](https://cotizador-ins-medical.netlify.app)
- **Repo:** [jhernandez-vibecode/cotizador-Ins-Medical](https://github.com/jhernandez-vibecode/cotizador-Ins-Medical)
- **Repo local:** `C:/Users/segur/cotizador-Ins-Medical`
- **Preview local:** `npx serve` puerto 8801 — nombre `cotizador-insmedical` en `~/.claude/launch.json`
- **Versión:** v1.0.0 commit inicial `4187324`
- **24 jun 2026 (commit `080837d`):** correo de póliza emitida con **adjuntos** (botón "Agregar documentos", hasta 20 MB) + **firma sin círculo de iniciales** en ambas plantillas. Ver sección "Plantilla de correo HTML".
- **jun 2026 (commit `698c444`):** fix adjuntos — se descartó el endpoint de subida por CORS y quedó el clásico + correo del cliente editable. Ver "Plantilla de correo HTML".
- **16 jul 2026 (commit `51d6240`, último):** respaldo del historial — exportar / importar JSON. `main` sincronizada con origin.

## Stack

- **HTML + CSS + JS vanilla single-file** (`index.html`, ~2700 líneas)
- **Sin frameworks, sin build step, sin Node, sin npm**
- **Google Identity Services (GIS)** — mismo Client ID compartido con Cotizador Autos SDI y Vital 360: `255791314248-apgnrs0tiii72ogau5dpsjm2eie6d2hu.apps.googleusercontent.com` (vive en proyecto Google Cloud "Cotizador Autos SDI")
- **Gmail API directo** desde el browser para envío de correos (scope `gmail.send`)
- **localStorage** para borrador (`insmedical.borrador.<email>`) + historial (`insmedical.historial.<email>`) namespaced por agente
- **Tipografía:** Plus Jakarta Sans (UI, todas las fuentes) · JetBrains Mono (números/primas)
- **Paleta:** Azul navy/electric INS Medical + emerald green para Grandes Deducibles + soft sky blue para Regional
  - Internacional (default blue): `--blue #2563EB`, `--blue-dark #1E3A8A`
  - Regional (azul tenue diferenciado): `--reg #5B91D0`, `--reg-dark #2E6FA8`
  - Grandes Deducibles (verde): `--green #059669`, `--green-dark #047857`

## Modelo de datos

Tarifas oficiales INS vigentes desde 01/12/2025, extraídas de 2 XLSX:
- `PRIMAS 2025 Dic 25.xlsx` — versión BASE (sin ampliación de epidemias)
- `PRIMAS 2025 AMP EPID Y PAND Dic 25.xlsx` — versión AMP (con ampliación a $75K Regional / $200K Internacional y GD)

Estructura del objeto `window.PRIMAS` en `primas.js`:

```
PRIMAS[version][producto][seccion][edad][deducible][genero] = prima_USD_anual_sin_IVA
```

Donde:
- `version`: `'base'` | `'amp'`
- `producto`: `'regional'` | `'internacional'` | `'grandes_deducibles'`
- `seccion`: `'con_reduccion'` | `'sin_reduccion'` (la segunda se aplica a partir de los 70 años si el agente la elige)
- `edad`: `'0'` .. `'99'` (99 = "99 o más")
- `deducible` (REG/INT): `'0'`, `'200'`, `'300'`, `'400'`, `'500'`, `'1000'`
- `deducible` (GD): `'5000'`, `'10000'`, `'15000'`
- `genero`: `'F'` | `'M'`

**IVA 2 %** (`window.PRIMAS_IVA = 0.02`, Ley 9635 seguros de personas en CR) se aplica automáticamente en `primaConIVA(primaSinIVA)`. Las primas mostradas SIEMPRE son CON IVA — son lo que el cliente paga.

### Constantes en index.html

- `PRODUCTOS` — catálogo con `nombre`, `tagline`, `suma_asegurada`, `deducibles[]`, `deducible_default`, `color_class`
- `PRODUCTOS_ORDER` — orden de presentación: `['regional', 'internacional', 'grandes_deducibles']`
- `DEDUCIBLE_LABELS` — etiquetas legibles
- `FORMAS_PAGO` — anual 0% (recomendado), semestral 5%, trimestral 7%. SIN mensual (decisión de oficina alineada con Vital 360)
- `COBERTURAS_SECCIONES` — 4 secciones, ~22 ítems totales con `label`, `desc` (tooltip), `val(prod, ded, payload)`
- `PERIODOS_ESPERA_COLS` — 3 columnas (General, Condiciones 10m, Condiciones 10m cont.) según Condiciones Particulares INS Medical V13
- `DOCS_BASE` — 4 documentos para emisión (Solicitud, Declaración de Salud, Autorización, Solic Beneficios)
- `DOCS_INFO` — 8 PDFs informativos (Condiciones Generales, Manual, Medicina Virtual, Coberturas Cáncer/Enf Graves/Odontología, Procedimiento GD, Pre-Autorización)
- `AGENTES` — whitelist: hoy `jhernandez@segurosdelins.com` (JC, WhatsApp 8822-1348, Lic. SUGESE 08-1318, Cód. 110113)
- `LOGO_INS_URL` — `https://cotizador.appsegurosdigitales.com/img/ins-logo.png` (compartido con Vital 360 y Cotizador Autos)

## Flujo agente

3 pasos + historial:

1. **Paso 1 · Asegurados:** form del titular (nombre + cédula + tel + email obligatorios) + lista de asegurados (modal CRUD con nombre, edad 0-99, género F/M, parentesco titular/cónyuge/hijo/otro)
2. **Paso 2 · Productos:**
   - Chips de asegurados arriba (resumen)
   - **Toggle "Ampliar cobertura de epidemias y pandemias"** siempre visible, default OFF (matching cotizador oficial INS)
   - **Toggle "Sin Reducción de Suma Asegurada"** auto-mostrado si algún asegurado ≥70
   - 3 cards de producto (Regional · Internacional · Grandes Deducibles) con:
     - Checkbox para incluir/excluir
     - Dropdown de deducibles
     - Lista de primas por asegurado (con IVA)
     - Total familiar / año (con IVA)
3. **Paso 3 · Enviar:** checkboxes para incluir 1-3 productos, dropdown de plan recomendado, link del cliente generado en vivo, 4 botones (Vista previa, Copiar enlace, WhatsApp, Enviar por correo)
4. **Mis cotizaciones (tab H):** historial localStorage con estados pendiente/aceptada/eliminada, botones Abrir / Copiar enlace / Marcar aceptada / Eliminar

## Flujo cliente

Vista renderizada desde el payload BASE64URL en `?c=`:

1. Hero (gradient navy/blue) con: top bar logo INS + nombre del agente + cód + nro cotización · greeting personalizado · chips de asegurados
2. Resumen de planes — 1-3 price cards con prima anual destacada y CTA "Me interesa este plan" (WhatsApp con mensaje pre-redactado)
3. Tabla comparativa con tooltips — 4 secciones: Principales · Maternidad · Especiales · Fallecimiento. Tooltips redactados desde Condiciones Particulares V13. La fila "Epidemias / pandemias" muestra montos dinámicos según `payload.ampliacionEpidemias`
4. Opciones de pago — 3 cards (anual recomendado, semestral +5%, trimestral +7%)
5. Períodos de espera — grid 3 columnas (general · condiciones 10m · condiciones 10m cont.)
6. Documentos para emisión — base + disparadores condicionales (66-70 telesuscripción · 71+ batería de exámenes)
7. Material informativo — 8 PDFs descargables del producto
8. CTA strip con datos del agente (WhatsApp + email)
9. Disclaimer naranja (Información importante · primas incluyen IVA · vigencia 30 días · indicación de si AMP está activado · SUGESE P16-35-A01-113)
10. Footer SDI con marca "Seguros Digitales" + barras + propiedad intelectual JC + Lic. SUGESE + Cód. agente

## Plantilla de correo HTML

`buildEmailHTML(payload, link)` produce HTML email-friendly (tablas anidadas + estilos inline):

- Header con gradiente navy/blue + logo INS (filter:brightness(0) invert(1)) + nro cotización
- Greeting personalizado al cliente
- CTA grande "VER COTIZACIÓN COMPLETA" al link `?c=`
- Lista de asegurados
- 1-3 cards de producto (color matching: navy/Internacional, reg/Regional soft blue, green/Grandes Deducibles) con barrita de color superior + nombre + deducible pill + prima familiar grande
- Sección "En la cotización completa encontrará" con bullets
- Firma del agente (nombre + cód + WhatsApp + email). **Sin avatar/círculo de iniciales** — removido el 24 jun 2026 por pedido de JC en ambas plantillas (cotización y póliza emitida).
- Footer SDI navy con propiedad intelectual + Lic. SUGESE + disclaimer SUGESE

### Segundo correo: guía de póliza emitida + adjuntos

Además del correo de cotización, hay un **segundo flujo** que la skill original no documentaba:

- Desde **Mis cotizaciones** (tab H), una vez emitida la póliza, `openPolizaModal(h)` abre el modal **"Datos de la póliza emitida"** (`#poliza-vigente-modal`, inyectado como string). Captura N.º de póliza, vigencia, producto y deducible, y envía la **guía de uso y reclamos** con `buildEmailPolizaVigenteMedical(st, polizaData)`.
- Ese modal tiene un **botón "＋ Agregar documentos"** (24 jun 2026): file input `multiple` (PDF/img/Word/Excel), lista con nombre+tamaño+✕ para quitar, tope **20 MB** total. El estado vive en `const pvmAttachments = []` dentro de `openPolizaModal`.
- **Adjuntos en Gmail:** `buildMime({..., attachments})` arma `multipart/mixed` (envuelve el `multipart/alternative` del HTML + cada adjunto base64 con `Content-Disposition: attachment`) **solo si hay adjuntos**; sin adjuntos mantiene el `multipart/alternative` original intacto. Plomería compartida por ambos correos, pero el botón de adjuntar **solo está en el de póliza emitida**.
- ⚠️ **El endpoint de subida NO sirve (commit `698c444`, jun 2026):** `upload/.../messages/send?uploadType=media` **no permite CORS desde el navegador** → "Failed to fetch". `sendEmailViaGmail` usa **siempre** el endpoint clásico `messages/send` con `{raw}` en JSON, haya o no adjuntos; el adjunto viaja dentro del MIME. Ver comentario en [index.html:2947](../../cotizador-Ins-Medical/index.html). **No volver a intentar el endpoint de subida.**

## Documentos del producto

PDFs en `docs/` del repo:

| Archivo | Origen | Tipo |
|---|---|---|
| `solicitud-ins-medical.pdf` | PENDIENTE de cargar (JC) | Base |
| `declaracion-salud.pdf` | Reusado de Vital 360 | Base |
| `autorizacion-expedientes.pdf` | Reusado de Vital 360 | Base |
| `solicitud-beneficios.pdf` | D0489 Solic de Beneficios español Edit.pdf | Base |
| `boleta-examen-fisico.pdf` | D0354 Boleta Examen Físico Edit.pdf | Edad 71+ |
| `boleta-laboratorios.pdf` | Boleta Laboratorios.pdf | Edad 71+ |
| `boleta-electrocardiograma.pdf` | Boleta Electrocardiogramas.pdf | Edad 71+ |
| `condiciones-generales-ins-medical.pdf` | Condiciones Generales INS Medical.pdf | Info |
| `manual-ins-medical.pdf` | Manual INS Medical.pdf | Info |
| `medicina-virtual.pdf` | Medicina Virtual Folleto.pdf | Info |
| `cobertura-cancer.pdf` | Cobertura Cancer.pdf | Info |
| `cobertura-enfermedades-graves.pdf` | Cobertura Enfermedades Graves.pdf | Info |
| `cobertura-odontologia-emergencia.pdf` | Cobertura Odontología Emergencia.pdf | Info |
| `procedimiento-grandes-deducibles.pdf` | Procedimiento Utilización Grandes Deducibles.pdf | Info |
| `formulario-preautorizacion.pdf` | Formulario Pre-Autorización.pdf | Info |

## Validación contra cotizador oficial INS

Caso de prueba: **Albert John Tierney**, 33 años, M, Grandes Deducibles $5000 sin AMP, anual.

- Prima del cotizador oficial INS (PDF "InformeCotización") = **$1,129.14** (con IVA)
- Prima del nuestro cotizador = **$1,129.14** (bit-for-bit match) ✅

Smoke tests 19/19 OK al cargar, incluyendo:
- BASE GD $5000 con_red edad 33 M = $1,107 sin IVA → $1,129.14 con IVA
- AMP GD $5000 con_red edad 33 M = $1,299 sin IVA
- Edades 0-99 completas × 12 secciones (2v × 3p × 2s)
- Recargos exactos por forma de pago

## Reglas y decisiones operativas

1. **Tarifas SIEMPRE con IVA al mostrar** — coincide con cotizador oficial INS y con lo que el cliente realmente paga.
2. **AMP epidemias default OFF** — coincide con default del cotizador INS oficial. El agente debe activar explícitamente.
3. **Sin opción mensual** — alineado con Vital 360, decisión de oficina (solo anual/semestral/trimestral).
4. **WhatsApp endpoint `wa.me`** — patrón estándar de cotizadores SDI.
5. **No commits a `main` sin verificación local previa** — preview `cotizador-insmedical` puerto 8801 antes de pushear.
6. **Bypass local visible solo en `hostname === "localhost"`** — para revisión sin OAuth. NO aparece en producción.
7. **OAuth Client compartido** con Cotizador Autos SDI y Vital 360. Authorized origins gestionados en el proyecto Google Cloud "Cotizador Autos SDI". Para subdominio nuevo agregar: `https://<sub>.appsegurosdigitales.com` + `https://<repo>.netlify.app`.

## Regeneración de tarifas

Si INS publica nuevas tarifas:

1. Reemplazar los XLSX en `C:\Users\segur\Ins Medical\`
2. `py scripts/extract_primas.py` — extrae y valida ambas versiones (base + amp)
3. `py scripts/build_primas_js.py` — regenera `primas.js`
4. Actualizar smoke tests si los valores conocidos cambian
5. Commit con label `tarifas-YYYY-MM-DD` y bump del `PRIMAS_VERSION`

## Errores comunes a evitar

- **No confundir versiones `base` vs `amp`** — el código siempre pasa `state.ampliacionEpidemias` al lookup. Si se olvida, devolverá tarifas inconsistentes.
- **No olvidar el IVA al mostrar** — `lookupPrima()` devuelve SIN IVA. Usar `calcPrimaProducto()` que ya aplica IVA en `total`, o `primaConIVA()` explícitamente.
- **No agregar IVA dos veces** — el campo `primaConIVA` en el payload ya incluye IVA; no multiplicar de nuevo.
- **No tocar `primas.js` a mano** — regenerar con `build_primas_js.py`.
- **No commitear `scripts/primas_data.js`** — es solo un artefacto de extracción opcional. La fuente de verdad es `primas.js` en la raíz.

## Pendientes / TODO

- 🟠 **ACORTAR EL LINK DEL CLIENTE — medido y confirmado el 27 jul 2026, JC lo dejó pendiente ese día.**

  **Diagnóstico (ya hecho, no hay que volver a medir).** Se replicó `buildClientPayload()` + `encodePayload()` contra el `primas.js` de producción. Largo real del link `?c=BASE64URL`:

  | Escenario | Link | URL `wa.me` |
  |---|---:|---:|
  | 1 asegurado · 1 producto (**piso absoluto**) | 1.028 | 1.276 |
  | Familia 3 · 3 productos (**típico**) | 2.254 | 2.506 |
  | Familia 7 · 3 productos (peor caso) | 3.798 | 4.050 |

  **Aplica el mismo problema que en Vital 360, y peor:** allá se acortó de ~1.000 → 51 chars con Netlify Function + Blobs (`/c/XXXXXXXXXX`) porque WhatsApp cortaba el link. Acá **la cotización más corta posible ya son 1.028 chars** — el piso de INS Medical es el techo que reventó en Vital 360, y la cotización típica es 2,2× ese umbral.

  **Síntoma distinto, misma causa:** si el corte parte la base64 a la mitad, esta app NO dice "Acceso restringido" sino *"No pudimos cargar esta cotización…"* ([index.html:3913](../../cotizador-Ins-Medical/index.html)). Solo cae en "Acceso restringido" si el corte se come el `?c=` entero.

  **Anatomía:** `productos` = **57 %** del payload, y es información **derivable** — `primasPorAseg` lleva `primaSinIVA` + `primaConIVA` por asegurado × producto, cuando `primas.js` se carga incondicionalmente en el mismo documento ([index.html:1346](../../cotizador-Ins-Medical/index.html)) y la vista cliente ya puede recalcularlas. Además `primaConIVA` no redondea → produce `1561.6200000000001` (17 chars donde caben 9).

  **Alternativas medidas** (1 / 3 / 7 asegurados): actual 1.437 / 2.274 / 3.798 · quitando derivados 1.005 / 1.282 / 1.824 · claves cortas agresivas 429 / 556 / 804. **Adelgazar solo no cierra el problema** — sigue arriba del umbral.

  **Recomendación:** replicar el patrón de Vital 360 (Function + Blobs). Costo a considerar: este repo **no tiene ninguna Function todavía** — `netlify.toml` es solo `publish = "."` + headers, sin `package.json`; `@netlify/blobs` obliga a meter build step en un proyecto que hoy no tiene. Beneficio extra: saca cédula, teléfono, correo, nombres y edades de toda la familia de una URL trivialmente decodificable que viaja por WhatsApp y queda en el historial.
- Cargar `docs/solicitud-ins-medical.pdf` (no estaba en la carpeta original)
- **Confirmar round-trip real de Gmail CON adjunto** por el endpoint clásico (póliza emitida). El endpoint de subida ya se descartó en real por CORS (commit `698c444`); falta confirmar un envío de prueba con PDF adjunto por la ruta que quedó viva.
- Considerar agregar segundo agente a `AGENTES` cuando JC lo necesite
- Eventual rediseño si cambian Condiciones Particulares del producto

---

> **Ubicaciones canon (desde el 7 sep 2026, decisión 10-C):** `jhernandez-vibecode/cotizador-Ins-Medical` → `.claude/skills/especialista-cotizador-ins-medical/SKILL.md` y `C:\Users\segur\.claude\skills\especialista-cotizador-ins-medical\SKILL.md`, byte-idénticas. Se edita en el repo, se commitea y se copia al user-level (o al revés, pero siempre las dos en el mismo día).
