#!/usr/bin/env python3
"""Genera el sitio estático de César Revilla (v2: motor de contenido SEO).

Uso:  python3 build.py && python3 audit.py

Para lanzar:
  1. BASE = dominio definitivo.
  2. Foto oficial en img/cesar-revilla.jpg (y una imagen social 1200x630 en img/og.jpg).
  3. Completar los bloques "Pendiente" con material del despacho.
  4. DRAFT = False  -> quita noindex y oculta avisos.

Cómo crecer (lo que hace "real SEO"):
  - Cada gestión nueva = una ficha en FICHAS (una URL propia, con fuente y fecha).
  - Cada duda ciudadana frecuente = una guía en GUIAS.
  - Una provincia sale de noindex sola cuando tiene fichas en PROV_FICHAS.
"""
import html
import json
import os
import re

BASE = "https://cesarrevilla.com"   # dominio comprado en Porkbun
DRAFT = False                       # True = noindex + avisos visibles
PUB = "2026-10-30"                  # fecha de publicación de las fichas y guías creadas hoy
OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "César Revilla"
TAG = "Diputado del Perú por Piura"
BRAND_SUFFIX = " | César Revilla"

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def esc(s):
    return html.escape(s, quote=True)


def fdate(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} de {MESES[int(m) - 1]} de {y}"


def pend(t):
    if not DRAFT:
        return ""
    return f'<aside class="pendiente"><strong>Pendiente · solo borrador</strong>{t}</aside>'


# ---------- Fuentes verificadas ----------
SRC = {
    "recons": ("Congreso de la República", "https://comunicaciones.congreso.gob.pe/?p=135974"),
    "acta": ("Acta de la comisión (congreso.gob.pe)",
             "https://www.congreso.gob.pe/Docs/comisiones2021/cems-reconstruccion-fenomeno-nino-c/files/9na_desc_acta.pdf"),
    "radio": ("Radio Congreso",
              "https://comunicaciones.congreso.gob.pe/radio-congreso/entrevista-al-congresista-cesar-revilla-presidente-de-la-comision-de-seguimiento-al-proceso-de-la-reconstruccion-con-cambios"),
    "econ": ("Congreso de la República",
             "https://comunicaciones.congreso.gob.pe/noticias/comision-de-economia-realizo-sesion-extraordinaria-descentralizada-en-piura"),
    "ppto": ("El Tiempo", "https://eltiempo.pe/local/ejecutivo-intento-recortar-el-presupuesto-para-la-region-piura/"),
    "hosp1": ("El Tiempo",
              "https://eltiempo.pe/local/autoridades-no-vamos-a-permitir-que-le-quiten-a-la-region-piura-el-hospital-de-alta-complejidad/"),
    "hosp2": ("El Tiempo",
              "https://eltiempo.pe/nacional/retiro-de-inversion-de-hospital-de-alta-complejidad-es-una-represalia-a-piura/"),
    "dren": ("Panamericana (22/10/2026)",
             "https://panamericana.pe/EstaNoche/politica/476193-cesar-revilla-piura-necesita-sistema-integral-drenaje-pluvial"),
    "pl2902": ("LP Derecho", "https://lpderecho.pe/proponen-eliminar-trabajo-investigacion-obtener-grado-bachiller/"),
    "acred": ("El Tiempo (27/06/2026)", "https://eltiempo.pe/local/acreditan-a-representantes-por-piura-para-el-nuevo-congreso/"),
    "perfil": ("El Búho", "https://elbuho.pe/?p=193433"),
    "bio": ("Infomercado",
            "https://infomercado.pe/cesar-revilla-villanueva-hoja-de-vida-biografia-perfil-y-quien-es-el-congresista/"),
    "canaln": ("Canal N",
               "https://canaln.pe/actualidad/cesar-revilla-fuerza-popular-aun-no-define-si-buscara-presidir-mesa-directiva-camara-diputados-n493563"),
    "bicam": ("Diario Correo",
              "https://diariocorreo.pe/politica/adios-al-congreso-unicameral-asi-funcionara-el-nuevo-parlamento-bicameral-desde-el-proximo-27-de-julio-noticia/"),
    "semana": ("Congreso de la República · ABC Parlamentario",
               "https://comunicaciones.congreso.gob.pe/tv-congreso/abc-parlamentario-que-es-la-semana-de-representacion/"),
    "bn": ("Biblioteca Nacional del Perú (procedimiento de acceso a la información)",
           "https://www.bn.com.pe/transparenciabn/acceso-informacion.asp"),
    "cas": ("Piura Empresarial (2 de julio de 2022)", "https://piuraempresarial.com/2022/07/02/congresista-cesar-revilla-la-estabilidad-para-los-cas-covid-es-una-realidad/"),
    "rpp23": ("RPP (17 de agosto de 2023)", "https://rpp.pe/economia/negocios/quien-es-cesar-revilla-el-nuevo-presidente-de-la-comision-de-economia-noticia-1500820"),
    "econ23": ("Congreso de la República (16 de agosto de 2023)", "https://comunicaciones.congreso.gob.pe/noticias/comision-de-economia-trabajara-por-leyes-populares-y-no-populistas/"),
    "comercio23": ("El Comercio (14 de agosto de 2023)", "https://elcomercio.pe/economia/peru/cesar-revilla-elegido-por-fuerza-popular-para-presidir-la-comision-de-economia-que-proyectos-economicos-ha-presentado-congreso-cajas-municipales-presidente-noticia/"),
    "candados": ("Congreso de la República (4 de noviembre de 2023)", "https://comunicaciones.congreso.gob.pe/noticias/comision-de-economia-rompera-todos-los-candados-para-que-el-ejecutivo-pueda-auxiliar-a-poblacion-vulnerable-ante-el-nino/"),
    "ani": ("Caretas (23 de octubre de 2024)", "https://caretas.pe/?p=725381"),
    "cts": ("América TV (16 de abril de 2024)", "https://www.americatv.com.pe/noticias/amp/actualidad/congresista-cesar-revilla-buscamos-aprobar-retiro-cts-manana-n490673"),
    "km980a": ("Cutivalú (3 de septiembre de 2021)", "https://www.cutivalu.pe/congresista-cesar-revilla-propondra-sesion-descentralizada-de-comision-de-la-reconstruccion-en-el-bajo-piura/"),
    "km980b": ("Cutivalú (3 de septiembre de 2021)", "https://www.cutivalu.pe/congresistas-se-comprometen-a-gestionar-proyectos-a-favor-de-damnificados-del-km-980/"),
    "huanca1": ("Congreso de la República (17 de octubre de 2024)", "https://comunicaciones.congreso.gob.pe/noticias/aprueban-dictamen-para-la-creacion-de-la-universidad-nacional-de-huancabamba/"),
    "huanca2": ("La Hora (noviembre de 2024)", "https://lahora.pe/local/piura-publican-ley-para-la-creacion-de-la-universidad-nacional-de-huancabamba/"),
    "crimen1": ("Congreso de la República (27 de marzo de 2025)", "https://comunicaciones.congreso.gob.pe/?p=388948"),
    "crimen2": ("Congreso de la República (7 de julio de 2025)", "https://comunicaciones.congreso.gob.pe/?p=410087"),
    "vocero1": ("El Comercio (9 de agosto de 2024)", "https://elcomercio.pe/politica/congreso/keiko-fujimori-informa-que-bancada-fuerza-popular-eligio-a-arturo-alegria-como-vocero-para-el-periodo-2024-2025-congreso-cesar-revilla-jeny-lopez-ultimas-noticia/"),
    "vocero2": ("Infobae (7 de agosto de 2025)", "https://www.infobae.com/peru/2025/08/07/keiko-fujimori-anuncia-a-fuerza-popular-al-mando-de-comisiones-clave-del-congreso-2025-2026-constitucion-economia-agraria-y-produccion/"),
    "rpp26": ("RPP (22 de agosto de 2026)", "https://rpp.pe/politica/congreso/cesar-revilla-respalda-gestion-del-ejecutivo-frente-a-el-nino-y-dice-que-el-gobierno-anterior-no-tomo-las-medidas-adecuadas-noticia-1703120"),
    "diputados": ("Cámara de Diputados · ficha oficial", "https://diputados.congreso.gob.pe/diputado/revilla-villanueva-cesar-manuel/"),
    "planhid": ("Congreso de la República (24 de julio de 2025)", "https://comunicaciones.congreso.gob.pe/noticias/comision-permanente-aprueba-iniciativa-que-impulsa-el-plan-hidraulico-del-departamento-de-piura/"),
    "tapacuy": ("Congreso de la República (17 de noviembre de 2021)", "https://comunicaciones.congreso.gob.pe/noticias/comision-agraria-aprobo-recomendar-que-ejecutivo-construya-proyecto-de-riego-en-bajo-piura/"),
    "tapacuy2": ("Congreso de la República · Radio Congreso (16 de febrero de 2026)", "https://comunicaciones.congreso.gob.pe/radio-congreso/congreso-en-regiones-16-de-febrero-2026-i-represa-en-tapa-de-cuy-avanza-con-respaldo-legal/"),
    "alcaldes22": ("Congreso de la República (21 de abril de 2022)", "https://comunicaciones.congreso.gob.pe/noticias/alcaldes-de-piura-piden-presupuesto-para-proyectos-que-requiere-la-poblacion/"),
    "nino26": ("El Tiempo (30 de julio de 2026)", "https://eltiempo.pe/local/piura-con-recursos-insuficientes-para-el-nino/"),
    "razon26": ("La Razón (15 de agosto de 2026)", "https://larazon.pe/cesar-revilla-queremos-reducir-la-pobreza-de-26-a-menos-de-15-en-estos-cinco-anos-de-gobierno/"),
    "econbal": ("Congreso de la República (9 de julio de 2024)", "https://comunicaciones.congreso.gob.pe/noticias/comision-de-economia-del-congreso-aprobo-58-dictamenes-y-logro-20-leyes-a-favor-de-millones-de-peruanos/"),
    "mypes23": ("Congreso de la República (12 de octubre de 2023)", "https://comunicaciones.congreso.gob.pe/noticias/congreso-insiste-en-propuesta-que-busca-fortalecer-la-capacidad-financiera-de-las-mypes/"),
    "textil23": ("Congreso de la República (16 de octubre de 2023)", "https://comunicaciones.congreso.gob.pe/noticias/aprueban-dictamen-que-define-medidas-para-impulsar-competitividad-del-sector-textil/"),
    "afp24": ("Infobae (25 de marzo de 2024)", "https://www.infobae.com/peru/2024/03/25/retiro-afp-comision-de-economia-del-congreso-aprueba-dictamen-para-septima-liberacion-de-fondos-de-hasta-4-uit/"),
    "cts24": ("Infobae (2 de mayo de 2024)", "https://www.infobae.com/peru/2024/05/02/retiro-cts-2024-pleno-del-congreso-debate-hoy-dictamen-que-autoriza-liberar-el-100-del-dinero-de-los-trabajadores/"),
    "ir24": ("Congreso de la República (12 de junio de 2024)", "https://comunicaciones.congreso.gob.pe/noticias/pleno-aprueba-dictamen-que-propone-un-regimen-excepcional-del-impuesto-a-la-renta/"),
    "vbp": ("Vota Bien Perú (datos del Congreso y de la declaración al JNE)", "https://votabienperu.com/legisladores/h0w8xr6ateux0umk5u0q78i5"),
    "canaln26": ("Canal N (21 de julio de 2026)", "https://canaln.pe/actualidad/cesar-revilla-fuerza-popular-aun-no-define-si-buscara-presidir-mesa-directiva-camara-diputados-n493563"),
    "eclara": ("Elección Clara (hoja de vida declarada al JNE)", "https://www.eleccionclara.pe/candidatos/4492"),
    "gobpe": ("gob.pe · Solicitar acceso a la información pública",
              "https://www.gob.pe/20399-solicitar-acceso-a-la-informacion-publica"),
    "proceso": ("Congreso de la República · Proceso legislativo", "https://www.congreso.gob.pe/eng/legislative-process/"),
    "infomercado26": ("Infomercado (17 de junio de 2026)", "https://infomercado.pe/asi-quedo-el-nuevo-congreso-tras-el-conteo-final-de-la-onpe/"),
    "gestionvoc": ("Gestión (11 de julio de 2026)", "https://gestion.pe/peru/politica/fuerza-popular-designa-a-cecilia-chacon-y-patricia-juarez-como-voceras-en-el-congreso-bicameral-noticia/"),
    "reto": ("Canal N (26 de julio de 2026)", "https://canaln.pe/actualidad/oscar-reto-otero-elegido-presidente-camara-diputados-n493694"),
    "infobae1001": ("Infobae (1 de octubre de 2026)", "https://www.infobae.com/peru/2026/10/01/fuerza-popular-no-insistira-con-los-66-puntos-del-pedido-de-facultades-entendemos-que-ese-es-el-consenso/"),
    "canaln1001": ("Canal N (1 de octubre de 2026)", "https://canaln.pe/actualidad/cesar-revilla-hay-parte-juntos-peru-que-busca-generar-caos-y-enfrentamiento-n495386"),
    "fb1118": ("Publicación oficial de César Revilla en Facebook (18 de noviembre de 2026)", "https://www.facebook.com/story.php?story_fbid=1755730106562699&id=100063771796817"),
    "congreso1014": ("Congreso de la República (14 de octubre de 2026)", "https://comunicaciones.congreso.gob.pe/noticias/diputados-de-fuerza-popular-atienden-demandas-de-infraestructura-prevencion-de-riesgos-y-presupuesto-para-hospitales/"),
}


from explica_data import EXP_SRC, EXP_TEMAS, EXPLICA, COYUNTURA  # noqa: E402
SRC.update(EXP_SRC)


def a_src(key):
    label, url = SRC[key]
    return f'<a class="fuente" href="{url}" rel="noopener" target="_blank">Fuente: {esc(label)}</a>'


def li_src(key):
    label, url = SRC[key]
    return f'<li><a href="{url}" rel="noopener" target="_blank">{esc(label)}</a></li>'


# ---------- Temas (hubs) ----------
TEMAS = {
    "reconstruccion": dict(
        h1="Reconstrucción tras el Niño Costero", seo="Reconstrucción del Niño Costero en Piura",
        desc="Seguimiento del Congreso a la reconstrucción en las zonas afectadas por el Niño Costero, con las gestiones de César Revilla.",
        intro="La reconstrucción tras el Fenómeno del Niño Costero ha sido uno de los ejes de su trabajo en el Congreso.",
        card="Presidió la comisión que da seguimiento a la reconstrucción.",
        pend="Agregar obras concretas (nombre, distrito, monto, avance), oficios enviados a la ARCC/ANIN y fotos de visitas. Cada obra = una ficha nueva."),
    "salud": dict(
        h1="Salud y Hospital de Alta Complejidad", seo="Salud en Piura: Hospital de Alta Complejidad",
        desc="Las gestiones de César Revilla en salud para Piura, con eje en el Hospital de Alta Complejidad.",
        intro="César Revilla es cirujano dentista y tiene una maestría en Gestión de los Servicios de la Salud.",
        card="Su postura frente a la exclusión del hospital para Piura.",
        pend="Agregar cronología con fechas, oficios al Minsa, intervenciones en comisión y estado actual del proyecto con fuente oficial."),
    "presupuesto-regional": dict(
        h1="Presupuesto regional para Piura", seo="Presupuesto regional para Piura",
        desc="Defensa del presupuesto de Piura y sesiones descentralizadas de la Comisión de Economía en la región.",
        intro="El presupuesto para Piura y las sesiones descentralizadas del Congreso en la región son parte de su agenda.",
        card="Defensa del presupuesto y sesiones descentralizadas en Piura.",
        pend="Agregar montos (presupuesto 2026 y 2027 para Piura) con enlace al MEF."),
    "lluvias-y-drenaje": dict(
        h1="Lluvias y drenaje pluvial en Piura", seo="Lluvias y drenaje pluvial en Piura",
        desc="Propuestas de César Revilla para prevenir inundaciones en Piura frente al anunciado Fenómeno El Niño.",
        intro="Las lluvias recientes volvieron a poner la prevención en la agenda regional.",
        card="Plan integral de drenaje frente al anunciado Fenómeno El Niño.",
        pend="Agregar estado del proyecto (CUI, monto, plazos) con fuente de ANIN o MEF y las gestiones nuevas."),
    "economia-y-empleo": dict(
        h1="Economía, pensiones y empleo", seo="Economía, AFP, CTS y mypes: César Revilla",
        desc="Las leyes económicas que impulsó César Revilla como presidente de la Comisión de Economía del Congreso: AFP, CTS, mypes, Fonavi y contrataciones.",
        intro="Como presidente de la Comisión de Economía del Congreso (2023-2024), César Revilla condujo leyes que alcanzan a trabajadores y empresas de todo el Perú.",
        card="20 leyes desde la Comisión de Economía: AFP, CTS, mypes y Fonavi.",
        pend=""),
    "seguridad-ciudadana": dict(
        h1="Seguridad ciudadana y crimen organizado", seo="Seguridad y crimen organizado: César Revilla",
        desc="El trabajo de César Revilla en el Congreso frente al terrorismo y el crimen organizado transnacional.",
        intro="La seguridad ciudadana es uno de los temas que César Revilla ha trabajado a nivel nacional desde el Congreso.",
        card="Presidió la comisión contra el terrorismo y el crimen organizado.",
        pend="Agregar proyectos de ley de seguridad que presente como diputado, con número y estado."),
    "agua-y-agro": dict(
        h1="Agua, riego y agro en Piura", seo="Agua y riego en Piura: César Revilla",
        desc="Las iniciativas de César Revilla sobre agua, riego y agricultura en Piura: Plan Hidráulico y represa Tapa de Cuy.",
        intro="El agua para el agro y la gestión de los ríos de Piura están ligados a la prevención frente a El Niño.",
        card="Autor de la ley que impulsa el Plan Hidráulico de Piura.",
        pend="Agregar el número de ley publicada del Plan Hidráulico y su avance en el Ejecutivo."),
    "educacion": dict(
        h1="Educación y universidades", seo="Educación y universidades: César Revilla",
        desc="Las iniciativas de César Revilla en educación superior, como la ley que crea la Universidad Nacional de Huancabamba.",
        intro="La educación superior en las provincias de Piura es parte de su trabajo legislativo.",
        card="Autor del proyecto que creó la Universidad Nacional de Huancabamba.",
        pend="Agregar el avance de la implementación de la Universidad Nacional de Huancabamba (comisión organizadora, sede, presupuesto)."),
}

# ---------- Fichas de gestión (una URL por hecho) ----------
FICHAS = [
    dict(slug="drenaje-pluvial-piura-fenomeno-el-nino", tema="lluvias-y-drenaje", hecho="22 de octubre de 2026", iso="2026-10-22",
         h1="Drenaje pluvial en Piura: Revilla pide un sistema integral ante El Niño",
         seo="Drenaje pluvial en Piura y El Niño",
         desc="César Revilla advirtió el 22 de octubre de 2026 que las lluvias evidenciaron la vulnerabilidad de Piura y pidió un sistema integral de drenaje pluvial.",
         resumen="Revilla pidió un sistema integral de drenaje pluvial para Piura tras las lluvias recientes y ante el anunciado Fenómeno El Niño.",
         paras=["El 22 de octubre de 2026, el diputado César Revilla advirtió que las lluvias recientes en Piura volvieron a evidenciar la vulnerabilidad de la región ante el anunciado Fenómeno El Niño, y planteó que Piura necesita un sistema integral de drenaje pluvial.",
                "Según explicó, la Autoridad Nacional de Infraestructura (ANIN) culminó el perfil del proyecto, luego de que el plan maestro elaborado por Reconstrucción con Cambios no cumpliera con los requisitos técnicos necesarios."],
         keys=["dren"], pend="Agregar el estado actual del proyecto (código CUI, monto, plazos) y los oficios que Revilla envíe a la ANIN y al MEF."),
    dict(slug="hospital-alta-complejidad-piura", tema="salud", hecho="Fecha por confirmar", iso=None,
         h1="Hospital de Alta Complejidad de Piura: la postura de César Revilla",
         seo="Hospital de Alta Complejidad de Piura",
         desc="La postura de César Revilla frente a la propuesta de dejar de lado el Hospital de Alta Complejidad de Piura y su exclusión del programa de inversiones.",
         resumen="Revilla rechazó que se postergue otra vez el Hospital de Alta Complejidad de Piura y calificó de represalia su exclusión del programa de inversiones.",
         paras=["César Revilla rechazó la propuesta del entonces ministro de Salud de dejar de lado el Hospital de Alta Complejidad para Piura y, en su lugar, fortalecer el primer nivel de atención. Sostuvo que no se puede permitir que otra vez se postergue a Piura con el hospital para la población de menores recursos.",
                "Después, cuando el Ministerio de Salud excluyó el hospital del programa de inversiones, Revilla afirmó que la decisión sería una represalia hacia la región.",
                "Revilla es cirujano dentista y tiene una maestría en Gestión de los Servicios de la Salud."],
         keys=["hosp1", "hosp2", "perfil"], pend="Confirmar las fechas de ambas declaraciones y agregar los oficios y pedidos al Minsa."),
    dict(slug="presupuesto-piura-recorte-mef", tema="presupuesto-regional", hecho="Fecha por confirmar", iso=None,
         h1="Presupuesto de Piura: Revilla informó un intento de recorte del MEF",
         seo="Presupuesto de Piura y el MEF",
         desc="César Revilla informó que el Ejecutivo, a través del MEF, intentó recortar el presupuesto asignado a Piura y planteó un frente de bancadas aliadas.",
         resumen="Revilla informó que el MEF intentó recortar el presupuesto de Piura y propuso un frente político de bancadas aliadas.",
         paras=["El congresista César Revilla informó a la población de Piura que el Ejecutivo, a través del Ministerio de Economía y Finanzas (MEF), intentó recortar el presupuesto asignado a la región.",
                "Ante ello, planteó conformar un frente político de bancadas aliadas para evitar lo que consideró injusto para Piura."],
         keys=["ppto"], pend="Confirmar fecha y agregar las cifras del presupuesto (antes y después) con enlace al MEF."),
    dict(slug="comision-economia-sesion-descentralizada-piura", tema="presupuesto-regional", hecho="Fecha por confirmar", iso=None,
         h1="La Comisión de Economía sesionó en Piura bajo la presidencia de Revilla",
         seo="Comisión de Economía sesiona en Piura",
         desc="La Comisión de Economía del Congreso, que presidía César Revilla, realizó en Piura su III Sesión Extraordinaria Descentralizada.",
         resumen="La Comisión de Economía que presidía Revilla sesionó en Piura y analizó, entre otros, el proyecto de nueva Ley de Contrataciones del Estado.",
         paras=["La Comisión de Economía, Banca, Finanzas e Inteligencia Financiera, que presidía el congresista César Revilla, realizó en Piura su III Sesión Extraordinaria Descentralizada.",
                "En la sesión se analizó el Proyecto de Ley 5472/2022-PE, que plantea una nueva Ley de Contrataciones del Estado. También sustentaron proyectos la congresista Rossangella Barbarán (PL 6331/2023-CR, sobre gastos deducibles de las rentas de cuarta y quinta categoría) y la congresista Cruz María Zeta Chunga (PL 5101/2022-CR, que propone autorizar al Fondo AgroPerú la compra de deuda de agricultores afectados por el fenómeno climatológico).",
                "Revilla destacó la importancia de las sesiones y audiencias descentralizadas, sobre todo cuando hay demandas urgentes que atender."],
         keys=["econ"], pend="Confirmar la fecha de la sesión y agregar fotos, asistentes y acuerdos."),
    dict(slug="comision-reconstruccion-nino-costero", tema="reconstruccion", hecho="Periodo 2021–2026", iso=None,
         h1="Revilla presidió la Comisión de Seguimiento a la Reconstrucción del Niño Costero",
         seo="Comisión de Reconstrucción del Niño Costero",
         desc="César Revilla fue elegido presidente de la comisión del Congreso que da seguimiento a la reconstrucción en las zonas afectadas por el Niño Costero.",
         resumen="Revilla fue elegido presidente de la comisión multipartidaria que da seguimiento a la reconstrucción tras el Niño Costero.",
         paras=["El congresista por Piura César Revilla fue elegido presidente de la Comisión Especial Multipartidaria de Seguimiento al proceso de Reconstrucción en las zonas afectadas por el Fenómeno del Niño Costero.",
                "Como presidente, dirigió sesiones en las que la comisión acordó pedir a la Comisión de Economía que priorice el dictamen del Proyecto de Ley 3236-2022-PE, sobre medidas para implementar el Plan Integral para la Reconstrucción con Cambios. El pedido se aprobó por unanimidad de los presentes.",
                "También se reunió en Piura con autoridades locales y evaluó los sistemas de salud durante su Semana de Representación."],
         keys=["recons", "acta", "radio"], pend="Agregar obras concretas supervisadas por la comisión, con distrito, monto y avance."),
    dict(slug="cas-covid-pl-2204-personal-de-salud", tema="salud", hecho="Julio de 2022", iso="2022-07-02",
         h1="CAS COVID: el Pleno aprobó el PL 2204, de autoría de Revilla, para el personal de salud",
         seo="CAS COVID: Pleno aprueba el PL 2204",
         desc="El Pleno aprobó con 112 votos el PL 2204, de César Revilla, que pasa al personal de salud CAS COVID a contrato CAS regular de forma excepcional.",
         resumen="El Pleno aprobó con 112 votos el Proyecto de Ley 2204, que pasa al personal CAS COVID a contrato CAS regular por una sola vez.",
         paras=["En julio de 2022, el Pleno del Congreso aprobó con 112 votos a favor el Proyecto de Ley 2204, presentado por Fuerza Popular y de autoría del congresista piurano César Revilla Villanueva.",
                "La iniciativa busca que el personal de salud contratado bajo la modalidad CAS COVID pase a un contrato CAS regular, de forma excepcional y por una sola vez, en el marco de la emergencia sanitaria. Según la nota, alcanzaría a unos 60 mil trabajadores asistenciales contratados durante la pandemia, y quienes fueron despedidos y cumplen ciertos requisitos podrían volver a la plaza donde trabajaban.",
                "Revilla expresó su satisfacción por el respaldo de las distintas bancadas. La fuente no confirma si la autógrafa fue luego promulgada por el Ejecutivo."],
         keys=["cas"], pend=""),
    dict(slug="comision-economia-presidencia-2023", tema="economia-y-empleo", hecho="16 de agosto de 2023", iso="2023-08-16",
         h1="Revilla asumió la presidencia de la Comisión de Economía en agosto de 2023",
         seo="Revilla presidió la Comisión de Economía",
         desc="El 16 de agosto de 2023 se instaló la Comisión de Economía del Congreso con César Revilla como presidente; estas fueron sus prioridades.",
         resumen="La Comisión de Economía se instaló el 16 de agosto de 2023 con Revilla como presidente y una agenda de mypes, inversión y responsabilidad fiscal.",
         paras=["La Comisión de Economía, Banca, Finanzas e Inteligencia Financiera se instaló el 16 de agosto de 2023, para el año de sesiones 2023-2024, con César Revilla Villanueva (Fuerza Popular) como presidente. Segundo Montalvo (Perú Libre) fue vicepresidente y Alejandro Cavero (Avanza País), secretario. La lista fue aprobada por unanimidad y Revilla reemplazó en el cargo a Rosangella Barbarán.",
                "Entre las prioridades que se anunciaron figuran impulsar leyes que beneficien a la mayoría y evitar propuestas populistas con poca responsabilidad fiscal, reducir la informalidad, promover la inversión privada, fortalecer a las mypes, mejorar el empleo y atender el impacto del Fenómeno El Niño. También se propuso pedir al Ministerio de Economía y Finanzas proyecciones realistas de crecimiento e inflación.",
                "Según RPP, la comisión tenía 32 dictámenes listos para el Pleno, y Revilla había presentado 21 proyectos de ley hasta ese momento."],
         keys=["econ23", "rpp23"], pend=""),
    dict(slug="proyectos-economicos-2023", folder="proyectos-de-ley", tema="economia-y-empleo", hecho="Agosto de 2023", iso="2023-08-14",
         h1="Cuatro proyectos económicos de Revilla: maquinaria, El Niño, pasivos mineros y cajas municipales",
         seo="Proyectos económicos de César Revilla (2023)",
         desc="Los cuatro proyectos económicos de César Revilla en 2023: maquinaria ante desastres, El Niño, pasivos ambientales mineros y cajas municipales.",
         resumen="De sus 21 proyectos de ley hasta agosto de 2023, cuatro eran de materia económica, según El Comercio.",
         paras=["El Comercio informó el 14 de agosto de 2023 que, de los 21 proyectos de ley presentados por César Revilla, cuatro eran de materia económica.",
                "PL 4769: permitiría a gobiernos regionales y locales adquirir maquinaria para prevenir desastres; el MEF y el MTC definirían el tipo de maquinaria y los mecanismos de compra, financiados con el Foncomún y el Foncor.",
                "PL 4661: autorizaría a la Autoridad para la Reconstrucción con Cambios a realizar acciones de construcción en zonas de emergencia, como medida de mitigación ante El Niño.",
                "Ley 31616: establece medidas especiales para empresas en reestructuración patrimonial y fortalece la gestión ambiental en áreas con pasivos ambientales mineros. El Ejecutivo la observó por falta de análisis costo-beneficio y el Congreso la aprobó por insistencia.",
                "Expediente 2021/5514: busca reforzar la elección de los directorios de las cajas municipales de ahorro y crédito y limitar la permanencia prolongada de sus miembros."],
         keys=["comercio23"], pend=""),
    dict(slug="el-nino-2023-comision-economia-facilidades", tema="lluvias-y-drenaje", hecho="4 de noviembre de 2023", iso="2023-11-04",
         h1="El Niño 2023: la Comisión de Economía ofreció quitar obstáculos al Ejecutivo",
         seo="El Niño 2023 y la Comisión de Economía",
         desc="El 4 de noviembre de 2023, César Revilla ofreció quitar obstáculos para que el Ejecutivo atendiera a la población vulnerable ante El Niño.",
         resumen="Como presidente de la Comisión de Economía, Revilla ofreció eliminar trabas para que el Ejecutivo atendiera a la población vulnerable ante El Niño.",
         paras=["El 4 de noviembre de 2023, el presidente de la Comisión de Economía, César Revilla, dijo en Congreso TV que su comisión daría todo el apoyo posible y eliminaría los obstáculos para que el Gobierno pudiera atender a la población más vulnerable durante El Niño, previsto para el verano siguiente.",
                "Señaló que el Congreso había aprobado un crédito suplementario para que el Gobierno Nacional ejecutara el presupuesto destinado a la emergencia climática, y que la respuesta requería coordinación con gobernadores regionales, autoridades locales y el Ejecutivo.",
                "También expresó preocupación por las temperaturas altas en Piura, inusuales para la época, que podían anticipar lluvias intensas."],
         keys=["candados"], pend=""),
    dict(slug="ani-comision-seguimiento-2024", tema=None, hecho="23 de octubre de 2024", iso="2024-10-23",
         h1="Revilla presidió la comisión de seguimiento a la Autoridad Nacional de Infraestructura",
         seo="Revilla preside comisión de la ANI",
         desc="En octubre de 2024, César Revilla fue elegido presidente de la comisión que hace seguimiento a la Autoridad Nacional de Infraestructura.",
         resumen="Revilla fue elegido presidente de la comisión que da seguimiento a la creación e implementación de la Autoridad Nacional de Infraestructura.",
         paras=["César Revilla Villanueva fue elegido presidente de la Comisión Especial de Seguimiento e Implementación de la Autoridad Nacional de Infraestructura (ANI), según informó Caretas el 23 de octubre de 2024.",
                "La comisión fue creada por la Moción de Orden del Día 7515, presentada por Fuerza Popular y aprobada por el Pleno el 31 de agosto de 2023, y funciona hasta el fin del periodo parlamentario. Su función es hacer seguimiento al proceso de creación, implementación y funcionamiento de la ANI.",
                "Revilla indicó que el grupo priorizaría el trabajo conjunto para impulsar megaproyectos en las regiones. La mesa directiva la completaron Darwin Espinoza (vicepresidente) y Gustavo Cordero Jon Tay (secretario)."],
         keys=["ani"], pend=""),
    dict(slug="retiro-cts-2024-comision-economia", tema="economia-y-empleo", hecho="Abril y mayo de 2024", iso="2024-05-02",
         h1="Retiro del 100% de la CTS en 2024: el dictamen salió de la comisión que presidía Revilla",
         seo="Retiro del 100% de la CTS 2024 (Ley 32027)",
         desc="La liberación del 100% de la CTS en 2024 (Ley 32027) salió de la Comisión de Economía que presidía César Revilla. Alcanzó a unos 4 millones de trabajadores.",
         resumen="El Pleno aprobó con 98 votos liberar el 100% de la CTS hasta fines de 2024. La norma se publicó como Ley 32027.",
         paras=["El 16 de abril de 2024, César Revilla, presidente de la Comisión de Economía, anunció en Canal N que el Congreso buscaba aprobar la liberación de la CTS y advirtió que el sistema de pensiones necesitaba una reforma integral.",
                "El 2 de mayo de 2024, el Pleno aprobó con 98 votos a favor el texto que permite a los trabajadores disponer del 100% de su Compensación por Tiempo de Servicios hasta el 31 de diciembre de 2024. El dictamen agrupó 11 proyectos de las comisiones de Economía y de Trabajo, y según Infobae alcanzaría a unos 4 millones de trabajadores.",
                "Revilla sostuvo que la medida debía ser temporal, hasta fines de 2024, porque la economía podía reactivarse al año siguiente. La norma se publicó como Ley 32027, una de las 20 leyes que la Comisión de Economía logró en el periodo 2023-2024."],
         keys=["cts", "cts24", "econbal"], pend=""),
    dict(slug="km-980-sesion-descentralizada-reconstruccion", tema="reconstruccion", hecho="3 de septiembre de 2021", iso="2021-09-03",
         h1="Km 980: Revilla propuso una sesión descentralizada de la comisión de Reconstrucción",
         seo="Km 980 y la comisión de Reconstrucción",
         desc="El 3 de septiembre de 2021, César Revilla propuso llevar al km 980 de la vía Piura-Chiclayo una sesión de la comisión de Reconstrucción.",
         resumen="En el asentamiento Nuevo Santa Rosa, Revilla propuso que la comisión de Reconstrucción sesione en el km 980, donde viven damnificados del Niño Costero.",
         paras=["El 3 de septiembre de 2021, en el asentamiento Nuevo Santa Rosa, km 980 de la carretera Piura-Chiclayo, se reunieron damnificados del Niño Costero de 2017, congresistas y autoridades locales, convocados por la Municipalidad Provincial de Piura. Los pobladores llevaban cuatro años viviendo allí sin servicios básicos.",
                "César Revilla, integrante de la Comisión Especial Multipartidaria que monitorea la reconstrucción, propuso que una sesión descentralizada de esa comisión se realice en el km 980. Dijo que la comisión debía instalarse la semana siguiente y que esa sería su primera solicitud.",
                "En la misma reunión, el congresista Eduardo Castillo anunció que pediría que un congresista de Piura presidiera esa comisión, y el alcalde de Piura señaló que era el primer paso para urbanizar los asentamientos reubicados."],
         keys=["km980a", "km980b"], pend=""),
    dict(slug="revilla-lidera-votacion-piura-2026", tema=None, hecho="26 de junio de 2026", iso="2026-06-26",
         h1="Elecciones 2026: César Revilla encabezó la votación de Piura con 23,816 votos",
         seo="Revilla encabezó la votación de Piura 2026",
         desc="César Revilla encabezó la votación regional de Piura en 2026 con 23,816 votos preferenciales y recibió su credencial del JNE el 26 de junio.",
         resumen="Revilla obtuvo 23,816 votos preferenciales, la primera votación de Piura, y recibió su credencial del JNE el 26 de junio de 2026.",
         paras=["César Revilla encabezó la votación regional de Piura en las elecciones de 2026 con 23,816 votos preferenciales, por encima de Eduardo Castillo, quien fue reelecto con 21,130.",
                "El Jurado Nacional de Elecciones entregó las credenciales a los representantes de Piura el viernes 26 de junio de 2026, para el periodo 2026–2031. La región tiene siete escaños en la Cámara de Diputados."],
         keys=["acred"], pend=""),
    dict(slug="universidad-nacional-de-huancabamba-ley-32162", tema="educacion", hecho="Noviembre de 2024", iso="2024-11-12",
         h1="Universidad Nacional de Huancabamba: la ley nació de un proyecto de Revilla",
         seo="Universidad de Huancabamba: Ley 32162",
         desc="La Ley 32162 crea la Universidad Nacional de Huancabamba. El dictamen se basó en el Proyecto de Ley 8018/2023-CR, de César Revilla.",
         resumen="El Congreso creó la Universidad Nacional de Huancabamba con la Ley 32162, sobre la base del PL 8018/2023-CR de Revilla.",
         paras=["El 17 de octubre de 2024, el Pleno del Congreso aprobó el dictamen que crea la Universidad Nacional de Huancabamba. Según la nota oficial del Congreso, el dictamen se sustentó en el Proyecto de Ley 8018/2023-CR, cuyo autor es el congresista César Revilla Villanueva (Fuerza Popular).",
                "Durante el debate, Revilla propuso incorporar una disposición complementaria final para que la universidad sea un pliego presupuestal, propuesta que fue aceptada. La votación fue de 75 votos a favor, ninguno en contra y 4 abstenciones, y el Pleno la exoneró de segunda votación.",
                "La Ley 32162 se publicó en el diario oficial El Peruano en noviembre de 2024. Según La Hora, la universidad funcionará en la provincia de Huancabamba, contempla carreras como Ingeniería Civil, Agronomía, Medicina Humana, Enfermería y Educación, y el Gobierno Regional de Piura se encargará de construir la sede central."],
         keys=["huanca1", "huanca2"], pend="Enlazar el texto oficial de la Ley 32162 en El Peruano y el avance de su implementación."),
    dict(slug="comision-crimen-organizado-presidencia-2025", tema="seguridad-ciudadana", hecho="27 de marzo de 2025", iso="2025-03-27",
         h1="Revilla presidió la comisión contra el terrorismo y el crimen organizado",
         seo="Revilla preside comisión contra el crimen",
         desc="El 27 de marzo de 2025, César Revilla fue elegido por unanimidad presidente de la comisión del Congreso contra el terrorismo y el crimen organizado.",
         resumen="Revilla fue elegido por unanimidad para presidir la comisión multipartidaria contra el terrorismo y el crimen organizado transnacional.",
         paras=["El 27 de marzo de 2025, César Revilla Villanueva (Fuerza Popular) fue elegido por unanimidad presidente de la Comisión Especial Multipartidaria encargada de realizar trabajo conjunto con el Ministerio del Interior y las entidades responsables de la lucha frontal contra el terrorismo y el crimen organizado transnacional.",
                "La mesa directiva la completaron Patricia Chirinos (Renovación Popular) como vicepresidenta y Jorge Flores Ancachi (Podemos Perú) como secretario.",
                "Al asumir, Revilla dijo que la comisión buscaría hacer frente a la creciente amenaza de la delincuencia organizada y el terrorismo, que afectan la seguridad y el bienestar de la ciudadanía."],
         keys=["crimen1"], pend=""),
    dict(slug="crimen-organizado-sesion-descentralizada-piura-2025", tema="seguridad-ciudadana", hecho="7 de julio de 2025", iso="2025-07-07",
         h1="Crimen organizado: la comisión de Revilla sesionó en Piura",
         seo="Comisión contra el crimen sesiona en Piura",
         desc="El 7 de julio de 2025, la comisión contra el crimen organizado que presidía César Revilla sesionó en Piura con autoridades regionales.",
         resumen="La comisión sesionó en el Gobierno Regional de Piura para evaluar si declarar organizaciones terroristas a bandas como el Tren de Aragua.",
         paras=["El 7 de julio de 2025, la comisión especial contra el terrorismo y el crimen organizado transnacional, presidida por César Revilla, realizó su segunda sesión extraordinaria descentralizada en la sede del Gobierno Regional de Piura.",
                "La sesión analizó si bandas como el Tren de Aragua deben ser declaradas organizaciones terroristas internacionales. Las autoridades regionales plantearon, entre otras medidas, juzgados especializados, cárceles seguras, bloqueadores de señal en penales y un marco legal para el apoyo militar a la Policía.",
                "Revilla explicó que la comisión quería recoger información de las autoridades locales para evaluar la utilidad de esa declaratoria en la legislación y conocer cómo responden las entidades al aumento de la criminalidad."],
         keys=["crimen2"], pend=""),
    dict(slug="vocero-fuerza-popular-2024-2025", tema=None, hecho="Agosto de 2024 y agosto de 2025", iso="2025-08-07",
         h1="Revilla fue vocero de la bancada de Fuerza Popular",
         seo="Revilla, vocero de Fuerza Popular",
         desc="César Revilla fue primer vocero alterno de Fuerza Popular en 2024-2025 y, según Infobae, su portavoz principal para 2025-2026.",
         resumen="La bancada lo eligió primer vocero alterno en 2024 y, según Infobae, portavoz principal para el periodo 2025-2026.",
         paras=["El 9 de agosto de 2024, Keiko Fujimori informó que la bancada de Fuerza Popular eligió a César Revilla como primer vocero alterno para el periodo 2024-2025, con Arturo Alegría como vocero titular.",
                "El 7 de agosto de 2025, Infobae informó que César Revilla sería el nuevo portavoz principal de la bancada para el periodo 2025-2026.",
                "La vocería es la representación de la bancada ante la Junta de Portavoces, donde se coordina la agenda del Pleno."],
         keys=["vocero1", "vocero2"], pend=""),
    dict(slug="el-nino-2026-preparacion-piura", tema="lluvias-y-drenaje", hecho="22 de agosto de 2026", iso="2026-08-22",
         h1="El Niño 2026: Revilla pidió priorizar la preparación en Piura",
         seo="El Niño 2026: la postura de Revilla",
         desc="El 22 de agosto de 2026, el diputado César Revilla habló en RPP sobre la preparación frente a El Niño Costero y las acciones en Piura.",
         resumen="En RPP, Revilla sostuvo que faltó prevención y destacó acciones de preparación en Piura, como la descolmatación de un río.",
         paras=["El 22 de agosto de 2026, el diputado por Piura César Revilla habló en el programa Enfoque de los Sábados de RPP sobre El Niño Costero. Respaldó las acciones del Ejecutivo para mitigar sus efectos y sostuvo que el gobierno anterior no tomó medidas de prevención ni asignó presupuesto.",
                "Afirmó que el país está en una fase de preparación y anticipó un impacto fuerte. Sobre Piura, destacó un convenio entre el Ministerio de Desarrollo Agrario y Riego y una empresa privada para descolmatar un río, las campañas de vacunación del Ministerio de Salud y la maquinaria que pondría el gobierno regional."],
         keys=["rpp26"], pend=""),
    dict(slug="el-nino-2026-credito-suplementario-piura", tema="lluvias-y-drenaje", hecho="30 de julio de 2026", iso="2026-07-30",
         h1="El Niño 2026: Revilla informó S/ 300 millones para mitigación, con 60 a 70 para Piura",
         seo="El Niño 2026: recursos para Piura",
         desc="César Revilla informó en julio de 2026 que el crédito suplementario asignó S/ 300 millones para El Niño, de los cuales 60 a 70 millones irían a Piura.",
         resumen="Revilla explicó que el crédito suplementario destinó S/ 300 millones a mitigar El Niño, entre 60 y 70 millones de ellos para Piura.",
         paras=["El 30 de julio de 2026, César Revilla, entonces congresista y diputado electo por Piura, informó que el crédito suplementario aprobado por más de S/ 9 mil millones incluyó unos S/ 300 millones directos para enfrentar el Fenómeno El Niño. Según dijo, entre 60 y 70 millones de esa cifra irían a Piura.",
                "Explicó que la misma norma permite al Gobierno Regional y a los gobiernos locales reorientar hacia la emergencia los recursos ordinarios no comprometidos hasta el 31 de julio.",
                "Advirtió que el fenómeno podría ser de magnitud fuerte a extraordinaria y señaló que ya existían recursos para prepararse."],
         keys=["nino26"], pend="Enlazar el decreto o la ley del crédito suplementario y el monto final transferido a Piura (MEF)."),
    dict(slug="plan-hidraulico-piura-pl-7131", tema="agua-y-agro", hecho="24 de julio de 2025", iso="2025-07-24",
         h1="Plan Hidráulico de Piura: se aprobó el proyecto de Revilla que lo declara de interés nacional",
         seo="Plan Hidráulico de Piura (PL 7131)",
         desc="La Comisión Permanente aprobó por unanimidad el PL 7131 de César Revilla, que declara de interés nacional el Plan Hidráulico de Piura.",
         resumen="El PL 7131 de Revilla, que declara de interés nacional el Plan Hidráulico de Piura, se aprobó por unanimidad en segunda votación.",
         paras=["El 24 de julio de 2025, la Comisión Permanente del Congreso aprobó en segunda votación, por unanimidad (28 votos a favor), el texto sustitutorio del Proyecto de Ley 7131, de autoría del congresista César Revilla Villanueva (Fuerza Popular). La primera votación se realizó el 9 de junio.",
                "La iniciativa declara de interés nacional la formulación y aprobación del Plan Hidráulico de Piura, un instrumento de gestión multisectorial para el uso sostenible y eficiente del agua en la región.",
                "Un plan de este tipo ordena las inversiones en ríos, drenaje y riego, temas clave para Piura frente a El Niño y para su agricultura."],
         keys=["planhid"], pend="Agregar el número de ley con el que se publicó en El Peruano."),
    dict(slug="represa-tapa-de-cuy-sechura", tema="agua-y-agro", hecho="17 de noviembre de 2021", iso="2021-11-17",
         h1="Represa Tapa de Cuy en Sechura: Revilla respaldó el proyecto en la Comisión Agraria",
         seo="Represa Tapa de Cuy (Sechura)",
         desc="César Revilla respaldó en la Comisión Agraria la represa Tapa de Cuy, en Sechura, declarada luego de necesidad pública por la Ley 31413.",
         resumen="Revilla respaldó la represa Tapa de Cuy, que ampliaría la frontera agrícola en Sechura. La Ley 31413 la declaró de necesidad pública.",
         paras=["El 17 de noviembre de 2021, la Comisión Agraria aprobó por unanimidad el dictamen que declara de necesidad pública y preferente interés nacional el expediente técnico y la construcción del sistema de riego Tapa de Cuy, en el distrito de Cristo Nos Valga, provincia de Sechura. La autora de la iniciativa fue la congresista Cruz María Zeta (Fuerza Popular).",
                "En la sesión, César Revilla afirmó que la represa dinamizaría la economía de la zona, permitiría aprovechar mejor el agua en épocas de lluvia y aumentaría la actividad agrícola. Según la autora, el proyecto ampliaría la frontera agrícola en 3500 hectáreas.",
                "La norma se publicó como Ley 31413. En febrero de 2026, el programa Congreso en Regiones informó que el proyecto avanza con ese respaldo legal y que el MEF y el Ministerio de Desarrollo Agrario deben coordinar su ejecución con el gobierno regional."],
         keys=["tapacuy", "tapacuy2"], pend=""),
    dict(slug="reconstruccion-audiencia-alcaldes-piura-2022", tema="reconstruccion", hecho="21 de abril de 2022", iso="2022-04-21",
         h1="Reconstrucción: Revilla escuchó en Piura a los alcaldes que pedían presupuesto",
         seo="Audiencia de Reconstrucción con alcaldes",
         desc="El 21 de abril de 2022, la comisión de Reconstrucción presidida por César Revilla hizo en Piura su primera audiencia descentralizada con alcaldes.",
         resumen="En la primera audiencia descentralizada, los alcaldes pidieron al MEF recursos para obras de la Reconstrucción y Revilla se comprometió a impulsarlas.",
         paras=["El 21 de abril de 2022, la Comisión Especial Multipartidaria de Seguimiento al proceso de reconstrucción tras el Niño Costero, presidida por César Revilla, realizó en Piura su primera audiencia descentralizada.",
                "Alcaldes y funcionarios locales pidieron al Ministerio de Economía y Finanzas desembolsar recursos para proyectos ya aprobados por la Reconstrucción con Cambios. Revilla explicó que había obras en ejecución que necesitaban recursos para avanzar su valorización y otras sin observaciones, listas para recibir presupuesto.",
                "Se comprometió a seguir trabajando con las autoridades para sacar adelante los proyectos que necesita la población. Participaron también los congresistas Miguel Ciccia, Idelso García y Heidy Juárez."],
         keys=["alcaldes22"], pend=""),
    dict(slug="agenda-2026-2031-pobreza-seguridad", tema="seguridad-ciudadana", hecho="15 de agosto de 2026", iso="2026-08-15",
         h1="Su agenda 2026-2031: reducir la pobreza, seguridad y formalizar a las mypes",
         seo="Agenda de Revilla 2026-2031",
         desc="En agosto de 2026, el diputado César Revilla planteó reducir la pobreza a menos de 15%, endurecer la seguridad y apoyar a las mypes.",
         resumen="Revilla planteó bajar la pobreza de 26% a menos de 15% en cinco años, con más seguridad, compras rápidas para El Niño y apoyo a mypes.",
         paras=["En una entrevista con La Razón publicada el 15 de agosto de 2026, el diputado César Revilla planteó como meta reducir la pobreza de 26% a menos de 15% en el periodo 2026-2031, mejorando y ampliando los programas sociales que funcionan.",
                "En seguridad ciudadana propuso reformas para endurecer el régimen penitenciario y patrullajes conjuntos de la Policía y las Fuerzas Armadas en zonas identificadas por inteligencia, dentro de los estados de emergencia.",
                "Frente a El Niño, propuso marcos especiales de compra para adquirir con rapidez coberturas térmicas y alimento para el ganado, con un control propositivo de la Contraloría. También planteó una Sunat que acompañe la formalización de micro y pequeñas empresas, y abrir mercados para los agroexportadores."],
         keys=["razon26"], pend=""),
    dict(slug="balance-comision-economia-2023-2024", tema="economia-y-empleo", hecho="9 de julio de 2024", iso="2024-07-09",
         h1="Comisión de Economía 2023-2024: 58 dictámenes y 20 leyes bajo la presidencia de Revilla",
         seo="Comisión de Economía: 20 leyes en 2023-2024",
         desc="Con César Revilla como presidente, la Comisión de Economía del Congreso aprobó 58 dictámenes y logró 20 leyes: AFP, CTS, Fonavi, mypes y contrataciones.",
         resumen="Bajo su presidencia, la comisión evaluó 268 proyectos, aprobó 58 dictámenes y logró 20 leyes para trabajadores, pensionistas y mypes.",
         paras=["El 9 de julio de 2024, la Comisión de Economía, Banca, Finanzas e Inteligencia Financiera, presidida por César Revilla, presentó el balance del periodo 2023-2024: 58 dictámenes aprobados tras evaluar 268 proyectos de ley, y 20 leyes oficializadas.",
                "Entre las leyes destacadas figuran la Ley 32002, que permitió retirar hasta 4 UIT de las AFP; la Ley 32027, que liberó el 100% de la CTS; la Ley 31888, que creó el régimen de reprogramación de aportes previsionales (REPRO AFP III), y la Ley 31886, que promueve la competencia en el transporte terrestre.",
                "La comisión también aprobó el marco para reiniciar la devolución de aportes a los fonavistas, una nueva Ley de Contrataciones del Estado, que no se modificaba en más de 20 años, y facilidades para que las mypes cobren a tiempo.",
                "La comisión realizó 15 sesiones ordinarias, 19 extraordinarias, 9 descentralizadas y 4 audiencias públicas, entre ellas una en Puinahua, Loreto, sobre la distribución del canon petrolero."],
         keys=["econbal"], pend=""),
    dict(slug="retiro-afp-2024-ley-32002", tema="economia-y-empleo", hecho="25 de marzo de 2024", iso="2024-03-25",
         h1="Retiro de AFP 2024: la comisión de Revilla aprobó hasta 4 UIT para todos los afiliados",
         seo="Retiro AFP 2024 hasta 4 UIT (Ley 32002)",
         desc="La Comisión de Economía que presidía César Revilla aprobó en 2024 el retiro de hasta 4 UIT de las AFP para todos los afiliados. Hoy es la Ley 32002.",
         resumen="El dictamen del séptimo retiro de AFP, de hasta 4 UIT y para todos los afiliados, se aprobó en la comisión de Revilla con 17 votos.",
         paras=["El 25 de marzo de 2024, la Comisión de Economía, presidida por César Revilla, aprobó con 17 votos a favor el dictamen que permitió un nuevo retiro de fondos de las AFP de hasta 4 UIT (S/ 20 600), en cuatro cuotas.",
                "El texto amplió el alcance de la propuesta inicial, que solo cubría a afiliados desempleados, para que el retiro alcance a todos los afiliados. Revilla anticipó que el dictamen llegaría al Pleno entre fines de abril e inicios de mayo.",
                "La medida se publicó como Ley 32002, que autorizó el retiro extraordinario y facultativo de hasta cuatro UIT del Sistema Privado de Pensiones."],
         keys=["afp24", "econbal"], pend=""),
    dict(slug="mypes-detracciones-ley-por-insistencia-2023", tema="economia-y-empleo", hecho="12 de octubre de 2023", iso="2023-10-12",
         h1="Mypes: el Congreso aprobó por insistencia el uso libre de sus fondos de detracciones",
         seo="Mypes y detracciones: ley por insistencia",
         desc="En octubre de 2023, con César Revilla al frente de la Comisión de Economía, el Congreso aprobó por insistencia que las mypes usen sus fondos de detracciones.",
         resumen="El Pleno aprobó por insistencia, con 89 votos, que las mypes dispongan temporalmente de sus fondos de detracciones.",
         paras=["El 12 de octubre de 2023, el Pleno del Congreso aprobó por insistencia, con 89 votos a favor, la propuesta que permite a las micro y pequeñas empresas disponer libremente, de manera temporal, de los fondos de sus cuentas de detracciones, y actualiza el Sistema de Pago de Obligaciones Tributarias (SPOT).",
                "La Comisión de Economía, presidida por César Revilla, respaldó la insistencia tras evaluar las observaciones del Ejecutivo. El objetivo es fortalecer la capacidad financiera de las mypes y apoyar la reactivación económica.",
                "La iniciativa se basó en los proyectos de ley 2035/2021-CR y 4117/2022-CR."],
         keys=["mypes23"], pend=""),
    dict(slug="sector-textil-competitividad-2023", tema="economia-y-empleo", hecho="16 de octubre de 2023", iso="2023-10-16",
         h1="Sector textil: la Comisión de Economía aprobó incentivos para reactivar el empleo",
         seo="Sector textil: incentivos aprobados en 2023",
         desc="En octubre de 2023, la Comisión de Economía presidida por César Revilla aprobó un dictamen para impulsar la competitividad y el empleo del sector textil.",
         resumen="El dictamen propone un crédito tributario por reinversión de utilidades para la industria textil y de confecciones.",
         paras=["El 16 de octubre de 2023, la Comisión de Economía, presidida por César Revilla, aprobó un dictamen para impulsar la competitividad y el empleo en los sectores textil y de confecciones, y fomentar su reactivación económica.",
                "La propuesta plantea un programa excepcional y temporal de crédito tributario por reinversión de utilidades, equivalente al 50% de lo reinvertido en infraestructura, maquinaria y equipos.",
                "El dictamen reunió los proyectos 1567/2021, 3821/2022-PE, 4355/2022, 5118/2022 y 5380/2022-PE."],
         keys=["textil23"], pend=""),
    dict(slug="regimen-excepcional-impuesto-renta-2024", tema="economia-y-empleo", hecho="12 de junio de 2024", iso="2024-06-12",
         h1="Formalización: Revilla sustentó el régimen excepcional del Impuesto a la Renta",
         seo="Régimen excepcional del Impuesto a la Renta",
         desc="En junio de 2024, César Revilla sustentó en el Pleno el régimen excepcional del Impuesto a la Renta, aprobado con 104 votos para ampliar la base tributaria.",
         resumen="El Pleno aprobó con 104 votos el régimen que busca formalizar rentas no declaradas y ampliar la base tributaria.",
         paras=["El 12 de junio de 2024, César Revilla sustentó en nombre de la Comisión de Economía el dictamen del Proyecto de Ley 7536/2023-CR, que propone un régimen excepcional del Impuesto a la Renta.",
                "La propuesta busca formalizar la economía y ampliar la base tributaria respecto de rentas no declaradas al 31 de diciembre de 2022, con una tasa preferencial que también incentive la repatriación de capitales.",
                "El Pleno la aprobó con 104 votos a favor, 6 en contra y 7 abstenciones."],
         keys=["ir24"], pend=""),
    dict(slug="proyectos-2025-2026-salud-emergencias-titulos-rurales", folder="proyectos-de-ley", tema="salud", hecho="Octubre de 2025 a septiembre de 2026", iso="2026-09-06",
         h1="Sus proyectos recientes: salud en emergencias, títulos rurales y trabajo social",
         seo="Proyectos de César Revilla 2025-2026",
         desc="Los proyectos de ley recientes de César Revilla: acceso inmediato a salud en emergencias, formalización de títulos rurales, trabajadores sociales y personeros.",
         resumen="Su primer proyecto como diputado garantiza la atención inmediata en emergencias de salud. Antes impulsó la titulación rural y el trabajo social en empresas.",
         paras=["Como diputado del periodo 2026-2031, César Revilla presentó el 6 de septiembre de 2026 el Proyecto de Ley 00150/2026-2031-CD, que garantiza el acceso inmediato a los servicios de salud en emergencias para toda persona. Se encuentra en comisión.",
                "En la etapa final de su periodo como congresista presentó otras tres iniciativas: el PL 13397/2025-CR (27 de noviembre de 2025), que promueve la formalización de la propiedad agraria para que los gobiernos regionales financien mejor la inscripción de títulos de propiedad rural; el PL 12718/2025-CR (8 de octubre de 2025), que fomenta que las empresas públicas y privadas con más de 100 trabajadores contraten trabajadores sociales; y el PL 14091/2025-CR (26 de febrero de 2026), que otorga un día no laborable compensable a los personeros de mesa de las Elecciones Generales 2026 y que cuenta con dictamen.",
                "Según el mismo registro, a lo largo de su labor parlamentaria presentó 46 proyectos de ley, de los cuales 21 se convirtieron en ley."],
         keys=["vbp"], pend="Enlazar el expediente de cada proyecto en el portal del Congreso."),
    dict(slug="pl-2902-2022-cr", folder="proyectos-de-ley", tema="educacion", hecho="Presentado en 2022", iso=None,
         h1="Proyecto de Ley 2902/2022-CR: bachiller sin trabajo de investigación obligatorio",
         seo="Proyecto de Ley 2902/2022-CR (bachiller)",
         desc="El PL 2902/2022-CR, presentado por César Revilla, propone modificar la Ley Universitaria para que el grado de bachiller no exija un trabajo de investigación.",
         resumen="Propone que la aprobación de un trabajo de investigación deje de ser requisito obligatorio para obtener el grado de bachiller.",
         paras=["El congresista César Revilla Villanueva, del grupo parlamentario Fuerza Popular, presentó el Proyecto de Ley 2902/2022-CR.",
                "La iniciativa propone modificar el artículo 45.1 de la Ley 30220, Ley Universitaria, para excluir como requisito obligatorio, para obtener el grado de bachiller, la aprobación de un trabajo de investigación.",
                "Estado del proyecto: por confirmar en el sistema de seguimiento del Congreso."],
         keys=["pl2902"], pend="Consultar el expediente en el Congreso y agregar estado, comisión, dictamen y fecha de presentación."),
    dict(slug="puente-carnero-descolmatacion-tambogrande-las-lomas", tema="lluvias-y-drenaje", hecho="14 de octubre de 2026", iso="2026-10-14",
         h1="Puente Carnero: Revilla gestiona la descolmatación entre Las Lomas y Tambogrande",
         seo="Puente Carnero: descolmatación en Piura",
         desc="César Revilla recorrió el puente Carnero y gestionó ante el Midagri y la ANA la descolmatación de siete kilómetros para proteger parcelas y la carretera.",
         resumen="Revilla recorrió el puente Carnero y gestionó ante el Midagri y la ANA la intervención de unos siete kilómetros pendientes de descolmatación.",
         paras=["El 14 de octubre de 2026, el Congreso informó que el diputado César Revilla recorrió el puente Carnero, ubicado entre los distritos de Las Lomas y Tambogrande, en Piura.",
                "Durante la visita constató que aún quedan tramos pendientes de descolmatación. Gestionó ante el Ministerio de Desarrollo Agrario y Riego (Midagri) y la Autoridad Nacional del Agua (ANA) la intervención de unos siete kilómetros.",
                "El objetivo es proteger las parcelas agrícolas y prevenir afectaciones en la carretera Tambogrande-Las Lomas."],
         keys=["congreso1014"], pend="Agregar el oficio enviado al Midagri y a la ANA, y el avance de la intervención con fecha."),
    dict(slug="sullana-evacuacion-aerea-nina-insn-san-borja", tema="salud", hecho="18 de noviembre de 2026", iso="2026-11-18", pub="2026-11-18",
         h1="Sullana: Revilla coordinó la evacuación aérea de una niña a Lima",
         seo="Evacuación aérea de niña de Sullana a Lima",
         desc="César Revilla informó que su despacho coordinó con el SAMU y el Ministerio de Defensa la evacuación aérea de una niña de Sullana al INSN San Borja.",
         resumen="El despacho de Revilla coordinó con el SAMU y el Ministerio de Defensa el traslado aéreo urgente de una niña desde Sullana al INSN San Borja, en Lima.",
         paras=["El 18 de noviembre de 2026, el diputado César Revilla informó en su página oficial de Facebook que su despacho coordinó con el Servicio de Atención Móvil de Urgencias (SAMU) y el Ministerio de Defensa la evacuación aérea de una niña que necesitaba ser trasladada con urgencia desde Sullana a Lima.",
                "Según la publicación, el despacho se sumó al trabajo que venía realizando el Hospital de Especialidades Sullana para conseguir el traslado. La menor fue llevada al Instituto Nacional de Salud del Niño San Borja (INSN San Borja), en Lima, donde continúa recibiendo atención.",
                "Revilla se encontraba en el Congreso mientras se gestionaba la evacuación. «Cuando se trata de salvar una vida, no existen horarios, distancias ni trámites que puedan esperar», escribió.",
                "Revilla conoce de cerca el hospital: según su hoja de vida declarada al JNE, fue director del Hospital de Sullana entre 2015 y 2016. Por respeto a la menor y a su familia, esta ficha no publica sus datos personales."],
         keys=["fb1118", "eclara"], pend="Agregar la nota oficial del SAMU, el Minsa o el Hospital de Sullana cuando se publique, y una foto autorizada."),
]
for f in FICHAS:
    f.setdefault("folder", "gestion")
    f["path"] = f"{f['folder']}/{f['slug']}.html"

# ---------- Guías ciudadanas ----------
DIP_ROWS = [
    ("César Revilla", "Fuerza Popular", "23,816"),
    ("Eduardo Castillo", "No indicado en la fuente (reelecto)", "21,130"),
    ("Félix Chang", "Renovación Popular", "13,945"),
    ("Carmela Paucará", "Fuerza Popular", "7,896"),
    ("María Silupú", "Fuerza Popular", "5,298"),
    ("Miguel Huamán", "Partido del Buen Gobierno", "5,191"),
    ("Henry Albañil", "Partido Cívico OBRAS", "5,049"),
]
dip_table = ("<table><thead><tr><th>#</th><th>Diputado</th><th>Partido</th><th>Votos preferenciales</th></tr></thead><tbody>"
             + "".join(f"<tr><td>{i}</td><td>{n}</td><td>{p}</td><td>{v}</td></tr>" for i, (n, p, v) in enumerate(DIP_ROWS, 1))
             + "</tbody></table>")

GUIAS = [
    dict(slug="diputados-de-piura-2026-2031", iso=PUB,
         h1="Diputados de Piura 2026–2031: quiénes son y cuántos votos obtuvieron",
         seo="Diputados de Piura 2026–2031: quiénes son",
         desc="Los siete diputados de Piura para 2026–2031, con partido y votos preferenciales, y la senadora regional. Datos del JNE y de la prensa.",
         resumen="Piura eligió siete diputados para 2026–2031. César Revilla encabezó la votación con 23,816 votos preferenciales.",
         card="Lista completa, partidos y votos.",
         html=f"""<h2>Lista de diputados por Piura</h2>
{dip_table}
<p class="upd">Votos y partidos según la nota de El Tiempo del 27 de junio de 2026; el partido de César Revilla, según Canal N.</p>
<h2>Cómo se entregaron las credenciales</h2>
<p>El Jurado Nacional de Elecciones entregó las credenciales a los representantes de Piura el viernes 26 de junio de 2026, para el periodo 2026–2031. Según la nota, Fuerza Popular obtuvo cuatro de las siete curules.</p>
<h2>Senadora por Piura</h2>
<p>Piura tiene una representante en el Senado: Karla Schaefer, de Fuerza Popular, acreditada previamente por el JNE.</p>
<h2>Más información</h2>
<p>Conoce <a href="~/guias/que-hace-un-diputado-del-peru.html">qué hace un diputado</a> y <a href="~/gestion/revilla-lidera-votacion-piura-2026.html">cómo fue la votación de César Revilla</a>.</p>""",
         keys=["acred", "canaln"]),
    dict(slug="que-hace-un-diputado-del-peru", iso=PUB,
         h1="Qué hace un diputado en el Perú: funciones de la Cámara de Diputados",
         seo="Qué hace un diputado del Perú: funciones",
         desc="Funciones de la Cámara de Diputados del Perú y diferencias con el Senado, en el Congreso bicameral que inició funciones el 27 de julio de 2026.",
         resumen="Desde el 27 de julio de 2026 el Congreso es bicameral: los diputados presentan y aprueban leyes y ejercen control político.",
         card="Funciones de la Cámara de Diputados y del Senado.",
         html="""<h2>Un Congreso con dos cámaras</h2>
<p>Las nuevas autoridades asumieron funciones el 27 de julio de 2026. El Senado tiene como mínimo 60 senadores y la Cámara de Diputados, al menos 130 diputados. Ambas cámaras fueron elegidas por voto popular para ejercer funciones durante cinco años.</p>
<h2>Funciones de la Cámara de Diputados</h2>
<ul class="clean">
<li>Presentar, debatir, aprobar, modificar y derogar proyectos de ley. Todo proyecto ingresa primero a esta cámara.</li>
<li>Ejercer control político mediante pedidos de información, citaciones, interpelaciones, estaciones de preguntas y censuras a ministros.</li>
<li>Admitir e investigar denuncias constitucionales y poder iniciar acusaciones constitucionales.</li>
<li>Citar y exigir información a gobernadores regionales, según el artículo 145 de su reglamento.</li>
</ul>
<h2>Funciones del Senado</h2>
<ul class="clean">
<li>Revisar, aprobar, modificar o rechazar los proyectos enviados por la Cámara de Diputados.</li>
<li>Ejercer control político sobre determinados actos normativos del Poder Ejecutivo.</li>
<li>Resolver las acusaciones constitucionales presentadas por la Cámara de Diputados.</li>
<li>Elegir, ratificar, designar o remover altas autoridades, como magistrados del Tribunal Constitucional, el Defensor del Pueblo, el Contralor General y directores del Banco Central de Reserva.</li>
</ul>
<h2>Y en Piura</h2>
<p>Piura tiene siete diputados y una senadora. Mira la <a href="~/guias/diputados-de-piura-2026-2031.html">lista completa con sus votos</a>.</p>""",
         keys=["bicam"]),
    dict(slug="semana-de-representacion-que-es", iso=PUB,
         h1="Semana de Representación: qué es y cómo se vive en Piura",
         seo="Semana de Representación: qué es",
         desc="Qué es la Semana de Representación del Congreso, qué hacen los parlamentarios en sus regiones y cómo plantear tu caso al despacho de César Revilla.",
         resumen="Es el periodo en que los parlamentarios regresan a sus regiones para escuchar a la ciudadanía, recibir denuncias y fiscalizar.",
         card="Qué hacen los parlamentarios cuando vuelven a la región.",
         html="""<h2>Qué es</h2>
<p>La Semana de Representación es el periodo en que los parlamentarios regresan a sus regiones. Durante esa semana escuchan a la ciudadanía, reciben denuncias, fiscalizan a las autoridades y rinden cuentas sobre su labor. El Congreso la presenta como un momento para fortalecer el vínculo con la población.</p>
<h2>Un ejemplo en Piura</h2>
<p>Siendo presidente de la Comisión de Seguimiento a la Reconstrucción con Cambios, César Revilla se reunió en Piura con autoridades locales y evaluó los sistemas de salud como parte de su Semana de Representación. Más en la <a href="~/gestion/comision-reconstruccion-nino-costero.html">ficha de la comisión</a>.</p>
<h2>Cómo plantear tu caso</h2>
<p>Si quieres que el despacho de César Revilla conozca un problema de tu distrito, escríbenos desde la página de <a href="~/contacto.html">contacto</a> indicando la provincia y el tema.</p>
<p class="upd">Para ver otras guías sobre el Congreso, revisa <a href="~/guias/que-hace-un-diputado-del-peru.html">qué hace un diputado</a>.</p>
PEND_SEMANA""",
         keys=["semana", "radio"], pend="Publicar el calendario de las próximas semanas de representación (fecha, provincia y actividades) y confirmar el canal oficial para recibir casos."),
    dict(slug="que-ha-hecho-cesar-revilla-por-piura", iso=PUB,
         h1="¿Qué ha hecho César Revilla por Piura? Sus principales gestiones",
         seo="¿Qué ha hecho César Revilla por Piura?",
         desc="Resumen con fuentes de lo que ha hecho César Revilla por Piura: Universidad de Huancabamba, Plan Hidráulico, El Niño, reconstrucción, salud y seguridad.",
         resumen="Universidad de Huancabamba, Plan Hidráulico de Piura, recursos ante El Niño, reconstrucción y sesiones del Congreso en la región.",
         card="Sus gestiones por Piura, en un solo lugar.",
         html="""<h2>Educación</h2>
<p>Es autor del proyecto que dio origen a la <a href="~/gestion/universidad-nacional-de-huancabamba-ley-32162.html">Ley 32162, que crea la Universidad Nacional de Huancabamba</a>, aprobada por el Pleno con 75 votos en 2024.</p>
<h2>Agua y agricultura</h2>
<p>Su proyecto que declara de interés nacional el <a href="~/gestion/plan-hidraulico-piura-pl-7131.html">Plan Hidráulico de Piura</a> se aprobó por unanimidad en 2025. También respaldó la <a href="~/gestion/represa-tapa-de-cuy-sechura.html">represa Tapa de Cuy en Sechura</a>, que ampliaría la frontera agrícola en 3500 hectáreas.</p>
<h2>Fenómeno El Niño y lluvias</h2>
<p>En 2026 informó que el crédito suplementario destinó <a href="~/gestion/el-nino-2026-credito-suplementario-piura.html">S/ 300 millones para mitigar El Niño, de los cuales entre 60 y 70 irían a Piura</a>, y pidió un <a href="~/gestion/drenaje-pluvial-piura-fenomeno-el-nino.html">sistema integral de drenaje pluvial</a> para la región. Lee la guía <a href="~/guias/cesar-revilla-fenomeno-el-nino.html">César Revilla y el Fenómeno El Niño</a>.</p>
<h2>Reconstrucción</h2>
<p>Presidió la <a href="~/gestion/comision-reconstruccion-nino-costero.html">comisión de seguimiento a la Reconstrucción</a>, llevó una <a href="~/gestion/reconstruccion-audiencia-alcaldes-piura-2022.html">audiencia con los alcaldes de Piura</a> para destrabar recursos y propuso sesionar en el <a href="~/gestion/km-980-sesion-descentralizada-reconstruccion.html">km 980</a>, con los damnificados del Niño Costero.</p>
<h2>Salud</h2>
<p>Defendió el <a href="~/gestion/hospital-alta-complejidad-piura.html">Hospital de Alta Complejidad de Piura</a> y es autor del <a href="~/gestion/cas-covid-pl-2204-personal-de-salud.html">proyecto CAS COVID</a> para el personal de salud, aprobado con 112 votos.</p>
<h2>Seguridad y presupuesto</h2>
<p>Llevó a Piura la <a href="~/gestion/crimen-organizado-sesion-descentralizada-piura-2025.html">comisión contra el crimen organizado</a> que presidía y la <a href="~/gestion/comision-economia-sesion-descentralizada-piura.html">Comisión de Economía</a>. También alertó sobre un <a href="~/gestion/presupuesto-piura-recorte-mef.html">intento de recorte del presupuesto regional</a>.</p>
<h2>Por provincia</h2>
<p>Revisa las gestiones en <a href="~/piura/provincia-de-piura.html">Piura</a>, <a href="~/piura/huancabamba.html">Huancabamba</a> y <a href="~/piura/sechura.html">Sechura</a>, o mira <a href="~/cifras.html">todo en cifras</a>.</p>""",
         keys=["huanca1", "planhid", "nino26", "alcaldes22", "cas", "crimen2"]),
    dict(slug="cesar-revilla-fenomeno-el-nino", iso=PUB,
         h1="César Revilla y el Fenómeno El Niño: lo que ha planteado y logrado",
         seo="César Revilla y el Fenómeno El Niño",
         desc="Lo que ha hecho César Revilla frente al Fenómeno El Niño en Piura: recursos en 2026, drenaje pluvial, apoyo al Ejecutivo en 2023 y la reconstrucción.",
         resumen="Desde 2021 sigue la reconstrucción del Niño Costero y en 2023 y 2026 impulsó recursos y medidas para enfrentar El Niño en Piura.",
         card="Recursos, drenaje y reconstrucción frente a El Niño.",
         html="""<h2>2026: recursos y preparación</h2>
<p>En julio de 2026 informó que el crédito suplementario aprobado incluyó <a href="~/gestion/el-nino-2026-credito-suplementario-piura.html">unos S/ 300 millones directos para mitigar El Niño, de los cuales entre 60 y 70 millones irían a Piura</a>, y que los gobiernos regionales y locales podían reorientar recursos ordinarios no comprometidos hacia la emergencia. En agosto, en RPP, insistió en <a href="~/gestion/el-nino-2026-preparacion-piura.html">priorizar la preparación</a>. En agosto también propuso <a href="~/gestion/agenda-2026-2031-pobreza-seguridad.html">compras rápidas de coberturas térmicas y alimento para ganado</a> en zonas afectadas.</p>
<h2>Drenaje pluvial para Piura</h2>
<p>En octubre de 2026 advirtió que las lluvias evidenciaron la vulnerabilidad de la región y pidió un <a href="~/gestion/drenaje-pluvial-piura-fenomeno-el-nino.html">sistema integral de drenaje pluvial</a>, con el perfil ya culminado por la Autoridad Nacional de Infraestructura.</p>
<h2>Agua y ríos</h2>
<p>Su proyecto del <a href="~/gestion/plan-hidraulico-piura-pl-7131.html">Plan Hidráulico de Piura</a>, aprobado por unanimidad, ordena las inversiones en ríos, drenaje y riego.</p>
<h2>2023: la Comisión de Economía frente a El Niño</h2>
<p>Como presidente de la Comisión de Economía, ofreció <a href="~/gestion/el-nino-2023-comision-economia-facilidades.html">eliminar las trabas para que el Ejecutivo atendiera a la población vulnerable</a> y respaldó el crédito suplementario para la emergencia.</p>
<h2>Reconstrucción tras el Niño Costero</h2>
<p>Presidió la <a href="~/gestion/comision-reconstruccion-nino-costero.html">comisión de seguimiento a la Reconstrucción con Cambios</a> y escuchó en Piura a los <a href="~/gestion/reconstruccion-audiencia-alcaldes-piura-2022.html">alcaldes que pedían presupuesto</a> para obras pendientes.</p>
<p class="upd">Más en el tema <a href="~/temas/lluvias-y-drenaje.html">Lluvias y drenaje pluvial en Piura</a>.</p>""",
         keys=["nino26", "rpp26", "dren", "planhid", "candados", "alcaldes22"]),
    dict(slug="como-pedir-informacion-publica-peru", iso=PUB,
         h1="Cómo pedir información pública a una entidad del Estado en el Perú",
         seo="Cómo pedir información pública en el Perú",
         desc="Guía práctica para solicitar información pública a una entidad: dónde presentar el pedido, plazo de respuesta de 10 días hábiles y costos de reproducción.",
         resumen="Cualquier persona puede pedir información pública a una entidad. La respuesta debe darse en 10 días hábiles, según el DL 1353.",
         card="Pasos, plazos y costos para pedir información a una entidad.",
         html="""<h2>Paso a paso</h2>
<ol class="clean">
<li><strong>Identifica la entidad</strong> que tiene la información (municipalidad, gobierno regional, ministerio, hospital).</li>
<li><strong>Presenta la solicitud</strong> por el formulario virtual de la entidad, por correo electrónico (si lo habilita) o en su mesa de partes. Describe con precisión qué documento o dato necesitas.</li>
<li><strong>Espera la respuesta:</strong> la solicitud debe atenderse en un plazo de diez (10) días hábiles desde su presentación, según el Decreto Legislativo 1353 y su reglamento.</li>
</ol>
<h2>Si piden más tiempo</h2>
<p>La prórroga es excepcional. Solo procede si cumplir el plazo es materialmente imposible por falta comprobada de capacidad logística, operativa o de recursos humanos, o por un volumen significativo de información. La entidad debe comunicarlo, por única vez y de forma fundamentada, dentro de los dos (2) días hábiles de recibida la solicitud.</p>
<h2>Cuánto cuesta</h2>
<p>Solo se cobra el costo de reproducción, según el TUPA de cada entidad. Como ejemplo, la Biblioteca Nacional cobra S/ 0.10 por folio de copia simple y S/ 1.00 por CD, y el envío por correo es gratuito. Confirma el costo en la entidad a la que pidas la información.</p>
<h2>Si no te responden</h2>
<p>Consulta en gob.pe los recursos disponibles ante la autoridad de transparencia y acceso a la información pública.</p>
<h2>Relacionado</h2>
<p>La sección de <a href="~/transparencia.html">transparencia</a> reúne las fuentes oficiales sobre la labor de César Revilla.</p>""",
         keys=["bn", "gobpe"], pend="Confirmar si el despacho ofrecerá orientación a vecinos para estos pedidos; de ser así, agregar el canal."),
    dict(slug="fuerza-popular-congreso-2026-2031", iso=PUB,
         h1="Fuerza Popular en el Congreso 2026–2031: cuántos diputados y senadores tiene",
         seo="Fuerza Popular en el Congreso 2026–2031",
         desc="Fuerza Popular tiene 41 de 130 diputados y 22 de 60 senadores. Voceros, bancada y los diputados de Piura, entre ellos César Revilla.",
         resumen="Según el conteo final de la ONPE, Fuerza Popular obtuvo 41 de los 130 diputados y 22 de los 60 senadores, la mayor bancada de ambas cámaras.",
         card="Bancada, voceros y representantes de Piura.",
         faq=[("¿Cuántos diputados tiene Fuerza Popular?", "41 de los 130 diputados, según el conteo al 100% de la ONPE publicado por Infomercado el 17 de junio de 2026."),
              ("¿Cuántos senadores tiene Fuerza Popular?", "22 de los 60 senadores, según la misma fuente."),
              ("¿Quiénes son los voceros de Fuerza Popular en el Congreso?", "En la Cámara de Diputados, Cecilia Chacón es la vocera titular y Arturo Alegría el alterno. En el Senado, Patricia Juárez es la vocera principal y Víctor Flores el alterno, según Gestión (11 de julio de 2026)."),
              ("¿Qué diputados de Fuerza Popular hay por Piura?", "Fuerza Popular obtuvo cuatro de las siete curules de Piura. César Revilla encabezó la votación regional con 23,816 votos preferenciales, y la senadora Karla Schaefer también es de Fuerza Popular.")],
         html=f"""<h2>Así quedó el reparto de curules</h2>
<table><thead><tr><th>Partido</th><th>Diputados (de 130)</th><th>Senadores (de 60)</th><th>Total</th></tr></thead><tbody>
<tr><td>Fuerza Popular</td><td>41</td><td>22</td><td>63</td></tr>
<tr><td>Juntos por el Perú</td><td>32</td><td>14</td><td>46</td></tr>
<tr><td>Partido del Buen Gobierno</td><td>18</td><td>7</td><td>25</td></tr>
<tr><td>Renovación Popular</td><td>15</td><td>8</td><td>23</td></tr>
<tr><td>Partido Cívico Obras</td><td>14</td><td>5</td><td>19</td></tr>
<tr><td>Ahora Nación</td><td>10</td><td>4</td><td>14</td></tr>
</tbody></table>
<p class="upd">Cifras del conteo al 100% de la ONPE (13 de junio de 2026), según Infomercado.</p>
<h2>Voceros de la bancada</h2>
<p>El 11 de julio de 2026 Fuerza Popular designó a Cecilia Chacón como vocera en la Cámara de Diputados, con Arturo Alegría como alterno, y a Patricia Juárez como vocera en el Senado, con Víctor Flores como alterno.</p>
<h2>César Revilla en la bancada</h2>
<p>César Revilla es diputado por Piura de Fuerza Popular para 2026–2031. El 1 de octubre de 2026, Infobae lo presentó como vocero de la bancada de diputados al informar su posición sobre el <a href="~/guias/facultades-legislativas-2026-cesar-revilla.html">pedido de facultades legislativas</a>. El 14 de octubre, el Congreso informó que <a href="~/gestion/puente-carnero-descolmatacion-tambogrande-las-lomas.html">recorrió el puente Carnero y gestionó la descolmatación pendiente</a> ante el Midagri y la ANA.</p>
<h2>La Mesa Directiva</h2>
<p>La Cámara de Diputados eligió presidente a Oscar Reto Otero, del Partido del Buen Gobierno, con 74 votos para la lista 1. Antes de la elección, César Revilla dijo que su bancada aún no definía si buscaría presidir la Mesa.</p>
<h2>Más información</h2>
<p>Revisa cómo está conformado el <a href="~/guias/congreso-bicameral-peru-2026-2031.html">Congreso bicameral</a> y quiénes son los <a href="~/guias/diputados-de-piura-2026-2031.html">diputados de Piura</a>.</p>""",
         keys=["infomercado26", "gestionvoc", "reto", "canaln26", "infobae1001", "congreso1014", "acred"]),
    dict(slug="congreso-bicameral-peru-2026-2031", iso=PUB,
         h1="Congreso bicameral del Perú 2026–2031: cómo está conformado",
         seo="Congreso bicameral del Perú 2026–2031",
         desc="El Congreso del Perú 2026–2031 tiene 60 senadores y 130 diputados. Reparto por partido, Mesa Directiva y qué cambia con la bicameralidad.",
         resumen="Desde el 27 de julio de 2026 el Congreso peruano tiene dos cámaras: 60 senadores y 130 diputados, elegidos por cinco años.",
         card="Senadores, diputados y reparto por partido.",
         faq=[("¿Cuántos congresistas tiene el Perú desde 2026?", "190 parlamentarios: 60 senadores y 130 diputados."),
              ("¿Desde cuándo es bicameral el Congreso del Perú?", "Desde el 27 de julio de 2026, cuando asumieron las nuevas autoridades, según Diario Correo."),
              ("¿Quién preside la Cámara de Diputados?", "Oscar Reto Otero, del Partido del Buen Gobierno, elegido con 74 votos para el periodo 2026–2027."),
              ("¿Cuánto dura el mandato de un diputado o senador?", "Cinco años: 2026–2031.")],
         html="""<h2>Dos cámaras, 190 parlamentarios</h2>
<p>El Congreso de la República dejó de ser unicameral el 27 de julio de 2026. La Cámara de Diputados tiene 130 miembros y el Senado, 60. Ambas cámaras fueron elegidas por voto popular para el periodo 2026–2031.</p>
<h2>Reparto por partido</h2>
<table><thead><tr><th>Partido</th><th>Diputados</th><th>Senadores</th></tr></thead><tbody>
<tr><td>Fuerza Popular</td><td>41</td><td>22</td></tr>
<tr><td>Juntos por el Perú</td><td>32</td><td>14</td></tr>
<tr><td>Partido del Buen Gobierno</td><td>18</td><td>7</td></tr>
<tr><td>Renovación Popular</td><td>15</td><td>8</td></tr>
<tr><td>Partido Cívico Obras</td><td>14</td><td>5</td></tr>
<tr><td>Ahora Nación</td><td>10</td><td>4</td></tr>
</tbody></table>
<p class="upd">Conteo al 100% de la ONPE, según Infomercado (17 de junio de 2026). Se listan los seis partidos con mayor representación.</p>
<h2>Mesa Directiva de Diputados</h2>
<p>Oscar Reto Otero, del Partido del Buen Gobierno, fue elegido presidente de la Cámara de Diputados para 2026–2027 con 74 votos.</p>
<h2>Qué hace cada cámara</h2>
<p>Lee <a href="~/guias/que-hace-un-diputado-del-peru.html">qué hace un diputado</a> y <a href="~/guias/que-hace-un-senador-del-peru.html">qué hace un senador</a>. Para ver la bancada más numerosa, consulta <a href="~/guias/fuerza-popular-congreso-2026-2031.html">Fuerza Popular en el Congreso</a>.</p>""",
         keys=["infomercado26", "bicam", "reto"]),
    dict(slug="que-hace-un-senador-del-peru", iso=PUB,
         h1="Qué hace un senador en el Perú y en qué se diferencia de un diputado",
         seo="Qué hace un senador del Perú: funciones",
         desc="Funciones del Senado del Perú: revisa leyes, resuelve acusaciones constitucionales y elige altas autoridades. Diferencias con la Cámara de Diputados.",
         resumen="El Senado revisa las leyes que aprueba Diputados, resuelve las acusaciones constitucionales y elige o ratifica a altas autoridades del Estado.",
         card="Funciones del Senado y diferencias con Diputados.",
         faq=[("¿Qué hace un senador en el Perú?", "Revisa, aprueba, modifica o rechaza los proyectos de la Cámara de Diputados, resuelve acusaciones constitucionales y participa en la elección de altas autoridades."),
              ("¿Cuál es la diferencia entre senador y diputado?", "Los proyectos de ley ingresan primero a Diputados, que además investiga y acusa. El Senado revisa lo aprobado y resuelve las acusaciones."),
              ("¿Cuántos senadores hay en el Perú?", "60 senadores para el periodo 2026–2031.")],
         html="""<h2>Funciones del Senado</h2>
<ul class="clean">
<li>Revisar, aprobar, modificar o rechazar los proyectos enviados por la Cámara de Diputados.</li>
<li>Ejercer control político sobre determinados actos normativos del Poder Ejecutivo.</li>
<li>Resolver las acusaciones constitucionales presentadas por la Cámara de Diputados.</li>
<li>Elegir, ratificar, designar o remover altas autoridades, como magistrados del Tribunal Constitucional, el Defensor del Pueblo, el Contralor General y directores del Banco Central de Reserva.</li>
</ul>
<h2>Senador y diputado: la diferencia</h2>
<table><thead><tr><th></th><th>Cámara de Diputados</th><th>Senado</th></tr></thead><tbody>
<tr><td>Miembros</td><td>130</td><td>60</td></tr>
<tr><td>Proyectos de ley</td><td>Los recibe primero y los aprueba</td><td>Los revisa, modifica o rechaza</td></tr>
<tr><td>Acusaciones constitucionales</td><td>Las admite, investiga y puede iniciar</td><td>Las resuelve</td></tr>
<tr><td>Altas autoridades</td><td>—</td><td>Elige, ratifica, designa o remueve</td></tr>
</tbody></table>
<h2>Piura en el Senado</h2>
<p>Piura tiene una senadora, Karla Schaefer, de Fuerza Popular. Los <a href="~/guias/diputados-de-piura-2026-2031.html">siete diputados de Piura</a> incluyen a César Revilla.</p>""",
         keys=["bicam", "acred"]),
    dict(slug="facultades-legislativas-2026-cesar-revilla", iso=PUB,
         h1="Pedido de facultades legislativas 2026: qué dijo César Revilla",
         seo="Facultades legislativas 2026: César Revilla",
         desc="Qué planteó César Revilla sobre el pedido de facultades legislativas del Ejecutivo en octubre de 2026: consenso, seguridad ciudadana y El Niño.",
         resumen="El 1 de octubre de 2026 César Revilla dijo que Fuerza Popular no insistiría con los 66 puntos del pedido y propuso un texto de consenso.",
         card="Su posición sobre el pedido de facultades.",
         faq=[("¿Qué dijo César Revilla sobre las facultades legislativas?", "Dijo que Fuerza Popular no insistiría con los 66 puntos del pedido y que aceptaría reducir las materias si así se define en la negociación."),
              ("¿Qué materias priorizó?", "Propuso un texto sustitutorio con consensos, sobre todo en seguridad ciudadana y emergencias por El Niño, según Canal N.")],
         html="""<h2>Qué dijo</h2>
<p>El 1 de octubre de 2026, en una entrevista con Canal N, César Revilla afirmó que Fuerza Popular no insistiría con los 66 puntos del pedido de facultades del Ejecutivo: «Entendemos que ese es el consenso». Según Infobae, explicó que la bancada mantiene como base el texto original, pero que cualquier recorte dependerá del debate parlamentario.</p>
<h2>Un texto de consenso</h2>
<p>Canal N informó que propuso un texto sustitutorio para lograr acuerdos, con énfasis en seguridad ciudadana y en las emergencias por El Niño.</p>
<h2>Materias ambientales y derechos laborales</h2>
<p>Reconoció que todas las bancadas coinciden en excluir las materias ambientales, aunque su sector preferiría incluirlas, y rechazó que la propuesta recorte derechos laborales.</p>
<h2>Contexto</h2>
<p>Revilla habló como vocero de la bancada de diputados de Fuerza Popular, según Infobae. Mira <a href="~/guias/fuerza-popular-congreso-2026-2031.html">la composición de la bancada</a> y su trabajo frente a <a href="~/guias/cesar-revilla-fenomeno-el-nino.html">El Niño</a>.</p>""",
         keys=["infobae1001", "canaln1001"]),
    dict(slug="como-se-crea-una-ley-en-el-peru", iso=PUB,
         h1="Cómo se crea una ley en el Perú: del proyecto a la publicación",
         seo="Cómo se crea una ley en el Perú: pasos",
         desc="Pasos para que un proyecto de ley llegue a ser ley en el Perú: presentación, comisión, Pleno, Ejecutivo y publicación en El Peruano. Con fuente oficial.",
         resumen="Un proyecto se presenta, pasa por comisión, se vota en el Pleno y el Ejecutivo lo promulga o lo observa. Se publica en El Peruano.",
         card="Los pasos, desde el proyecto hasta El Peruano.",
         faq=[("¿Quién puede presentar un proyecto de ley en el Perú?", "El Presidente de la República, los congresistas, otras entidades del Gobierno, organismos autónomos, municipalidades y colegios profesionales. La Constitución también reconoce el derecho a los ciudadanos."),
              ("¿Cuánto tiempo tiene una comisión para dictaminar?", "Según el Congreso, 30 días desde el ingreso del proyecto."),
              ("¿Dónde se publica una ley?", "En el diario oficial El Peruano, en la sección de normas legales. Entra en vigencia al día siguiente, salvo que la ley diga otra fecha.")],
         html="""<h2>Paso a paso</h2>
<ol class="clean">
<li><strong>Presentación.</strong> Puede presentarlo el Presidente de la República, los congresistas, otras entidades del Gobierno, organismos autónomos, municipalidades y colegios profesionales.</li>
<li><strong>Registro.</strong> La Oficina de Trámite Documentario lo recibe, registra y numera. La Secretaría General decide a qué comisión o comisiones va.</li>
<li><strong>Comisión.</strong> Revisa el proyecto con representación de todos los grupos parlamentarios y tiene 30 días para emitir un dictamen, favorable o desfavorable.</li>
<li><strong>Agenda del Pleno.</strong> El Consejo Directivo programa los proyectos dictaminados y reparte los dictámenes a los congresistas al menos 24 horas antes de la sesión.</li>
<li><strong>Votación en el Pleno.</strong> Tras el debate, aprueba o rechaza el proyecto.</li>
<li><strong>Autógrafa.</strong> Se prepara el texto final y se envía al Presidente de la República.</li>
<li><strong>Ejecutivo.</strong> Tiene 15 días para promulgar la ley o devolverla con observaciones. Si vence el plazo sin que actúe, puede promulgarla el Presidente del Congreso o de la Comisión Permanente.</li>
<li><strong>Publicación.</strong> Se publica en El Peruano y entra en vigencia al día siguiente, salvo que la ley indique otra fecha.</li>
</ol>
<p class="upd">El Congreso describe estos pasos para el proceso legislativo. Con el Congreso bicameral desde el 27 de julio de 2026, todo proyecto ingresa primero a la Cámara de Diputados y el Senado lo revisa después.</p>
<h2>Ejemplos con nombre y número</h2>
<p>Mira cómo siguió este camino la <a href="~/gestion/universidad-nacional-de-huancabamba-ley-32162.html">Ley 32162 de la Universidad Nacional de Huancabamba</a>, del proyecto de César Revilla, y el <a href="~/gestion/plan-hidraulico-piura-pl-7131.html">Plan Hidráulico de Piura</a>.</p>
<p>Lee también <a href="~/guias/que-hace-un-diputado-del-peru.html">qué hace un diputado</a> y <a href="~/guias/que-hace-un-senador-del-peru.html">qué hace un senador</a>.</p>""",
         keys=["proceso", "bicam"]),
]
POLITICA_SLUGS = ["como-se-crea-una-ley-en-el-peru","fuerza-popular-congreso-2026-2031", "congreso-bicameral-peru-2026-2031", "que-hace-un-diputado-del-peru",
                  "que-hace-un-senador-del-peru", "diputados-de-piura-2026-2031", "facultades-legislativas-2026-cesar-revilla"]
for g in GUIAS:
    g["path"] = f"guias/{g['slug']}.html"
    g["html"] = g["html"].replace("PEND_SEMANA", pend(g["pend"]) if g["slug"].startswith("semana") else "")

# ---------- Provincias ----------
PROVS = {
    "provincia-de-piura": ("Piura", ["Piura", "Castilla", "Catacaos", "Cura Mori", "El Tallán", "La Arena", "La Unión", "Las Lomas", "Tambo Grande", "Veintiséis de Octubre"]),
    "ayabaca": ("Ayabaca", ["Ayabaca", "Frías", "Jililí", "Lagunas", "Montero", "Pacaipampa", "Paimas", "Sapillica", "Sícchez", "Suyo"]),
    "huancabamba": ("Huancabamba", ["Huancabamba", "Canchaque", "El Carmen de la Frontera", "Huarmaca", "Lalaquiz", "San Miguel de El Faique", "Sóndor", "Sondorillo"]),
    "morropon": ("Morropón", ["Chulucanas", "Buenos Aires", "Chalaco", "La Matanza", "Morropón", "Salitral", "San Juan de Bigote", "Santa Catalina de Mossa", "Santo Domingo", "Yamango"]),
    "paita": ("Paita", ["Paita", "Amotape", "Arenal", "Colán", "La Huaca", "Tamarindo", "Vichayal"]),
    "sullana": ("Sullana", ["Sullana", "Bellavista", "Ignacio Escudero", "Lancones", "Marcavelica", "Miguel Checa", "Querecotillo", "Salitral"]),
    "talara": ("Talara", ["Pariñas", "El Alto", "La Brea", "Lobitos", "Los Órganos", "Máncora"]),
    "sechura": ("Sechura", ["Sechura", "Bellavista de la Unión", "Bernal", "Cristo Nos Valga", "Vice", "Rinconada Llicuar"]),
}
# Una provincia pasa a indexable cuando tiene fichas. Ej.: PROV_FICHAS["sullana"] = ["slug-ficha", ...]
PROV_FICHAS = {"provincia-de-piura": ["drenaje-pluvial-piura-fenomeno-el-nino", "km-980-sesion-descentralizada-reconstruccion", "comision-economia-sesion-descentralizada-piura", "crimen-organizado-sesion-descentralizada-piura-2025",
                                     "reconstruccion-audiencia-alcaldes-piura-2022", "el-nino-2026-credito-suplementario-piura", "puente-carnero-descolmatacion-tambogrande-las-lomas"],
               "huancabamba": ["universidad-nacional-de-huancabamba-ley-32162"],
               "sechura": ["represa-tapa-de-cuy-sechura"],
               "sullana": ["sullana-evacuacion-aerea-nina-insn-san-borja"]}

FAQ = [
    ("¿Quién es César Revilla?",
     "César Revilla es un cirujano dentista y político peruano, diputado por Piura para el periodo 2026–2031 por Fuerza Popular. "
     "Antes fue congresista por Piura en el periodo 2021–2026."),
    ("¿Qué comisiones ha presidido?",
     "Presidió la Comisión Especial Multipartidaria de Seguimiento al proceso de Reconstrucción en las zonas afectadas por el "
     "Fenómeno del Niño Costero, la Comisión de Economía, Banca, Finanzas e Inteligencia Financiera (2023-2024), la comisión de "
     "seguimiento a la Autoridad Nacional de Infraestructura y, en 2025, la comisión contra el terrorismo y el crimen organizado transnacional."),
    ("¿Qué logró como presidente de la Comisión de Economía?",
     "Entre 2023 y 2024 la comisión que presidió aprobó 58 dictámenes y logró 20 leyes, entre ellas el retiro de AFP de hasta 4 UIT "
     "(Ley 32002), la libre disposición del 100% de la CTS (Ley 32027), el REPRO AFP III (Ley 31888), el marco para devolver el Fonavi "
     "y una nueva Ley de Contrataciones del Estado."),
    ("¿Qué leyes ha impulsado?",
     "Es autor del Proyecto de Ley 8018/2023-CR, base de la Ley 32162 que crea la Universidad Nacional de Huancabamba, "
     "y del PL 2204 sobre el personal de salud CAS COVID, aprobado por el Pleno con 112 votos en 2022."),
    ("¿Cuántos votos obtuvo en 2026?",
     "Encabezó la votación regional de Piura con 23,816 votos preferenciales, según El Tiempo."),
    ("¿Quiénes son los diputados de Piura 2026–2031?",
     "Piura eligió siete diputados: César Revilla, Eduardo Castillo, Félix Chang, Carmela Paucará, María Silupú, Miguel Huamán y Henry Albañil, "
     "más la senadora Karla Schaefer."),
    ("¿César Revilla es de Fuerza Popular?",
     "Sí. César Revilla es diputado por Piura de Fuerza Popular para 2026–2031. La bancada tiene 41 de los 130 diputados, según el conteo de la ONPE."),
    ("¿Cuántos diputados y senadores tiene Fuerza Popular?",
     "Fuerza Popular tiene 41 diputados y 22 senadores en el Congreso bicameral 2026–2031, la mayor bancada de ambas cámaras, según Infomercado."),
    ("¿Qué hace un diputado en el Perú?",
     "Presenta, debate y aprueba leyes, ejerce control político sobre el Ejecutivo y puede admitir e iniciar acusaciones constitucionales. La Cámara tiene 130 diputados."),
    ("¿Dónde puedo ver su asistencia y sus votaciones?",
     "En la sección de transparencia de este sitio se enlazan las fuentes oficiales del Congreso donde se publican asistencia, "
     "votaciones y proyectos de ley."),
]

NAV = [
    ("index.html", "Inicio"),
    ("biografia.html", "Biografía"),
    ("gestion.html", "Gestión"),
    ("proyectos-de-ley.html", "Leyes"),
    ("cifras.html", "En cifras"),
    ("congreso-2026-2031.html", "Congreso"),
    ("explica.html", "Explica"),
    ("guias.html", "Guías"),
    ("piura.html", "Piura"),
    ("transparencia.html", "Transparencia"),
    ("contacto.html", "Contacto"),
]

PERSON = {
    "@context": "https://schema.org", "@type": "Person", "@id": BASE + "/#persona",
    "name": "César Manuel Revilla Villanueva", "alternateName": ["César Revilla", "César Revilla Villanueva"],
    "givenName": "César Manuel", "familyName": "Revilla Villanueva",
    "jobTitle": "Diputado de la República del Perú", "url": BASE + "/", "image": BASE + "/img/og.jpg",
    "description": "Cirujano dentista y político peruano. Diputado por Piura (2026-2031) y congresista (2021-2026); presidió la Comisión de Economía del Congreso.",
    "birthDate": "1987-03-19",
    "birthPlace": {"@type": "Place", "name": "Chiclayo, Lambayeque, Perú"},
    "nationality": {"@type": "Country", "name": "Perú"},
    "hasOccupation": [{"@type": "Occupation", "name": "Diputado de la República del Perú"}, {"@type": "Occupation", "name": "Cirujano dentista"}],
    "memberOf": [
        {"@type": "OrganizationRole", "roleName": "Diputado por Piura", "startDate": "2026-07-26",
         "memberOf": {"@type": "GovernmentOrganization", "name": "Cámara de Diputados del Perú", "url": "https://diputados.congreso.gob.pe/"}},
        {"@type": "OrganizationRole", "roleName": "Congresista por Piura", "startDate": "2021-07-26", "endDate": "2026-07-26",
         "memberOf": {"@type": "GovernmentOrganization", "name": "Congreso de la República del Perú", "url": "https://www.congreso.gob.pe/"}},
        {"@type": "OrganizationRole", "roleName": "Presidente de la Comisión de Economía, Banca, Finanzas e Inteligencia Financiera", "startDate": "2023-08-16", "endDate": "2024-07-26",
         "memberOf": {"@type": "GovernmentOrganization", "name": "Congreso de la República del Perú"}},
    ],
    "affiliation": {"@type": "PoliticalParty", "name": "Fuerza Popular"},
    "worksFor": {"@type": "GovernmentOrganization", "name": "Cámara de Diputados del Perú", "url": "https://diputados.congreso.gob.pe/"},
    "workLocation": {"@type": "Place", "name": "Congreso de la República, Lima, Perú"},
    "homeLocation": {"@type": "Place", "name": "Piura, Perú"},
    "areaServed": {"@type": "AdministrativeArea", "name": "Región Piura, Perú"},
    "mainEntityOfPage": BASE + "/",
    "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Universidad César Vallejo"}, {"@type": "CollegeOrUniversity", "name": "Universidad Inca Garcilaso de la Vega"}],
    "email": "crevilla@congreso.gob.pe",
    "knowsAbout": ["Economía", "Pensiones (AFP)", "CTS", "Mypes", "Contrataciones del Estado", "Seguridad ciudadana", "Crimen organizado",
                   "Fenómeno El Niño", "Reconstrucción", "Salud pública", "Educación universitaria", "Recursos hídricos", "Piura"],
    "sameAs": ["https://www.facebook.com/cesarrevillav", "https://www.tiktok.com/@cesarrevillav", "https://www.wikidata.org/wiki/Q108414723", "https://es.wikipedia.org/wiki/C%C3%A9sar_Revilla",
               "https://diputados.congreso.gob.pe/diputado/revilla-villanueva-cesar-manuel/"],
}

GA_ID = "G-Z73V8KFPQT"
GTAG = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>'
        f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());"
        f"gtag('config','{GA_ID}',{{allow_google_signals:false,allow_ad_personalization_signals:false}});</script>")
PERSON_REF = {"@type": "Person", "@id": BASE + "/#persona", "name": "César Manuel Revilla Villanueva", "url": BASE + "/"}
PAGES = []


def add(path, title, desc, body, h1=None, lead=None, crumbs=None, kind="page", index=True, date=None,
        keys=(), home=False, ld_extra=None, in_feed=False, brand=True):
    PAGES.append(dict(path=path, title=title, desc=desc, body=body, h1=h1, lead=lead, crumbs=crumbs or [], kind=kind,
                      index=index, date=date, keys=list(keys), home=home, ld_extra=ld_extra, in_feed=in_feed, brand=brand))


def retrato():
    if os.path.exists(os.path.join(OUT, "img", "cesar-revilla.jpg")):
        inner = ('<img class="retrato" src="~/img/cesar-revilla.jpg" width="640" height="800" fetchpriority="high" '
                 'alt="César Revilla, diputado por Piura">')
    else:
        inner = ('<div class="retrato ph" role="img" aria-label="César Revilla, diputado por Piura">'
                 '<div>CR<span>Diputado por Piura<br>2026–2031</span></div></div>')
    return f'<div class="retrato-wrap">{inner}</div>'


GALERIA = [
    ("01-pleno-congreso.jpg", "En el Pleno del Congreso de la República"),
    ("02-juramentacion-2026.jpg", "Juramentación como diputado, 2026"),
    ("03-parada-militar-2026.jpg", "Parada militar 2026"),
    ("04-fenomeno-el-nino-piura.jpg", "Fenómeno de El Niño en Piura: revisión de obras en campo"),
    ("05-anin-semana-representacion.jpg", "Semana de Representación con la ANIN"),
    ("06-anin-piura-proyectos.jpg", "Proyectos de la ANIN para Piura"),
    ("07-cas-covid.jpg", "Intervención sobre el personal CAS COVID"),
]


def galeria():
    """Fotos del despacho (img/galeria/), cada una con su descripción."""
    folder = os.path.join(OUT, "img", "galeria")
    figs = "".join(f'<figure><img src="~/img/galeria/{f}" loading="lazy" width="600" height="450" '
                   f'alt="César Revilla: {esc(c)}"><figcaption>{esc(c)}</figcaption></figure>'
                   for f, c in GALERIA if os.path.exists(os.path.join(folder, f)))
    if not figs:
        return ""
    return (f'<section class="block"><div class="wrap"><h2 class="kicker" data-k="Galería">En el territorio y el Congreso</h2>'
            f'<div class="gallery">{figs}</div></div></section>')


LEY_PUB = {"universidad-nacional-de-huancabamba-ley-32162": "Ley 32162", "retiro-afp-2024-ley-32002": "Ley 32002",
           "retiro-cts-2024-comision-economia": "Ley 32027", "mypes-detracciones-ley-por-insistencia-2023": "Ley publicada",
           "represa-tapa-de-cuy-sechura": "Ley 31413"}


def stamp_for(path):
    slug = path.rsplit("/", 1)[-1].replace(".html", "")
    return f'<span class="stamp">✓ {LEY_PUB[slug]}</span>' if slug in LEY_PUB else ""


def card(tag, title, desc, path):
    return (f'<div class="card">{stamp_for(path)}<span class="tag">{esc(tag)}</span><h3><a href="~/{path}">{esc(title)}</a></h3>'
            f'<p>{esc(desc)}</p><a class="more" href="~/{path}">Leer →</a></div>')


def ficha_by_slug(s):
    return next(f for f in FICHAS if f["slug"] == s)


def related_for(f):
    items = []
    if f.get("tema"):
        items += [x for x in FICHAS if x["tema"] == f["tema"] and x is not f]
    items += [x for x in FICHAS if x is not f and x not in items]
    return items[:3]


# ============ LAYOUT ============
def layout(p):
    path = p["path"]
    depth = path.count("/")
    pre = "../" * depth
    clean = "" if path == "index.html" else path[:-5]
    url = BASE + "/" + clean
    _slug = os.path.basename(path)[:-5]
    og_rel = f"img/og/{_slug}.jpg" if os.path.exists(os.path.join(OUT, "img", "og", _slug + ".jpg")) else "img/og.jpg"
    og_url = BASE + "/" + og_rel
    title = p["title"] + (BRAND_SUFFIX if p["brand"] else "")
    if DRAFT:
        robots = "noindex, nofollow"
    elif not p["index"]:
        robots = "noindex, follow"
    else:
        robots = "index, follow, max-image-preview:large"

    nav = "".join(f'<a href="{pre}{pp}"' + (' aria-current="page"' if pp == path else "") + f">{t}</a>" for pp, t in NAV)

    ld = [PERSON] if p["home"] else []
    ld.append({"@context": "https://schema.org", "@type": "WebSite", "@id": BASE + "/#sitio", "name": SITE + " · " + TAG, "url": BASE + "/",
               "inLanguage": "es-PE", "publisher": PERSON_REF, "about": PERSON_REF})
    page_type = "ProfilePage" if p["home"] else ("CollectionPage" if p["path"] in ("medios.html", "guias.html", "gestion.html", "congreso-2026-2031.html", "proyectos-de-ley.html", "explica.html") else "WebPage")
    wp = {"@context": "https://schema.org", "@type": page_type, "@id": url + "#pagina", "url": url, "name": title, "description": p["desc"],
          "inLanguage": "es-PE", "isPartOf": {"@type": "WebSite", "@id": BASE + "/#sitio", "url": BASE + "/"}, "about": PERSON_REF,
          "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".resumen", ".lead"]}}
    if p["date"]:
        wp["datePublished"] = p["date"] + "T08:00:00-05:00"; wp["dateModified"] = p["date"] + "T08:00:00-05:00"
    if p["home"]:
        wp["mainEntity"] = PERSON_REF; wp["dateModified"] = PUB + "T08:00:00-05:00"
    ld.append(wp)
    if p["crumbs"]:
        items = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"}]
        for i, (n, cp) in enumerate(p["crumbs"], start=2):
            items.append({"@type": "ListItem", "position": i, "name": n, "item": BASE + "/" + cp[:-5]})
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
    if p["kind"] == "article":
        ld.append({"@context": "https://schema.org", "@type": "Article", "headline": p["h1"][:110], "description": p["desc"],
                   "datePublished": p["date"] + "T08:00:00-05:00", "dateModified": p["date"] + "T08:00:00-05:00", "inLanguage": "es-PE", "mainEntityOfPage": url,
                   "author": PERSON_REF, "publisher": PERSON_REF,
                   "about": PERSON_REF, "image": og_url, "isAccessibleForFree": True,
                   "isPartOf": {"@type": "WebPage", "@id": url + "#pagina", "url": url}, "mentions": [{"@type": "PoliticalParty", "name": "Fuerza Popular"}, {"@type": "Place", "name": "Piura, Perú"}],
                   "citation": [{"@type": "CreativeWork", "name": SRC[k][0], "url": SRC[k][1]} for k in p["keys"]]})
    if p["ld_extra"]:
        ld.extend(p["ld_extra"] if isinstance(p["ld_extra"], list) else [p["ld_extra"]])
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)

    head_block = ""
    if p["h1"]:
        trail = f'<li><a href="{pre}index.html">Inicio</a></li>'
        for n, cp in p["crumbs"]:
            trail += (f'<li aria-current="page">{esc(n)}</li>' if cp == path else f'<li><a href="{pre}{cp}">{esc(n)}</a></li>')
        head_block = (f'<header class="page-head"><div class="wrap"><nav class="crumbs" aria-label="Ruta"><ol>{trail}</ol></nav>'
                      f'<h1>{esc(p["h1"])}</h1>' + (f'<p class="lead">{p["lead"]}</p>' if p["lead"] else "") + "</div></header>")

    draftbar = ('<div class="draftbar">BORRADOR · no indexable · completar bloques “Pendiente” antes de publicar</div>' if DRAFT else "")
    _fa = [("biografia.html", "Biografía"), ("gestion.html", "Gestión"), ("proyectos-de-ley.html", "Leyes"), ("cifras.html", "En cifras"), ("congreso-2026-2031.html", "Congreso 2026–2031"), ("explica.html", "Explica"), ("guias.html", "Guías"), ("piura.html", "Piura")]
    _fb = [("transparencia.html", "Transparencia"), ("prensa.html", "Sala de prensa"), ("medios.html", "En los medios"), ("canales-oficiales.html", "Canales oficiales"), ("contacto.html", "Contacto")]
    foot_a = "".join(f'<li><a href="{pre}{pp}">{t}</a></li>' for pp, t in _fa)
    foot_b = "".join(f'<li><a href="{pre}{pp}">{t}</a></li>' for pp, t in _fb)
    og_img = (f'<meta property="og:image" content="{og_url}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
              f'<meta property="og:image:alt" content="{esc(p["h1"] or "César Revilla, diputado de la República del Perú por Piura")}"><meta name="twitter:image" content="{og_url}">'
              if os.path.exists(os.path.join(OUT, "img", "og.jpg")) else "")
    page = f"""<!doctype html>
<html lang="es-PE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(p['desc'])}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="es-PE" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">
<meta name="robots" content="{robots}">
<meta name="author" content="César Revilla"><meta name="geo.region" content="PE-PIU"><meta name="geo.placename" content="Piura, Perú">
<meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(p['desc'])}">
<meta name="theme-color" content="#0F2A44">
<link rel="alternate" type="application/rss+xml" title="Gestiones y guías de César Revilla" href="{pre}feed.xml">
<meta property="og:type" content="{'article' if p['kind'] == 'article' else ('profile' if p['home'] else 'website')}">
<meta property="og:locale" content="es_PE">
<meta property="og:site_name" content="{esc(SITE)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{url}">
{og_img}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}favicon.ico" sizes="any">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400&display=swap"></noscript>
<link rel="stylesheet" href="{pre}styles.css"><link rel="stylesheet" href="{pre}fotos.css">
<script src="{pre}main.js" defer></script>
{GTAG}
{ld_html}
</head>
<body>
<a class="skip" href="#contenido">Saltar al contenido</a>
{'<div class="progress" aria-hidden="true"></div>' if p['kind'] == 'article' else ''}
{draftbar}
<header class="site-head"><div class="wrap">
<a class="brand" href="{pre}index.html">{SITE}<small>{TAG} · 2026–2031</small></a>
<nav class="nav" aria-label="Principal">{nav}</nav>
</div></header>
<main id="contenido">
{head_block}
{p['body']}
</main>
<footer class="site-foot"><div class="wrap">
<div class="cols">
<div class="foot-brand"><strong>{SITE}</strong>
<p>{TAG}<br>Fuerza Popular · Periodo 2026–2031</p>
<ul class="foot-social">
<li><a href="https://www.facebook.com/cesarrevillav" rel="me noopener" target="_blank">Facebook</a></li>
<li><a href="https://www.tiktok.com/@cesarrevillav" rel="me noopener" target="_blank">TikTok</a></li>
<li><a href="mailto:crevilla@congreso.gob.pe">Correo</a></li>
</ul></div>
<div><strong>Explora</strong><ul>{foot_a}</ul></div>
<div><strong>Institucional</strong><ul>{foot_b}</ul></div>
<div><strong>Fuentes oficiales</strong><ul>
<li><a href="https://diputados.congreso.gob.pe/diputado/revilla-villanueva-cesar-manuel/" rel="noopener" target="_blank">Ficha en la Cámara de Diputados</a></li>
<li><a href="https://www.congreso.gob.pe" rel="noopener" target="_blank">Congreso de la República</a></li>
<li><a href="https://www.gob.pe/jne" rel="noopener" target="_blank">Jurado Nacional de Elecciones</a></li>
</ul></div>
</div>
<div class="foot-bottom">
<p class="aviso">Sitio personal de César Revilla. No es un portal oficial del Congreso de la República. Los datos citados enlazan a su fuente; si encuentras un error, escríbenos desde la sección de contacto.</p>
<p class="foot-legal">© 2026 César Revilla · <a href="{pre}politica-de-privacidad.html">Privacidad</a> · <a href="{pre}canales-oficiales.html">Canales oficiales</a> · <a href="{pre}feed.xml">RSS</a> · <a href="{pre}sitemap.xml">Mapa del sitio</a></p>
</div>
</div></footer>
<script>(function(){{if(typeof gtag!=="function")return;var h=location.hostname;
document.addEventListener("click",function(e){{var a=e.target.closest&&e.target.closest("a[href]");if(!a)return;var u=a.getAttribute("href")||"";
if(u.indexOf("mailto:")===0){{gtag("event","contacto_correo",{{link_url:u}});return}}
if(/wa[.]me|whatsapp[.]com/.test(u)){{gtag("event","contacto_whatsapp",{{link_url:u}});return}}
if(/^https?:/.test(u)&&a.hostname!==h){{gtag("event",a.closest(".fuentes,.src,.facts,article")?"clic_fuente":"clic_salida",{{link_url:u,link_domain:a.hostname,page_path:location.pathname}})}}}},true);
var f=0;window.addEventListener("scroll",function(){{if(f)return;var d=document.documentElement;if((window.scrollY+window.innerHeight)/d.scrollHeight>.9){{f=1;gtag("event","lectura_completa",{{page_path:location.pathname}})}}}},{{passive:true}})}})();</script>
</body>
</html>
"""
    page = page.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")
    return page.replace('"~/', '"' + pre)


# ============ ARTÍCULOS (fichas y guías) ============
def article_body(meta_line, resumen, content_html, keys, related_html, pend_html):
    fuentes = "".join(li_src(k) for k in keys)
    return f"""<section class="block"><div class="wrap narrow"><article>
<p class="meta">{meta_line}</p>
<p class="resumen"><strong>En breve:</strong> {esc(resumen)}</p>
{content_html}
<h2>Fuentes</h2>
<ul class="fuentes">{fuentes}</ul>
{pend_html}
<h2>Sigue leyendo</h2>
<div class="grid">{related_html}</div>
</article></div></section>"""


# ============ GRÁFICOS (HTML/CSS, sin librerías; Google lee los números) ============
def _fmt(n):
    return f"{n:,}"


def bars(title, rows, total, note, keys, unit_note=""):
    """rows: (etiqueta, valor, texto_valor, href|None, destacado:bool)"""
    out = []
    for lab, val, txt, href, hi in rows:
        w = max(1.5, round(100 * val / total, 1))
        lab_html = f'<a href="~/{href}">{esc(lab)}</a>' if href else esc(lab)
        out.append(f'<div class="bar-row{" hi" if hi else ""}"><span class="bar-label">{lab_html}</span>'
                   f'<span class="bar-track"><span class="bar-fill" style="--w:{w}%"></span></span>'
                   f'<span class="bar-val">{esc(txt)}</span></div>')
    src = " · ".join(f'<a href="{SRC[k][1]}" rel="noopener" target="_blank">{esc(SRC[k][0])}</a>' for k in keys)
    return (f'<figure class="chart-fig"><figcaption><h3>{esc(title)}</h3>{f"<span>{esc(unit_note)}</span>" if unit_note else ""}</figcaption>'
            f'<div class="bars">{"".join(out)}</div><p class="chart-note">{note} <span class="chart-src">Fuente: {src}</span></p></figure>')


def stacked(title, segs, note, keys):
    """segs: (etiqueta, valor, clase)"""
    tot = sum(v for _, v, _ in segs)
    bar = "".join(f'<span class="seg {c}" style="--w:{round(100 * v / tot, 1)}%" title="{esc(l)}: {v}"><b>{v}</b></span>' for l, v, c in segs)
    leg = "".join(f'<li><i class="dot {c}"></i>{esc(l)} <b>{v}</b></li>' for l, v, c in segs)
    src = " · ".join(f'<a href="{SRC[k][1]}" rel="noopener" target="_blank">{esc(SRC[k][0])}</a>' for k in keys)
    return (f'<figure class="chart-fig"><figcaption><h3>{esc(title)}</h3><span>Total: {tot}</span></figcaption>'
            f'<div class="stack">{bar}</div><ul class="legend">{leg}</ul>'
            f'<p class="chart-note">{note} <span class="chart-src">Fuente: {src}</span></p></figure>')


IMPACTO = [  # (número para contar, sufijo, texto, ficha, clave de fuente)
    ("4", " millones", "de trabajadores, según estimaciones, podían disponer del 100% de su CTS en 2024 (Ley 32027).", "gestion/retiro-cts-2024-comision-economia.html", "cts24"),
    ("2", " millones", "de fonavistas, con el marco para reiniciar la devolución de sus aportes.", "gestion/balance-comision-economia-2023-2024.html", "econbal"),
    ("60", " mil", "trabajadores de salud CAS COVID a los que podía alcanzar el PL 2204, aprobado con 112 votos.", "gestion/cas-covid-pl-2204-personal-de-salud.html", "cas"),
    ("3500", " ha", "de nueva frontera agrícola en Sechura con la represa Tapa de Cuy.", "gestion/represa-tapa-de-cuy-sechura.html", "tapacuy"),
    ("20", " leyes", "logradas por la Comisión de Economía que presidió (2023-2024).", "gestion/balance-comision-economia-2023-2024.html", "econbal"),
    ("300", " millones", "de soles para mitigar El Niño en 2026, de los cuales entre 60 y 70 millones irían a Piura.", "gestion/el-nino-2026-credito-suplementario-piura.html", "nino26"),
]


def impacto_html(n=6):
    items = []
    for num, suf, txt, href, k in IMPACTO[:n]:
        pre = "S/ " if "soles" in txt else ""
        items.append(f'<a class="imp" href="~/{href}"><strong>{pre}<span data-count="{num}">{_fmt(int(num))}</span>{esc(suf)}</strong>'
                     f'<span>{esc(txt)}</span></a>')
    return f'<div class="impact">{"".join(items)}</div>'


VOTOS_PLENO = [
    ("CAS COVID para el personal de salud (PL 2204)", 112, "gestion/cas-covid-pl-2204-personal-de-salud.html", "cas"),
    ("Régimen excepcional del Impuesto a la Renta", 104, "gestion/regimen-excepcional-impuesto-renta-2024.html", "ir24"),
    ("Liberación del 100% de la CTS", 98, "gestion/retiro-cts-2024-comision-economia.html", "cts24"),
    ("Fondos de detracciones para mypes (insistencia)", 89, "gestion/mypes-detracciones-ley-por-insistencia-2023.html", "mypes23"),
    ("Universidad Nacional de Huancabamba", 75, "gestion/universidad-nacional-de-huancabamba-ley-32162.html", "huanca1"),
]
chart_votos = bars("Respaldo en el Pleno del Congreso", [(l, v, f"{v} votos", h, False) for l, v, h, _ in VOTOS_PLENO], 130,
                   "Votos a favor obtenidos por iniciativas de su autoría o que sustentó como presidente de la Comisión de Economía. El Congreso unicameral tenía 130 miembros.",
                   sorted({k for *_, k in VOTOS_PLENO}), "Votos a favor, sobre 130 congresistas")
chart_embudo = bars("De 268 proyectos a 20 leyes", [("Proyectos de ley evaluados", 268, "268", None, False),
                                                    ("Dictámenes aprobados", 58, "58", None, False),
                                                    ("Leyes publicadas", 20, "20", None, True)], 268,
                    "Resultado de la Comisión de Economía, Banca, Finanzas e Inteligencia Financiera bajo su presidencia (periodo 2023-2024).", ["econbal"])
chart_dict = stacked("Los 58 dictámenes, por tipo", [("Favorables", 37, "s1"), ("Por insistencia frente al Ejecutivo", 13, "s2"), ("De inhibición", 8, "s3")],
                     "Los dictámenes por insistencia defendieron leyes que el Poder Ejecutivo había observado.", ["econbal"])
chart_sesiones = bars("Sesiones de trabajo de la comisión", [("Extraordinarias", 19, "19", None, False), ("Ordinarias", 15, "15", None, False),
                                                             ("Descentralizadas, en regiones", 9, "9", None, True), ("Audiencias públicas", 4, "4", None, False)], 19,
                      "Las sesiones descentralizadas llevaron la comisión a regiones, entre ellas Piura y Loreto.", ["econbal"])
_dv = [(n, int(v.replace(",", "")), v, None, i == 0) for i, (n, _, v) in enumerate(DIP_ROWS)]
chart_eleccion = bars("Elecciones 2026: votación preferencial en Piura", _dv, _dv[0][1],
                      "Diputados electos por Piura para el periodo 2026-2031. César Revilla obtuvo la votación más alta de la región.", ["acred", "diputados"])

ficha_by_slug("balance-comision-economia-2023-2024")["extra"] = chart_embudo + chart_dict + chart_sesiones
ficha_by_slug("revilla-lidera-votacion-piura-2026")["extra"] = chart_eleccion

for f in FICHAS:
    tema = TEMAS.get(f["tema"]) if f["tema"] else None
    tema_link = (f'Tema: <a href="~/temas/{f["tema"]}.html">{esc(tema["h1"])}</a> · ' if tema else "")
    meta = stamp_for(f["path"]) + f'Ficha de gestión · {tema_link}Hecho: {esc(f["hecho"])} · Publicado el {fdate(f.get("pub", PUB))}'
    content = "".join(f"<p>{t}</p>" for t in f["paras"]) + f.get("extra", "")
    rel = "".join(card("Gestión", r["h1"], r["resumen"], r["path"]) for r in related_for(f))
    crumbs = [("Gestión", "gestion.html")]
    if f["folder"] == "proyectos-de-ley":
        crumbs = [("Leyes", "proyectos-de-ley.html")]
    crumbs.append((f["h1"], f["path"]))
    add(f["path"], f["seo"], f["desc"], article_body(meta, f["resumen"], content, f["keys"], rel, pend(f["pend"]) if f["pend"] else ""),
        h1=f["h1"], crumbs=crumbs, kind="article", date=f.get("pub", PUB), keys=f["keys"], in_feed=True)

HOWTO_SLUGS = ["como-pedir-informacion-publica-peru", "como-se-crea-una-ley-en-el-peru"]
for g in GUIAS:
    meta = f'Guía ciudadana · Publicada el {fdate(g["iso"])}'
    others = [x for x in GUIAS if x is not g and x["slug"] in POLITICA_SLUGS][:3] or [x for x in GUIAS if x is not g][:3]
    rel = "".join(card("Guía", o["h1"], o["card"], o["path"]) for o in others)
    body_html = g["html"]
    faq_ld_g = None
    if g.get("faq"):
        body_html += "<h2>Preguntas frecuentes</h2>" + "".join(
            f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in g["faq"])
        faq_ld_g = {"@context": "https://schema.org", "@type": "FAQPage",
                    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]}
    if g["slug"] in HOWTO_SLUGS:
        _ol = re.search(r'<ol class="clean">(.*?)</ol>', g["html"], re.S)
        _steps = []
        for _li in re.findall(r"<li>(.*?)</li>", _ol.group(1), re.S):
            _t = re.sub(r"<[^>]+>", "", _li).strip()
            _n = re.match(r"([^.:]{3,60})[.:]\s", _t)
            _steps.append({"@type": "HowToStep", "name": (_n.group(1) if _n else _t[:60]), "text": _t})
        _howto = {"@context": "https://schema.org", "@type": "HowTo", "name": g["h1"], "description": g["desc"], "inLanguage": "es-PE",
                  "step": [dict(st, position=i) for i, st in enumerate(_steps, 1)]}
        faq_ld_g = [faq_ld_g, _howto] if faq_ld_g else _howto
    add(g["path"], g["seo"], g["desc"],
        article_body(meta, g["resumen"], body_html, g["keys"], rel, pend(g["pend"]) if (g.get("pend") and not g["slug"].startswith("semana")) else ""),
        h1=g["h1"], crumbs=[("Guías", "guias.html"), (g["h1"], g["path"])], kind="article", date=g["iso"], keys=g["keys"], in_feed=True,
        ld_extra=faq_ld_g)

# ============ EXPLICA (explicaciones con fuentes) ============
for e in EXPLICA:
    e["path"] = f"explica/{e['slug']}.html"
_exp_by_tema = {}
for e in EXPLICA:
    _exp_by_tema.setdefault(e["tema"], []).append(e)
_guia_by_slug = {g["slug"]: g for g in GUIAS}

for e in EXPLICA:
    t = EXP_TEMAS[e["tema"]]
    meta = f'Explicación · {esc(t["h1"])} · Publicada el {fdate(e["iso"])}'
    others = [x for x in _exp_by_tema[e["tema"]] if x is not e] + [_guia_by_slug[s] for s in t["guias"]]
    others = others[:3] or [x for x in EXPLICA if x is not e][:3]
    rel = "".join(card("Explica", o["h1"], o["card"], o["path"]) for o in others)
    body_html = e["html"] + "<h2>Preguntas frecuentes</h2>" + "".join(
        f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in e["faq"])
    faq_ld_e = {"@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in e["faq"]]}
    add(e["path"], e["seo"], e["desc"], article_body(meta, e["resumen"], body_html, e["keys"], rel, ""),
        h1=e["h1"], crumbs=[("Explica", "explica.html"), (t["h1"], f"explica/{e['tema']}.html"), (e["h1"], e["path"])],
        kind="article", date=e["iso"], keys=e["keys"], in_feed=True, ld_extra=faq_ld_e)

for slug, t in EXP_TEMAS.items():
    exps = _exp_by_tema.get(slug, [])
    gs = [_guia_by_slug[s] for s in t["guias"]]
    fs = [ficha_by_slug(s) for s in t["fichas"]]
    blocks = ""
    if exps:
        blocks += "<h2>Explicaciones</h2><div class=\"grid\">" + "".join(card("Explica", x["h1"], x["card"], x["path"]) for x in exps) + "</div>"
    if gs:
        blocks += "<h2>Guías</h2><div class=\"grid\">" + "".join(card("Guía", g["h1"], g["card"], g["path"]) for g in gs) + "</div>"
    if fs:
        blocks += "<h2>Gestiones documentadas de César Revilla</h2><div class=\"grid\">" + "".join(
            card("Ficha", f["h1"], f["resumen"], f["path"]) for f in fs) + "</div>"
    extra = f'<p><a href="~/{t["gestion"]}">Ver toda su gestión sobre este tema →</a></p>' if t["gestion"] else ""
    body = f"""<section class="block"><div class="wrap">
<p class="lead" style="color:var(--ink)">{t['intro']}</p>
{blocks}
{extra}
<p><a href="~/explica.html">← Volver a Explica</a></p>
</div></section>"""
    add(f"explica/{slug}.html", t["seo"], t["desc"], body, h1=t["h1"], lead=t["desc"],
        crumbs=[("Explica", "explica.html"), (t["h1"], f"explica/{slug}.html")], date="2026-11-14")

EXP_HUB_FAQ = [
    ("¿Qué es Explica?", "Es el apartado de este sitio donde se explican con fuentes los temas políticos y sociales del Perú: cómo funciona el Congreso, qué significa una norma o por qué ocurre algo."),
    ("¿Todo lo que se publica tiene fuente?", "Sí. Cada explicación enlaza a sus fuentes y lleva su fecha de publicación. Si hay un error, se corrige en la misma página."),
    ("¿Este sitio es del Congreso?", "No. Es el sitio personal del diputado César Revilla. Para documentos oficiales, cada página enlaza al portal del Congreso u otra fuente."),
]
add("explica.html", "Explica: política del Perú explicada con fuentes",
    "Explicaciones claras y con fuentes sobre el Congreso, la seguridad, la economía y la participación ciudadana en el Perú. Por César Revilla.",
    f"""<section class="block"><div class="wrap">
<p class="resumen"><strong>En breve:</strong> aquí encuentras explicaciones con fuente sobre cómo funciona el Congreso, qué significan las noticias políticas y cómo participar. Cada página lleva su fecha y sus enlaces.</p>
<h2>Por tema</h2>
<div class="grid">{''.join(card('Tema', t['h1'], t['desc'], f'explica/{s}.html') for s, t in EXP_TEMAS.items())}</div>
<h2>Explicaciones recientes</h2>
<div class="grid">{''.join(card('Explica', x['h1'], x['card'], x['path']) for x in sorted(EXPLICA, key=lambda z: z['iso'], reverse=True))}</div>
<h2>Cómo trabajamos</h2>
<ul class="clean">
<li>Cada afirmación sale de una fuente oficial o de un medio reconocido, y la fuente está enlazada.</li>
<li>Se separan los hechos de la opinión. Si una página recoge una postura de César Revilla, lo dice.</li>
<li>Cada página lleva su fecha. Si algo cambia, se actualiza y se corrige a la vista.</li>
</ul>
<h2>Preguntas frecuentes</h2>
{''.join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in EXP_HUB_FAQ)}
<p>¿Hay un tema que quieres que se explique? Escríbenos desde <a href="~/contacto.html">Contacto</a>.</p>
</div></section>""",
    h1="Explica: lo que pasa en el Perú, con fuentes", lead="Cómo funciona el Congreso y qué significan los temas políticos y sociales, en palabras simples.",
    crumbs=[("Explica", "explica.html")], brand=False, date="2026-11-14",
    ld_extra={"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in EXP_HUB_FAQ]})

# ============ HUBS DE TEMA ============
for slug, t in TEMAS.items():
    items = [f for f in FICHAS if f["tema"] == slug]
    cards = "".join(card("Ficha", f["h1"], f["resumen"], f["path"]) for f in items)
    body = f"""<section class="block"><div class="wrap">
<p class="lead" style="color:var(--ink)">{t['intro']}</p>
<h2>Fichas de este tema</h2>
<div class="grid">{cards}</div>
{pend(t['pend'])}
<p><a href="~/gestion.html">← Volver a Gestión</a></p>
</div></section>"""
    add(f"temas/{slug}.html", t["seo"], t["desc"], body, h1=t["h1"], lead=t["desc"],
        crumbs=[("Gestión", "gestion.html"), (t["h1"], f"temas/{slug}.html")])

# ============ GESTIÓN (hub) ============
tema_cards = "".join(card("Tema", t["h1"], t["card"], f"temas/{s}.html") for s, t in TEMAS.items())
all_cards = "".join(card("Ficha", f["h1"], f["resumen"], f["path"]) for f in FICHAS if f["folder"] == "gestion")
gestion_body = f"""<section class="block"><div class="wrap">
<h2>Por tema</h2>
<div class="grid">{tema_cards}</div>
</div></section>
<section class="block alt"><div class="wrap">
<h2>Todas las fichas de gestión</h2>
<div class="grid">{all_cards}</div>
<p><a class="btn" href="~/proyectos-de-ley.html">Ver sus leyes</a></p>
{pend("Cada obra, reunión, oficio o pedido de información nuevo debe entrar como una ficha propia (con fecha, lugar, monto y documento). Meta sugerida: 2 fichas por semana.")}
</div></section>"""
add("gestion.html", "Gestión de César Revilla por Piura",
    "Gestiones y leyes de César Revilla, diputado del Perú: economía, AFP y CTS, seguridad, El Niño, reconstrucción, agua y salud. Con fuentes.",
    gestion_body, h1="Gestión", lead="Lo que hace César Revilla por el Perú y por Piura, ordenado por tema y con su fuente.",
    crumbs=[("Gestión", "gestion.html")])

# ============ PROYECTOS DE LEY ============



TIMELINE = [
    ("2021", "Asume como congresista por Piura y propone llevar la comisión de Reconstrucción al km 980, con los damnificados del Niño Costero.", "gestion/km-980-sesion-descentralizada-reconstruccion.html"),
    ("2022", "Preside la comisión de seguimiento a la Reconstrucción y recibe en Piura a los alcaldes. El Pleno aprueba su proyecto CAS COVID con 112 votos.", "gestion/cas-covid-pl-2204-personal-de-salud.html"),
    ("2023", "Asume la presidencia de la Comisión de Economía. El Congreso libera los fondos de detracciones de las mypes.", "gestion/comision-economia-presidencia-2023.html"),
    ("2024", "Retiro de AFP de hasta 4 UIT, 100% de la CTS y 20 leyes de la comisión. Preside la comisión de la ANI. Se publica la ley de la Universidad de Huancabamba.", "gestion/balance-comision-economia-2023-2024.html"),
    ("2025", "Preside la comisión contra el terrorismo y el crimen organizado. Se aprueba por unanimidad su proyecto del Plan Hidráulico de Piura.", "gestion/comision-crimen-organizado-presidencia-2025.html"),
    ("2026", "Obtiene la primera votación de Piura (23,816 votos) y asume como diputado. Impulsa recursos para enfrentar El Niño.", "gestion/revilla-lidera-votacion-piura-2026.html"),
]
tl_html = "".join(f'<li><span class="tag">{y}</span><p>{esc(t)}</p><a class="fuente" href="~/{h}">Ver ficha →</a></li>' for y, t, h in TIMELINE)
prov_tiles = "".join(
    f'<a class="tile{" on" if PROV_FICHAS.get(sl) else ""}" href="~/piura/{sl}.html"><b>{len(PROV_FICHAS.get(sl, []))}</b><span>{esc(nm)}</span></a>'
    for sl, (nm, _) in PROVS.items())
cifras_body = f"""<section class="block"><div class="wrap">
<h2 class="kicker" data-k="Impacto">A quiénes llegó su trabajo</h2>
{impacto_html()}
</div></section>
<section class="block alt"><div class="wrap">
<h2 class="kicker" data-k="Comisión de Economía 2023-2024">Cómo trabajó la Comisión de Economía</h2>
<div class="charts">{chart_embudo}{chart_dict}</div>
{chart_sesiones}
<p><a class="btn" href="~/gestion/balance-comision-economia-2023-2024.html">Ver el balance completo</a></p>
</div></section>
<section class="block"><div class="wrap">
<h2 class="kicker" data-k="Votaciones">Respaldo a sus iniciativas</h2>
{chart_votos}
</div></section>
<section class="block alt"><div class="wrap">
<h2 class="kicker" data-k="Elecciones 2026">La primera votación de Piura</h2>
{chart_eleccion}
</div></section>
<section class="block"><div class="wrap narrow">
<h2 class="kicker" data-k="2021-2026">Línea de tiempo</h2>
<ul class="feed">{tl_html}</ul>
</div></section>
<section class="block alt"><div class="wrap">
<h2 class="kicker" data-k="Territorio">Gestiones documentadas por provincia</h2>
<div class="tiles">{prov_tiles}</div>
<p class="chart-note">Número de gestiones con fuente publicadas en este sitio para cada provincia de Piura. Se actualiza con cada ficha nueva.</p>
</div></section>"""
add("cifras.html", "César Revilla en cifras: leyes, votos y a quiénes llegó",
    "César Revilla en cifras: 20 leyes desde la Comisión de Economía, 4 millones de trabajadores con su CTS, votos en el Pleno y su trayectoria 2021-2026.",
    cifras_body, h1="En cifras", lead="Lo que logró y a quiénes llegó, en gráficos. Cada dato enlaza a su fuente.",
    crumbs=[("En cifras", "cifras.html")], brand=False)

add("proyectos-de-ley.html", "Leyes de César Revilla en el Congreso del Perú",
    "Leyes y proyectos de César Revilla: Universidad de Huancabamba, Plan Hidráulico de Piura, AFP, CTS, Fonavi y mypes. Con número de ley y fuente.",
    f"""<section class="block"><div class="wrap">
<h2 class="kicker" data-k="Autor">Leyes y proyectos de su autoría</h2>
<table><thead><tr><th>Norma o proyecto</th><th>Qué hace</th><th>Estado</th></tr></thead><tbody>
<tr><td><a href="~/proyectos-de-ley/proyectos-2025-2026-salud-emergencias-titulos-rurales.html">PL 00150/2026-2031-CD</a></td><td>Garantiza el acceso inmediato a servicios de salud en emergencias. Primer proyecto como diputado.</td><td>En comisión (septiembre de 2026)</td></tr>
<tr><td><a href="~/proyectos-de-ley/proyectos-2025-2026-salud-emergencias-titulos-rurales.html">PL 13397, 12718 y 14091</a></td><td>Títulos de propiedad rural, trabajadores sociales en empresas y día compensable para personeros.</td><td>En comisión y con dictamen</td></tr>
<tr><td><a href="~/gestion/universidad-nacional-de-huancabamba-ley-32162.html">Ley 32162 (PL 8018/2023-CR)</a></td><td>Crea la Universidad Nacional de Huancabamba.</td><td>Ley publicada (noviembre de 2024)</td></tr>
<tr><td><a href="~/gestion/plan-hidraulico-piura-pl-7131.html">PL 7131</a></td><td>Declara de interés nacional el Plan Hidráulico de Piura.</td><td>Aprobado por unanimidad (julio de 2025)</td></tr>
<tr><td><a href="~/gestion/cas-covid-pl-2204-personal-de-salud.html">PL 2204</a></td><td>Pasa al personal de salud CAS COVID a contrato CAS regular.</td><td>Aprobado por el Pleno con 112 votos (julio de 2022)</td></tr>
<tr><td><a href="~/proyectos-de-ley/proyectos-economicos-2023.html">PL 4769, PL 4661, Ley 31616</a></td><td>Maquinaria ante desastres, mitigación ante El Niño y pasivos ambientales mineros.</td><td>Ver ficha</td></tr>
<tr><td><a href="~/proyectos-de-ley/pl-2902-2022-cr.html">PL 2902/2022-CR</a></td><td>Grado de bachiller sin trabajo de investigación obligatorio.</td><td>Presentado</td></tr>
</tbody></table>
{chart_votos}
</div></section>
<section class="block alt"><div class="wrap">
<h2 class="kicker" data-k="Comisión de Economía 2023-2024">Leyes logradas desde la Comisión de Economía que presidió</h2>
<p>Como presidente de la Comisión de Economía, Banca, Finanzas e Inteligencia Financiera, condujo 58 dictámenes y 20 leyes publicadas. <a href="~/gestion/balance-comision-economia-2023-2024.html">Ver el balance completo</a>.</p>
<table><thead><tr><th>Ley</th><th>Para quién</th></tr></thead><tbody>
<tr><td><a href="~/gestion/retiro-afp-2024-ley-32002.html">Ley 32002 · Retiro de AFP hasta 4 UIT</a></td><td>Afiliados al Sistema Privado de Pensiones</td></tr>
<tr><td><a href="~/gestion/retiro-cts-2024-comision-economia.html">Ley 32027 · Libre disposición del 100% de la CTS</a></td><td>Unos 4 millones de trabajadores</td></tr>
<tr><td>Ley 31888 · REPRO AFP III</td><td>Empleadores con aportes previsionales pendientes</td></tr>
<tr><td>Ley 31886 · Competencia en el transporte terrestre</td><td>Usuarios y empresas de transporte</td></tr>
<tr><td><a href="~/gestion/mypes-detracciones-ley-por-insistencia-2023.html">Uso libre de fondos de detracciones</a></td><td>Micro y pequeñas empresas</td></tr>
<tr><td><a href="~/gestion/balance-comision-economia-2023-2024.html">Devolución de aportes del Fonavi</a></td><td>Fonavistas</td></tr>
<tr><td><a href="~/gestion/balance-comision-economia-2023-2024.html">Nueva Ley de Contrataciones del Estado</a></td><td>Proveedores y entidades públicas</td></tr>
</tbody></table>
</div></section>""",
    h1="Leyes y proyectos", lead="Lo que César Revilla ha logrado en el Congreso del Perú, con número de ley y fuente.", crumbs=[("Leyes", "proyectos-de-ley.html")], brand=False)

# ============ GUÍAS (índice) ============
add("guias.html", "Guías ciudadanas sobre el Congreso y Piura",
    "Guías claras sobre el Congreso, los diputados de Piura y cómo pedir información pública. Con fuentes oficiales.",
    f"""<section class="block"><div class="wrap">
<div class="grid">{''.join(card('Guía', g['h1'], g['card'], g['path']) for g in GUIAS)}</div>
{pend("Publicar 1 guía nueva por semana. Ideas: cómo seguir un proyecto de ley, qué es la ANIN y Reconstrucción con Cambios, cómo funciona el presupuesto regional.")}
</div></section>""",
    h1="Guías ciudadanas", lead="Respuestas claras a las dudas más frecuentes sobre el Congreso y la vida pública en Piura.",
    crumbs=[("Guías", "guias.html")])

# ============ HUB: CONGRESO Y FUERZA POPULAR ============
HUB_FAQ = [
    ("¿Cuántos diputados y senadores tiene el Perú?", "130 diputados y 60 senadores desde el 27 de julio de 2026."),
    ("¿Cuántos diputados y senadores tiene Fuerza Popular?", "41 diputados y 22 senadores, la mayor bancada de ambas cámaras, según el conteo de la ONPE publicado por Infomercado."),
    ("¿Quién preside la Cámara de Diputados?", "Oscar Reto Otero, del Partido del Buen Gobierno, elegido con 74 votos para 2026–2027."),
    ("¿Quiénes son los diputados de Piura?", "Siete: César Revilla, Eduardo Castillo, Félix Chang, Carmela Paucará, María Silupú, Miguel Huamán y Henry Albañil. Piura también tiene la senadora Karla Schaefer."),
    ("¿Qué diputado de Piura lidera la votación?", "César Revilla, de Fuerza Popular, con 23,816 votos preferenciales."),
]
_hub_g = [g for g in GUIAS if g["slug"] in POLITICA_SLUGS]
add("congreso-2026-2031.html", "Congreso 2026–2031: Fuerza Popular, diputados y senadores",
    "Congreso bicameral del Perú 2026–2031: bancada de Fuerza Popular, diputados, senadores y los representantes de Piura, con César Revilla.",
    f"""<section class="block"><div class="wrap narrow">
<p class="resumen"><strong>En breve:</strong> el Congreso tiene 130 diputados y 60 senadores desde el 27 de julio de 2026. Fuerza Popular, con 41 diputados y 22 senadores, es la mayor bancada. César Revilla es uno de sus diputados por Piura.</p>
<h2>Guías sobre el Congreso, Fuerza Popular y Piura</h2>
<div class="grid">{''.join(card('Guía', g['h1'], g['card'], g['path']) for g in _hub_g)}</div>
<h2>Preguntas frecuentes</h2>
{''.join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in HUB_FAQ)}
<p class="upd">Fuentes: <a href="~/guias/fuerza-popular-congreso-2026-2031.html">Fuerza Popular en el Congreso</a> y <a href="~/guias/congreso-bicameral-peru-2026-2031.html">Congreso bicameral</a>.</p>
</div></section>""",
    h1="Congreso 2026–2031", lead="Fuerza Popular, diputados y senadores del Perú, y el lugar de César Revilla.",
    crumbs=[("Congreso", "congreso-2026-2031.html")], brand=False, date=PUB,
    ld_extra={"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in HUB_FAQ]})

# ============ PIURA Y PROVINCIAS ============
add("piura.html", "César Revilla en las 8 provincias de Piura",
    "Gestiones de César Revilla en las ocho provincias de Piura y la lista de sus distritos.",
    f"""<section class="block"><div class="wrap">
<p>César Revilla representa a toda la región. Piura tiene siete diputados; conoce <a href="~/guias/diputados-de-piura-2026-2031.html">quiénes son</a>.</p>
<div class="grid">{''.join(card('Provincia', 'Provincia de ' + n, f'{len(d)} distritos.', f'piura/{s}.html') for s, (n, d) in PROVS.items())}</div>
</div></section>""",
    h1="Piura, provincia por provincia", lead="Las ocho provincias de la región y las gestiones de César Revilla en cada una.",
    crumbs=[("Piura", "piura.html")])

for s, (n, d) in PROVS.items():
    fs = [ficha_by_slug(x) for x in PROV_FICHAS.get(s, [])]
    if fs:
        gest = '<div class="grid">' + "".join(card("Ficha", f["h1"], f["resumen"], f["path"]) for f in fs) + "</div>"
    else:
        gest = "<p>Aquí se publicarán las gestiones de César Revilla en esta provincia.</p>"
    body = f"""<section class="block"><div class="wrap narrow">
<p>{n} es una de las ocho provincias de la región Piura. Está formada por {len(d)} distritos: {', '.join(d)}.</p>
<h2>Gestiones de César Revilla en {n}</h2>
{gest}
{pend("Esta página queda noindex hasta que tenga fichas reales (PROV_FICHAS). Evita páginas vacías: Google las trata como contenido de poco valor. Validar la lista de distritos con el INEI.")}
<p><a href="~/piura.html">← Todas las provincias</a> · <a href="~/contacto.html">Escribir al despacho</a></p>
</div></section>"""
    add(f"piura/{s}.html", f"César Revilla en la provincia de {n}",
        f"Gestiones de César Revilla en la provincia de {n}, región Piura: obras, reuniones y distritos.", body,
        h1=f"Provincia de {n}", crumbs=[("Piura", "piura.html"), (f"Provincia de {n}", f"piura/{s}.html")], index=bool(fs))

# ============ BIOGRAFÍA ============
add("biografia.html", "Biografía de César Revilla, diputado por Piura",
    "Biografía de César Revilla Villanueva: cirujano dentista, diputado por Piura 2026–2031 y presidente de comisiones del Congreso.",
    f"""<section class="block"><div class="wrap narrow">
<p class="resumen"><strong>En breve:</strong> César Revilla (Chiclayo, 1987) es cirujano dentista y diputado de la República por Piura (2026–2031), de Fuerza Popular. Fue congresista por Piura (2021–2026) y presidió la Comisión de Economía.</p>
<h2>Datos clave</h2>
<dl class="facts">
<dt>Nombre</dt><dd>César Manuel Revilla Villanueva</dd>
<dt>Nacimiento</dt><dd>19 de marzo de 1987, Chiclayo (Lambayeque) {a_src('bio')}</dd>
<dt>Profesión</dt><dd>Cirujano dentista (2012)</dd>
<dt>Estudios</dt><dd>Cirujano dentista por la Universidad Inca Garcilaso de la Vega (2012). Bachiller en Estomatología (2011), magíster en Gestión de los Servicios de la Salud (2014) y doctor en Gestión Pública y Gobernabilidad (2021) por la Universidad César Vallejo. {a_src('vbp')} {a_src('eclara')}</dd>
<dt>Partido</dt><dd>Fuerza Popular</dd>
<dt>Cargo actual</dt><dd>Diputado de la República por Piura, periodo 2026–2031</dd>
<dt>Cargo anterior</dt><dd>Congresista por Piura, periodo 2021–2026</dd>
</dl>
<h2>Trayectoria legislativa</h2>
<ul class="feed">
<li><span class="tag">2026</span><p>Encabezó la votación regional de Piura con 23,816 votos preferenciales. <a href="~/gestion/revilla-lidera-votacion-piura-2026.html">Ver ficha</a>.</p>{a_src('diputados')}</li>
<li><span class="tag">2025</span><p>Presidió la comisión contra el terrorismo y el crimen organizado transnacional. <a href="~/gestion/comision-crimen-organizado-presidencia-2025.html">Ver ficha</a>.</p>{a_src('crimen1')}</li>
<li><span class="tag">2024–2025</span><p>Vocero de la bancada de Fuerza Popular. <a href="~/gestion/vocero-fuerza-popular-2024-2025.html">Ver ficha</a>.</p>{a_src('vocero1')}</li>
<li><span class="tag">2024</span><p>Autor del proyecto que dio origen a la Ley 32162, que crea la Universidad Nacional de Huancabamba. <a href="~/gestion/universidad-nacional-de-huancabamba-ley-32162.html">Ver ficha</a>.</p>{a_src('huanca1')}</li>
<li><span class="tag">2021–2026</span><p>Presidió la Comisión de Seguimiento a la Reconstrucción del Niño Costero. <a href="~/gestion/comision-reconstruccion-nino-costero.html">Ver ficha</a>.</p>{a_src('recons')}</li>
<li><span class="tag">Comisión de Economía</span><p>Presidió la Comisión de Economía, que sesionó en Piura. <a href="~/gestion/comision-economia-sesion-descentralizada-piura.html">Ver ficha</a>.</p>{a_src('econ')}</li>
</ul>
<h2>Trayectoria profesional</h2>
<p>Según su hoja de vida declarada al JNE, trabajó en EsSalud entre 2015 y 2017. Fue director del Hospital de Sullana (2015–2016), gerente de la Red Asistencial Piura (2016) y director del Centro de Atención Primaria III (2016–2017). {a_src('eclara')}</p>
{pend("Contrastar la trayectoria con la hoja de vida en votoinformado.jne.gob.pe y agregar comisiones actuales en la Cámara de Diputados.")}
</div></section>""",
    h1="Biografía de César Revilla", lead="Cirujano dentista y diputado por Piura. Datos verificables, con su fuente.",
    crumbs=[("Biografía", "biografia.html")], brand=False,
    ld_extra={"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": "¿Quién es César Revilla?", "acceptedAnswer": {"@type": "Answer", "text": "César Manuel Revilla Villanueva (Chiclayo, 19 de marzo de 1987) es cirujano dentista y diputado de la República del Perú por Piura para 2026–2031, de Fuerza Popular."}},
        {"@type": "Question", "name": "¿Qué cargos ha tenido César Revilla?", "acceptedAnswer": {"@type": "Answer", "text": "Fue congresista por Piura (2021–2026), presidente de la Comisión de Economía, Banca, Finanzas e Inteligencia Financiera y presidente de las comisiones de seguimiento a la Reconstrucción y contra el terrorismo y el crimen organizado."}},
        {"@type": "Question", "name": "¿Cuántos votos obtuvo César Revilla en 2026?", "acceptedAnswer": {"@type": "Answer", "text": "23,816 votos preferenciales, la primera votación de la región Piura."}}]})

# ============ TRANSPARENCIA / PRENSA / CONTACTO ============
_FICHA = "https://diputados.congreso.gob.pe/diputado/revilla-villanueva-cesar-manuel/"
TRANSP = [
    ("Hoja de vida", "Formación y trayectoria registradas en la Cámara de Diputados.", _FICHA + "sobre-el-integrante/hoja-de-vida/"),
    ("Cargos", "Comisiones y cargos que ocupa en el periodo 2026-2031.", _FICHA + "sobre-el-integrante/cargos/"),
    ("Proyectos de ley", "Todas sus proposiciones legislativas y su estado.", _FICHA + "labor-legislativa/proposiciones-legislativas/"),
    ("Mociones", "Mociones de orden del día presentadas.", _FICHA + "labor-legislativa/mociones/"),
    ("Pedidos de información", "Oficios enviados a entidades del Estado.", _FICHA + "pedidos-de-informacion/"),
    ("Informe de representación", "Lo que informa de su semana de representación en Piura.", _FICHA + "representacion/informe-representacion/"),
    ("Notas de prensa del Congreso", "Comunicados oficiales sobre su labor.", _FICHA + "prensa/noticias/"),
    ("Voto Informado (JNE)", "Plataforma del Jurado Nacional de Elecciones con hojas de vida y declaraciones de candidatos.", "https://votoinformado.jne.gob.pe/"),
]
add("transparencia.html", "Transparencia: hoja de vida y proyectos de César Revilla",
    "Fuentes oficiales para verificar la labor de César Revilla: hoja de vida, cargos, proyectos de ley, mociones, pedidos de información y representación.",
    f"""<section class="block"><div class="wrap narrow">
<p class="lead" style="color:var(--ink)">Todo lo que se publica en este sitio se puede contrastar con fuentes oficiales. Aquí están los registros públicos de César Revilla en la Cámara de Diputados y en el Jurado Nacional de Elecciones.</p>
<h2 class="kicker" data-k="Fuentes oficiales">Registros públicos</h2>
<div class="channels">{''.join(f'<a class="channel" href="{u}" rel="noopener" target="_blank"><b>{esc(t)}</b><small>{esc(d)}</small><span>Ver en la fuente oficial →</span></a>' for t, d, u in TRANSP)}</div>
<h2 class="kicker" data-k="Cómo verificamos">Nuestro criterio</h2>
<ul class="clean">
<li>Cada ficha de gestión enlaza a la nota del medio o al comunicado oficial que la respalda.</li>
<li>Las cifras se citan tal como aparecen en la fuente. Si una fuente da un rango o una estimación, lo decimos.</li>
<li>Si encuentras un error, escríbenos desde la página de <a href="~/contacto.html">contacto</a> o al correo institucional <a href="mailto:crevilla@congreso.gob.pe">crevilla@congreso.gob.pe</a>.</li>
</ul>
<p>¿Quieres pedir información a una entidad del Estado? Lee la <a href="~/guias/como-pedir-informacion-publica-peru.html">guía para pedir información pública</a>.</p>
{pend("Agregar respuestas documentadas a los cuestionamientos publicados, solo con documentos y fecha.")}
</div></section>""",
    h1="Transparencia", lead="Fuentes oficiales para verificar su trabajo.", crumbs=[("Transparencia", "transparencia.html")], brand=False)

MEDIOS = [  # (fecha iso, medio, titular, url, ficha propia o None)
    ("2026-10-22", "Panamericana", "César Revilla: Piura necesita un sistema integral de drenaje pluvial", SRC["dren"][1], "gestion/drenaje-pluvial-piura-fenomeno-el-nino.html"),
    ("2026-10-01", "Infobae", "Fuerza Popular no insistirá con los 66 puntos del pedido de facultades: «Entendemos que ese es el consenso»", SRC["infobae1001"][1], "guias/facultades-legislativas-2026-cesar-revilla.html"),
    ("2026-08-22", "RPP", "César Revilla respalda gestión del Ejecutivo frente a El Niño", SRC["rpp26"][1], "gestion/el-nino-2026-preparacion-piura.html"),
    ("2026-08-15", "La Razón", "César Revilla: «Queremos reducir la pobreza de 26% a menos de 15%»", SRC["razon26"][1], "gestion/agenda-2026-2031-pobreza-seguridad.html"),
    ("2026-07-30", "El Tiempo", "Piura, con recursos para El Niño: lo que informó Revilla", SRC["nino26"][1], "gestion/el-nino-2026-credito-suplementario-piura.html"),
    ("2026-07-21", "Canal N", "César Revilla sobre la Mesa Directiva de la Cámara de Diputados", SRC["canaln26"][1], None),
    ("2026-06-27", "El Tiempo", "Acreditan a representantes por Piura para el nuevo Congreso", SRC["acred"][1], "gestion/revilla-lidera-votacion-piura-2026.html"),
    ("2026-06-10", "Primicias Piura", "César Revilla es el candidato más votado de Piura para la Cámara de Diputados", "https://primiciaspiura.com/2026/cesar-revilla-es-el-candidato-mas-votado-de-piura-para-la-camara-de-diputados/", "gestion/revilla-lidera-votacion-piura-2026.html"),
    ("2025-08-07", "Infobae", "César Revilla será el nuevo portavoz de la bancada de Fuerza Popular", SRC["vocero2"][1], "gestion/vocero-fuerza-popular-2024-2025.html"),
    ("2024-11-12", "La Hora", "Piura: publican ley para la creación de la Universidad Nacional de Huancabamba", SRC["huanca2"][1], "gestion/universidad-nacional-de-huancabamba-ley-32162.html"),
    ("2024-10-23", "Caretas", "César Revilla presidirá la comisión de seguimiento de la Autoridad Nacional de Infraestructura", SRC["ani"][1], "gestion/ani-comision-seguimiento-2024.html"),
    ("2024-08-09", "El Comercio", "Fuerza Popular elige a su vocería 2024-2025, con César Revilla como primer vocero alterno", SRC["vocero1"][1], "gestion/vocero-fuerza-popular-2024-2025.html"),
    ("2024-05-02", "Infobae", "Retiro de CTS 2024: el Congreso aprobó liberar el 100% de los fondos", SRC["cts24"][1], "gestion/retiro-cts-2024-comision-economia.html"),
    ("2024-04-16", "América TV", "César Revilla: «Esperamos debatir y aprobar el proyecto de retiro mañana»", SRC["cts"][1], "gestion/retiro-cts-2024-comision-economia.html"),
    ("2024-03-25", "Infobae", "Retiro AFP: la Comisión de Economía aprueba liberar hasta 4 UIT", SRC["afp24"][1], "gestion/retiro-afp-2024-ley-32002.html"),
    ("2023-08-17", "RPP", "¿Quién es César Revilla, el nuevo presidente de la Comisión de Economía?", SRC["rpp23"][1], "gestion/comision-economia-presidencia-2023.html"),
    ("2023-08-14", "El Comercio", "César Revilla, elegido para presidir la Comisión de Economía: sus proyectos económicos", SRC["comercio23"][1], "proyectos-de-ley/proyectos-economicos-2023.html"),
    ("2022-07-02", "Piura Empresarial", "Congresista César Revilla: la estabilidad para los CAS COVID es una realidad", SRC["cas"][1], "gestion/cas-covid-pl-2204-personal-de-salud.html"),
    ("2021-09-03", "Cutivalú", "César Revilla propondrá sesión descentralizada de la comisión de Reconstrucción en el Bajo Piura", SRC["km980a"][1], "gestion/km-980-sesion-descentralizada-reconstruccion.html"),
]
OFICIALES = [
    ("2026-10-14", "Diputados de Fuerza Popular atienden demandas de infraestructura, prevención de riesgos y presupuesto para hospitales", SRC["congreso1014"][1], "gestion/puente-carnero-descolmatacion-tambogrande-las-lomas.html"),
    ("2025-07-24", "Plan Hidráulico de Piura: la Comisión Permanente aprueba su proyecto", SRC["planhid"][1], "gestion/plan-hidraulico-piura-pl-7131.html"),
    ("2025-07-07", "La comisión contra el crimen organizado sesiona en Piura", SRC["crimen2"][1], "gestion/crimen-organizado-sesion-descentralizada-piura-2025.html"),
    ("2025-03-27", "César Revilla dirigirá la comisión contra el terrorismo y el crimen organizado", SRC["crimen1"][1], "gestion/comision-crimen-organizado-presidencia-2025.html"),
    ("2024-10-17", "Aprueban dictamen para la creación de la Universidad Nacional de Huancabamba", SRC["huanca1"][1], "gestion/universidad-nacional-de-huancabamba-ley-32162.html"),
    ("2024-07-09", "La Comisión de Economía aprobó 58 dictámenes y logró 20 leyes", SRC["econbal"][1], "gestion/balance-comision-economia-2023-2024.html"),
    ("2024-06-12", "Pleno aprueba régimen excepcional del Impuesto a la Renta", SRC["ir24"][1], "gestion/regimen-excepcional-impuesto-renta-2024.html"),
    ("2023-11-04", "La Comisión de Economía ofrece eliminar trabas ante El Niño", SRC["candados"][1], "gestion/el-nino-2023-comision-economia-facilidades.html"),
    ("2023-10-12", "El Congreso insiste en fortalecer la capacidad financiera de las mypes", SRC["mypes23"][1], "gestion/mypes-detracciones-ley-por-insistencia-2023.html"),
    ("2023-08-16", "La Comisión de Economía trabajará por leyes populares y no populistas", SRC["econ23"][1], "gestion/comision-economia-presidencia-2023.html"),
    ("2022-04-21", "Alcaldes de Piura piden presupuesto en audiencia de la comisión de Reconstrucción", SRC["alcaldes22"][1], "gestion/reconstruccion-audiencia-alcaldes-piura-2022.html"),
]
def _media_items(rows, with_outlet=True):
    out, year = [], None
    for r in rows:
        if with_outlet:
            iso, medio, tit, url, ficha = r
        else:
            iso, tit, url, ficha = r; medio = "Congreso de la República"
        y = iso[:4]
        if y != year:
            out.append(f'<li class="year"><span>{y}</span></li>'); year = y
        extra = f' · <a href="~/{ficha}">Ver ficha</a>' if ficha else ""
        out.append(f'<li class="press"><span class="press-src">{esc(medio)}</span><a class="press-title" href="{url}" rel="noopener" target="_blank">{esc(tit)}</a>'
                   f'<span class="press-meta">{fdate(iso)}{extra}</span></li>')
    return "".join(out)
_outlets = sorted({m for _, m, *_ in MEDIOS})
medios_body = f"""<section class="block"><div class="wrap narrow">
<p class="lead" style="color:var(--ink)">Notas y entrevistas sobre el trabajo de César Revilla publicadas por medios nacionales y regionales del Perú, ordenadas por fecha. Cada titular enlaza a la nota original.</p>
<ul class="chips">{''.join(f'<li><span>{esc(o)}</span></li>' for o in _outlets)}</ul>
<h2 class="kicker" data-k="Prensa">En los medios</h2>
<ul class="press-list">{_media_items(MEDIOS)}</ul>
<h2 class="kicker" data-k="Fuente oficial">Notas del Congreso de la República</h2>
<ul class="press-list">{_media_items(OFICIALES, False)}</ul>
</div></section>"""
_items_ld = [{"@type": "ListItem", "position": i, "url": r[3], "name": r[2]} for i, r in enumerate(MEDIOS, 1)]
add("medios.html", "César Revilla en los medios: entrevistas y notas de prensa",
    "Entrevistas y notas sobre César Revilla en RPP, El Comercio, Infobae, Canal N, América TV, Caretas y medios de Piura, con enlace a cada nota original.",
    medios_body, h1="En los medios", lead="Lo que han publicado los medios sobre su trabajo, con enlace a cada nota.",
    crumbs=[("En los medios", "medios.html")], brand=False,
    ld_extra={"@context": "https://schema.org", "@type": "ItemList", "name": "César Revilla en los medios", "itemListElement": _items_ld})

CANALES = [
    ("Facebook", "facebook.com/cesarrevillav", "https://www.facebook.com/cesarrevillav", "Página oficial"),
    ("TikTok", "@cesarrevillav", "https://www.tiktok.com/@cesarrevillav", "Cuenta oficial"),
    ("Cámara de Diputados", "Ficha oficial del diputado", "https://diputados.congreso.gob.pe/diputado/revilla-villanueva-cesar-manuel/", "Perfil institucional"),
    ("Correo institucional", "crevilla@congreso.gob.pe", "mailto:crevilla@congreso.gob.pe", "Despacho congresal"),
    ("Sitio web", "cesarrevilla.com", BASE + "/", "Sitio personal"),
    ("Wikidata", "Q108414723", "https://www.wikidata.org/wiki/Q108414723", "Ficha de datos abiertos"),
]
canales_body = f"""<section class="block"><div class="wrap narrow">
<p class="lead" style="color:var(--ink)">Estos son los canales oficiales confirmados de César Manuel Revilla Villanueva, diputado de la República del Perú por Piura (2026-2031). Todos usan el mismo nombre y enlazan a este sitio.</p>
<div class="channels">{''.join(f'<a class="channel" href="{u}" rel="me noopener" target="_blank"><b>{esc(n)}</b><span>{esc(h)}</span><small>{esc(t)}</small></a>' for n, h, u, t in CANALES)}</div>
<h2>¿Encontraste otra cuenta?</h2>
<p>Si ves una cuenta con su nombre que no figura en esta lista, no la consideres oficial y escribe al correo institucional para confirmarlo. Las cuentas falsas pueden reportarse desde cada red social.</p>
</div></section>"""
add("canales-oficiales.html", "Canales oficiales de César Revilla",
    "Cuentas oficiales de César Revilla, diputado del Perú por Piura: Facebook, TikTok, correo institucional y ficha de la Cámara de Diputados.",
    canales_body, h1="Canales oficiales", lead="Sus cuentas verificables, en un solo lugar.", crumbs=[("Canales oficiales", "canales-oficiales.html")], brand=False)

add("prensa.html", "Sala de prensa de César Revilla",
    "Biografía corta, datos clave y contacto de prensa de César Revilla, diputado del Perú por Piura 2026–2031 y expresidente de la Comisión de Economía.",
    f"""<section class="block"><div class="wrap narrow">
<h2>Biografía corta</h2>
<p>César Manuel Revilla Villanueva (Chiclayo, 1987) es cirujano dentista, magíster en Gestión de los Servicios de la Salud y doctor en Gestión Pública y Gobernabilidad. Es diputado de la República por Piura para el periodo 2026–2031, tras obtener la votación más alta de la región con 23,816 votos preferenciales. Como congresista (2021–2026) presidió la Comisión de Economía, Banca, Finanzas e Inteligencia Financiera, que en 2023-2024 logró 20 leyes, entre ellas la liberación del 100% de la CTS y el retiro de AFP de hasta 4 UIT. También presidió las comisiones de seguimiento a la Reconstrucción, a la Autoridad Nacional de Infraestructura y contra el terrorismo y el crimen organizado.</p>
<h2>Datos clave</h2>
<dl class="facts">
<dt>Cargo</dt><dd>Diputado de la República del Perú por Piura, 2026–2031</dd>
<dt>Cargo anterior</dt><dd>Congresista por Piura, 2021–2026</dd>
<dt>Partido</dt><dd>Fuerza Popular</dd>
<dt>Profesión</dt><dd>Cirujano dentista</dd>
<dt>Temas</dt><dd>Economía y empleo, El Niño y reconstrucción, seguridad ciudadana, salud, agua y educación</dd>
<dt>Contacto institucional</dt><dd><a href="mailto:crevilla@congreso.gob.pe">crevilla@congreso.gob.pe</a></dd>
</dl>
<h2>Cómo citarlo</h2>
<p>César Revilla Villanueva, diputado de la República del Perú por Piura (2026–2031), de Fuerza Popular. Su ficha oficial está en <a href="https://diputados.congreso.gob.pe/diputado/revilla-villanueva-cesar-manuel/" rel="noopener" target="_blank">diputados.congreso.gob.pe</a>. Para datos y fuentes verificables, consulta <a href="~/congreso-2026-2031.html">Congreso 2026–2031</a> y <a href="~/proyectos-de-ley.html">Leyes</a>.</p>
<h2>Recursos</h2>
<div class="grid">
{card("Prensa", "En los medios", "Entrevistas y notas publicadas, con enlace a cada original.", "medios.html")}
{card("Datos", "En cifras", "Sus logros y a quiénes llegaron, en gráficos con fuente.", "cifras.html")}
{card("Identidad", "Canales oficiales", "Sus cuentas oficiales y contacto institucional.", "canales-oficiales.html")}
</div>
{pend("Agregar fotos oficiales en alta resolución con crédito y un contacto de prensa del despacho (nombre y teléfono).")}
</div></section>""",
    h1="Sala de prensa", lead="Material para periodistas.", crumbs=[("Prensa", "prensa.html")], brand=False)

add("contacto.html", "Contacto con el despacho de César Revilla",
    "Contacto de César Revilla, diputado por Piura: correo institucional, redes oficiales y cómo presentar consultas o pedidos de gestión.",
    f"""<section class="block"><div class="wrap narrow">
<p class="resumen"><strong>En breve:</strong> el canal institucional es el correo <a href="mailto:crevilla@congreso.gob.pe">crevilla@congreso.gob.pe</a>. Indica tu provincia, distrito y el tema de tu consulta.</p>
<h2>Canales oficiales</h2>
<dl class="facts">
<dt>Correo institucional</dt><dd><a href="mailto:crevilla@congreso.gob.pe">crevilla@congreso.gob.pe</a></dd>
<dt>Facebook</dt><dd><a href="https://www.facebook.com/cesarrevillav" rel="me noopener" target="_blank">facebook.com/cesarrevillav</a></dd>
<dt>TikTok</dt><dd><a href="https://www.tiktok.com/@cesarrevillav" rel="me noopener" target="_blank">@cesarrevillav</a></dd>
<dt>Ficha oficial</dt><dd><a href="https://diputados.congreso.gob.pe/diputado/revilla-villanueva-cesar-manuel/" rel="noopener" target="_blank">Cámara de Diputados del Perú</a></dd>
</dl>
<h2>Qué incluir en tu mensaje</h2>
<ul class="clean">
<li>Tu nombre y cómo responderte.</li>
<li>Provincia y distrito.</li>
<li>Qué necesitas y, si existe, el documento o expediente relacionado.</li>
</ul>
<p>Usaremos tus datos solo para responderte. Lee la <a href="~/politica-de-privacidad.html">política de privacidad</a>.</p>
<h2>Para prensa</h2>
<p>Material y datos clave en la <a href="~/prensa.html">sala de prensa</a>. Para pedir información pública a una entidad, usa la <a href="~/guias/como-pedir-informacion-publica-peru.html">guía paso a paso</a>.</p>
{pend("Agregar dirección de la oficina de representación en Piura, teléfono, WhatsApp del despacho y horario.")}
</div></section>""",
    h1="Contacto", lead="Consultas, pedidos de gestión y solicitudes de agenda.", crumbs=[("Contacto", "contacto.html")])

add("politica-de-privacidad.html", "Política de privacidad",
    "Qué datos recoge este sitio, cómo se miden las visitas con Google Analytics y cómo ejercer tus derechos según la Ley 29733.",
    """<section class="block"><div class="wrap narrow">
<p class="resumen"><strong>En breve:</strong> este sitio no tiene cuentas ni formularios. Solo mide visitas de forma estadística con Google Analytics, sin fines publicitarios.</p>
<h2>Quién es el responsable</h2>
<p>Este es el sitio personal de César Manuel Revilla Villanueva, diputado de la República del Perú por Piura. No es un portal oficial del Congreso de la República.</p>
<h2>Qué datos se recogen</h2>
<p>El sitio no pide datos personales ni tiene registro de usuarios. Para saber cuántas personas lo visitan y qué páginas leen, usa Google Analytics 4, que registra datos estadísticos como páginas vistas, ciudad y país aproximados, tipo de dispositivo y la página desde la que llegaste. Tenemos desactivadas las señales de Google para publicidad personalizada.</p>
<h2>Cookies</h2>
<p>Google Analytics usa cookies para distinguir visitas. Puedes bloquearlas desde tu navegador o instalar el <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener" target="_blank">complemento de inhabilitación de Google Analytics</a>.</p>
<h2>Si nos escribes</h2>
<p>Si escribes a <a href="mailto:crevilla@congreso.gob.pe">crevilla@congreso.gob.pe</a>, usaremos tus datos solo para responder tu consulta.</p>
<h2>Tus derechos</h2>
<p>La Ley 29733, Ley de Protección de Datos Personales, reconoce los derechos de acceso, rectificación, cancelación y oposición. Para ejercerlos, escribe al correo indicado.</p>
<h2>Enlaces externos</h2>
<p>Este sitio enlaza a medios, entidades públicas y redes sociales. No controlamos sus políticas de privacidad.</p>
<p class="upd">Última actualización: 2 de noviembre de 2026.</p>
</div></section>""",
    h1="Política de privacidad", lead="Cómo se tratan los datos en este sitio.", crumbs=[("Privacidad", "politica-de-privacidad.html")], index=False, brand=False)

# ============ INICIO ============
faq_html = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
latest = sorted([f for f in FICHAS if f["folder"] == "gestion"], key=lambda f: f["iso"] or "0000", reverse=True)[:4]
ticker_items = "".join(f'<a href="~/temas/{s}.html">{esc(t["h1"])}</a>' for s, t in TEMAS.items())
n_fichas = len(FICHAS)
home_body = f"""<section class="hero"><div class="grid-bg" aria-hidden="true"></div><div class="wrap hero-grid">
<div>
<p class="eyebrow in">Diputado de la República por Piura · 2026–2031</p>
<h1 class="in">César <span class="hl">Revilla</span></h1>
<p class="lead in">Diputado de la República y expresidente de la Comisión de Economía del Congreso. Leyes para trabajadores, pensionistas y mypes de todo el Perú, y gestión para Piura frente a El Niño. Todo con su fuente.</p>
<p class="in"><a class="btn" href="~/proyectos-de-ley.html">Ver sus leyes</a><a class="btn ghost" href="~/gestion.html">Su gestión</a></p>
</div>
{retrato()}
</div></section>
<div class="ticker" aria-label="Temas"><div class="track">{ticker_items}{ticker_items}{ticker_items}{ticker_items}</div></div>
<section class="stats"><div class="wrap">
<div class="stat"><strong data-count="23816">23,816</strong><span>votos preferenciales en Piura (2026), la primera votación de la región</span></div>
<div class="stat"><strong data-count="4">4</strong><span>comisiones del Congreso presididas</span></div>
<div class="stat"><strong data-count="{n_fichas}">{n_fichas}</strong><span>gestiones y leyes documentadas con fuente en este sitio</span></div>
<div class="stat"><strong data-count="20">20</strong><span>leyes logradas como presidente de la Comisión de Economía (2023-2024)</span></div>
</div></section>
<section class="block"><div class="wrap">
<h2 class="kicker" data-k="Impacto">A quiénes llegó su trabajo</h2>
{impacto_html(6)}
<p><a class="btn" href="~/cifras.html">Ver todo en cifras</a></p>
</div></section>
<section class="block alt"><div class="wrap">
<h2 class="kicker" data-k="Agenda">Ejes de trabajo</h2>
<div class="grid">{tema_cards}</div></div></section>
<section class="block"><div class="wrap">
<h2 class="kicker" data-k="Lo más reciente">Últimas gestiones documentadas</h2>
<div class="grid">{''.join(card('Gestión', f['h1'], f['resumen'], f['path']) for f in latest)}</div>
<p><a class="btn" href="~/gestion.html">Ver todas las gestiones</a></p>
</div></section>
{galeria()}
<section class="block"><div class="wrap">
<h2 class="kicker" data-k="Para el ciudadano">Guías ciudadanas</h2>
<div class="grid">{''.join(card('Guía', g['h1'], g['card'], g['path']) for g in GUIAS)}</div>
<p><a href="~/guias.html">Ver todas las guías →</a></p>
</div></section>
<section class="block dark"><div class="wrap">
<h2 class="kicker" data-k="Prensa">Lo han entrevistado y citado</h2>
<ul class="outlets">{''.join(f'<li>{esc(o)}</li>' for o in ["RPP", "El Comercio", "Infobae", "Canal N", "América TV", "Caretas", "Panamericana", "La Razón", "El Tiempo"])}</ul>
<p><a class="btn" href="~/medios.html">Ver todas las notas</a><a class="btn ghost" href="~/canales-oficiales.html">Canales oficiales</a></p>
</div></section>
<section class="block alt"><div class="wrap">
<h2 class="kicker" data-k="Territorio">En las 8 provincias de Piura</h2>
<ul class="chips">{''.join(f'<li><a href="~/piura/{s}.html">{n}</a></li>' for s, (n, _) in PROVS.items())}</ul>
</div></section>
<section class="block"><div class="wrap narrow">
<h2 class="kicker" data-k="Preguntas">Preguntas frecuentes</h2>
{faq_html}
</div></section>"""
add("index.html", "César Revilla | Diputado por Piura · Fuerza Popular",
    "César Revilla, diputado por Piura de Fuerza Popular (2026–2031) en el Congreso bicameral del Perú: leyes sobre AFP, CTS, mypes y El Niño, con fuentes.",
    home_body, home=True, ld_extra=faq_ld, brand=False)


# ============ GENERACIÓN ============
def rfc822(iso):
    import datetime
    d = datetime.date.fromisoformat(iso)
    return d.strftime("%a, %d %b %Y 00:00:00 -0500")


def build():
    sitemap = []
    for p in PAGES:
        full = os.path.join(OUT, p["path"])
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(layout(p))
        if p["index"]:
            sitemap.append((BASE + "/" + ("" if p["path"] == "index.html" else p["path"][:-5]), p["date"] or PUB))

    e404 = dict(path="404.html", title="Página no encontrada", desc="La página que buscas no existe.", kind="page", index=False,
                h1="Página no encontrada", lead=None, crumbs=[], date=None, keys=[], home=False, ld_extra=None, in_feed=False, brand=True,
                body='<section class="block"><div class="wrap narrow"><p>No encontramos esa página. Vuelve al <a href="index.html">inicio</a>, revisa la <a href="gestion.html">gestión</a> o las <a href="guias.html">guías</a>.</p></div></section>')
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(layout(e404))

    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                 + "\n".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in sitemap) + "\n</urlset>\n")
    with open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8") as fh:
        fh.write(BASE.replace("https://", "") + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("".join(f"User-agent: {b}\nAllow: /\n\n" for b in
                         ["*", "Googlebot", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended"])
                 + f"Sitemap: {BASE}/sitemap.xml\n")
    explica_ll = f"- [Explica: índice por temas]({BASE}/explica)\n" + "\n".join(
        f"- [{e['h1']}]({BASE}/{e['path'][:-5]}): {e['resumen']}" for e in EXPLICA)
    guias_ll = "\n".join(f"- [{g['h1']}]({BASE}/{g['path'][:-5]}): {g['resumen']}" for g in GUIAS)
    with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"""# César Revilla · Diputado del Perú por Piura

> Sitio personal de César Manuel Revilla Villanueva, diputado por Piura (2026–2031) de Fuerza Popular, congresista 2021–2026 y expresidente de la Comisión de Economía del Congreso. No es un portal oficial del Congreso. Cada dato enlaza a su fuente.

## Datos clave
- Cargo: diputado de la República del Perú por Piura, periodo 2026–2031, bancada de Fuerza Popular.
- Votación 2026: 23,816 votos preferenciales, la más alta de Piura.
- Comisión de Economía (2023–2024): 58 dictámenes y 20 leyes, entre ellas retiro de AFP (Ley 32002) y libre disposición de la CTS (Ley 32027).
- Autor del proyecto que dio origen a la Ley 32162, que crea la Universidad Nacional de Huancabamba.
- Fuerza Popular: 41 de 130 diputados y 22 de 60 senadores en el Congreso bicameral 2026–2031.
- Ficha oficial: https://diputados.congreso.gob.pe/diputado/revilla-villanueva-cesar-manuel/

## Páginas principales
- [Inicio]({BASE}/): quién es y preguntas frecuentes
- [Congreso 2026–2031]({BASE}/congreso-2026-2031): Fuerza Popular, diputados y senadores
- [Biografía]({BASE}/biografia)
- [Leyes y proyectos]({BASE}/proyectos-de-ley)
- [Gestión por Piura]({BASE}/gestion)
- [En los medios]({BASE}/medios)
- [Canales oficiales]({BASE}/canales-oficiales)
- [Transparencia]({BASE}/transparencia)

## Explica (explicaciones con fuentes)
{explica_ll}

## Guías
{guias_ll}
""")

    items = "".join(
        f"<item><title>{esc(p['h1'])}</title><link>{BASE}/{p['path'][:-5]}</link><guid>{BASE}/{p['path'][:-5]}</guid>"
        f"<pubDate>{rfc822(p['date'])}</pubDate><description>{esc(p['desc'])}</description></item>"
        for p in PAGES if p["in_feed"])
    with open(os.path.join(OUT, "feed.xml"), "w", encoding="utf-8") as fh:
        fh.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>César Revilla · Gestiones y guías</title>'
                 f'<link>{BASE}/</link><description>Gestiones documentadas y guías ciudadanas de César Revilla, diputado por Piura.</description>'
                 f'<language>es-PE</language>{items}</channel></rss>\n')

    with open(os.path.join(OUT, "styles.css"), encoding="utf-8") as fh:
        css = fh.read()
    with open(os.path.join(OUT, "index.html"), encoding="utf-8") as fh:
        idx = fh.read()
    with open(os.path.join(OUT, "vista-previa.html"), "w", encoding="utf-8") as fh:
        fh.write(idx.replace('<link rel="stylesheet" href="styles.css">', f"<style>{css}</style>"))
    print(f"OK: {len(PAGES) + 1} páginas | {len(sitemap)} en sitemap | {sum(1 for p in PAGES if p['in_feed'])} en RSS | DRAFT={DRAFT}")


if __name__ == "__main__":
    build()
