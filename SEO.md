# SEO · César Revilla (plan de trabajo)

## Mapa de palabras clave (una URL por intención)

| URL | Búsqueda que debe ganar | Tipo |
|---|---|---|
| `/` | césar revilla, césar revilla diputado piura | Marca |
| `/biografia` | césar revilla biografía, quién es césar revilla | Marca |
| `/guias/diputados-de-piura-2026-2031` | diputados de piura 2026, diputados por piura | Informativa (alto volumen en el ciclo electoral) |
| `/guias/que-hace-un-diputado-del-peru` | qué hace un diputado perú, funciones cámara de diputados | Informativa |
| `/guias/semana-de-representacion-que-es` | semana de representación congreso | Informativa |
| `/guias/como-pedir-informacion-publica-peru` | cómo pedir información pública, solicitud de acceso a la información | Informativa (evergreen) |
| `/temas/reconstruccion` + ficha de la comisión | reconstrucción niño costero piura, comisión de reconstrucción | Tema |
| `/temas/salud` + ficha del hospital | hospital de alta complejidad piura | Tema (noticiosa) |
| `/temas/presupuesto-regional` + fichas | presupuesto piura mef, comisión de economía piura | Tema |
| `/temas/lluvias-y-drenaje` + ficha | drenaje pluvial piura, el niño piura | Tema (noticiosa) |
| `/piura/[provincia]` | congresista/diputado + provincia | Local (solo indexan con fichas) |

## Rutina semanal (lo que mantiene el sitio vivo)

1. **2 fichas de gestión** (agregar a `FICHAS` en `build.py`): qué pasó, dónde, cuándo, monto, documento, foto. Siempre con fuente oficial.
2. **1 guía ciudadana** (agregar a `GUIAS`) respondiendo una duda real de vecinos.
3. Enlazar cada ficha nueva desde su tema y desde la provincia correspondiente (`PROV_FICHAS`).
4. `python3 build.py && python3 audit.py` → subir a Netlify.
5. Notificar: Search Console (inspección de URL) y nota de prensa a medios locales con el enlace a la ficha.

## Reglas de calidad (evitan penalizaciones)

- Cada dato lleva su fuente. Sin fuente, no se publica.
- No crear una página por distrito sin contenido propio (Google la trata como "doorway page"). Primero ficha, después página.
- Cada título ≤ 60 caracteres y cada descripción ≤ 160 (`audit.py` lo valida).
- No borrar fichas: se actualizan. Si cambian los hechos, se agrega la actualización con fecha.
- La página de **Transparencia** responde con documentos, nunca con adjetivos.

## Pendientes antes de indexar (`DRAFT = False`)

- Dominio definitivo, foto oficial (`img/cesar-revilla.jpg`) e imagen social 1200×630 (`img/og.jpg`).
- Hoja de vida del JNE: contrastar trayectoria y docencia.
- Material del despacho: proyectos de ley, obras con monto y distrito, agenda, declaraciones juradas, contacto.
- Conectar Google Search Console y enviar `sitemap.xml`.
- Crear ficha en Wikidata y agregar `sameAs` (Congreso, redes verificadas) al `PERSON` de `build.py`.

## Wikipedia

Solo con fuentes de terceros y declarando la relación con el cliente (política de contribuciones remuneradas de Wikimedia). Las fichas de este sitio sirven como índice de fuentes, no como fuente.
