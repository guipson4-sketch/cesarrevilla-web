# -*- coding: utf-8 -*-
"""Datos del apartado «Explica» (cesarrevilla.com/explica).

Regla editorial: una explicación solo se publica si cada afirmación sale de una fuente de EXP_SRC.
Para agregar una explicación: (1) sumar la fuente en EXP_SRC, (2) agregar un dict en EXPLICA,
(3) asignarla a un tema en EXP_TEMAS, (4) correr  python3 build.py && python3 audit.py.
Las explicaciones de coyuntura (hechos del día) van en COYUNTURA con la misma estructura.
"""

EXP_SRC = {
    "andinabicam": ("Agencia Andina: «Vuelve el Congreso Bicameral» (2026)",
                    "https://portal.andina.pe/edpespeciales/2026/vuelve_el_congreso_bicameral/index.html"),
    "larep1117": ("La República (17 de noviembre de 2025)",
                  "https://larepublica.pe/politica/2025/11/17/con-el-nuevo-congreso-bicameral-no-sera-facil-la-vacancia-presidencialhnews-1592208"),
    "folletoproy": ("Congreso de la República: folleto «Proyecto de ley»",
                    "https://www.congreso.gob.pe/Docs/sites/eventos/proyecto_ley/Folleto_proyecto_Ley.pdf"),
    "andinaemerg": ("Agencia Andina (19 de septiembre de 2023)",
                    "https://andina.pe/agencia/noticia-conoce-es-estado-emergencia-y-que-situaciones-rige-955859.aspx"),
    "andinaemerg2": ("Agencia Andina (24 de septiembre de 2023)",
                     "https://andina.pe/agencia/noticia-conoce-cuales-son-las-restricciones-un-estado-emergencia-956472.aspx"),
    "ytpleno1119": ("Congreso de la República, Sesión del Pleno del 19/11/2026 (video oficial; intervención de César Revilla desde 6:48:57)", "https://www.youtube.com/watch?v=ehMRuO8zzls&t=24537s"),
    "conglc1119": ("Congreso de la República (19 de noviembre de 2026): Liga Parlamentaria de Amistad Perú-Corea del Sur cuenta con nuevo Comité Ejecutivo",
                   "https://comunicaciones.congreso.gob.pe/noticias/liga-parlamentaria-de-amistad-peru-corea-del-sur-cuenta-con-nuevo-comite-ejecutivo/"),
    "congre1119": ("Congreso de la República (19 de noviembre de 2026): Reinició debate parlamentario sobre dictamen de presupuesto del sector público 2027",
                   "https://comunicaciones.congreso.gob.pe/noticias/reinicio-debate-parlamentario-sobre-dictamen-de-presupuesto-del-sector-publico-2027/"),
    "congdip1119": ("Congreso de la República (19 de noviembre de 2026): Diputados fijan posición y transmiten necesidades de pobladores en debate de presupuesto público",
                    "https://comunicaciones.congreso.gob.pe/noticias/diputados-fijan-posicion-y-transmiten-necesidades-de-pobladores-en-debate-de-presupuesto-publico"),
    "congsen1119": ("Congreso de la República (19 de noviembre de 2026): Senadores piden reactivar obras y cerrar brechas de agua y saneamiento",
                    "https://comunicaciones.congreso.gob.pe/noticias/senadores-piden-reactivar-obras-y-cerrar-brechas-de-agua-y-saneamiento/"),
    "andina1119": ("Agencia Andina (19 de noviembre de 2026): Congreso continúa debate del presupuesto público para el Año Fiscal 2027",
                   "https://andina.pe/agencia/noticia-congreso-continua-debate-del-presupuesto-publico-para-ano-fiscal-2027-1100637.aspx"),
    "infobae1028": ("Infobae (28 de octubre de 2026): Retiro de AFP 2026, los siguientes pasos de las 4 UIT en la Comisión de Economía del Congreso",
                    "https://www.infobae.com/peru/2026/10/28/retiro-de-afp-2026-los-siguientes-pasos-de-las-4-uit-en-la-comision-de-economia-del-congreso/"),
    "larep1110": ("La República (10 de noviembre de 2026): Noveno retiro de AFP sigue en comisión, proyecto de hasta S/22.000 espera evaluación en el Congreso",
                  "https://larepublica.pe/economia/2026/11/10/noveno-retiro-de-afp-sigue-en-comision-proyecto-de-hasta-s22000-espera-evaluacion-en-el-congreso-hnews-669950"),
    "gestioncron": ("Gestión: «Congreso debatirá y votará el Presupuesto 2027 del 17 al 20 de noviembre: ¿cuál es el cronograma?» (2026)",
                    "https://gestion.pe/peru/politica/congreso-debatira-y-votara-el-presupuesto-2027-del-17-al-20-de-noviembre-cual-es-el-cronograma-noticia/"),
    "larep1105": ("La República (5 de noviembre de 2026): dictamen del Presupuesto 2027",
                  "https://larepublica.pe/economia/2026/11/05/presupuesto-publico-2027-congreso-aprueba-dictamen-por-mas-de-s266500-millones-hnews-371465"),
    "andinapres": ("Agencia Andina (5 de noviembre de 2026): dictamen del Presupuesto 2027",
                   "https://andina.pe/agencia/noticia-comision-bicameral-aprueba-dictamen-presupuesto-2027-mas-s-266500-millones-1098746.aspx"),
}

# Temas del apartado. Una página de tema agrupa explicaciones, guías y fichas de gestión ya publicadas.
# `gestion` enlaza al hub de gestión equivalente (clave de TEMAS en build.py).
EXP_TEMAS = {
    "congreso-y-politica": dict(
        h1="Congreso y política", seo="Congreso y política del Perú, explicado",
        desc="Cómo funciona el Congreso bicameral del Perú: leyes, control político, participación ciudadana y el trabajo de César Revilla.",
        intro="Cómo se hacen las leyes, qué controla cada cámara y cómo puede participar la ciudadanía en el Congreso bicameral que inició el 27 de julio de 2026.",
        guias=["como-se-crea-una-ley-en-el-peru", "que-hace-un-diputado-del-peru", "que-hace-un-senador-del-peru",
               "congreso-bicameral-peru-2026-2031", "facultades-legislativas-2026-cesar-revilla", "fuerza-popular-congreso-2026-2031"],
        fichas=[], gestion=None),
    "seguridad-ciudadana": dict(
        h1="Seguridad ciudadana", seo="Seguridad ciudadana en el Perú, explicada",
        desc="Qué es un estado de emergencia, qué derechos toca y qué ha hecho César Revilla contra el crimen organizado.",
        intro="Los conceptos que aparecen en las noticias sobre inseguridad, explicados con fuentes, y el trabajo de César Revilla en la comisión contra el crimen organizado.",
        guias=[], fichas=["comision-crimen-organizado-presidencia-2025", "crimen-organizado-sesion-descentralizada-piura-2025"],
        gestion="temas/seguridad-ciudadana.html"),
    "clima-y-desastres": dict(
        h1="Clima y desastres", seo="Fenómeno El Niño y lluvias en Piura",
        desc="Fenómeno El Niño, lluvias y reconstrucción en Piura: gestiones documentadas de César Revilla y guía para entender el tema.",
        intro="El Fenómeno El Niño y las lluvias son el tema que más afecta a Piura. Aquí están las gestiones documentadas de César Revilla y la guía para entenderlo.",
        guias=["cesar-revilla-fenomeno-el-nino"],
        fichas=["el-nino-2026-preparacion-piura", "el-nino-2026-credito-suplementario-piura", "drenaje-pluvial-piura-fenomeno-el-nino",
                "comision-reconstruccion-nino-costero"],
        gestion="temas/lluvias-y-drenaje.html"),
    "economia-y-empleo": dict(
        h1="Economía y empleo", seo="Economía, AFP y CTS: leyes aprobadas",
        desc="Retiro de AFP, CTS y otras leyes económicas aprobadas por la Comisión de Economía que presidió César Revilla, con número de ley.",
        intro="Las leyes económicas de la Comisión de Economía que presidió César Revilla entre 2023 y 2024, con su número de ley y fuente.",
        guias=[], fichas=["retiro-afp-2024-ley-32002", "retiro-cts-2024-comision-economia", "balance-comision-economia-2023-2024"],
        gestion="temas/economia-y-empleo.html"),
    "ciudadania": dict(
        h1="Ciudadanía y participación", seo="Participación ciudadana en el Perú",
        desc="Cómo pedir información pública, presentar un proyecto de ley como ciudadano y plantear un caso al despacho de César Revilla.",
        intro="Las herramientas que tiene una persona para participar: pedir información, proponer una ley y hacer llegar un problema a su representante.",
        guias=["como-pedir-informacion-publica-peru", "semana-de-representacion-que-es"], fichas=[], gestion=None),
}

EXPLICA = [
    dict(slug="interpelacion-censura-vacancia-que-hace-cada-camara", tema="congreso-y-politica", iso="2026-11-14",
         h1="Interpelación, censura y vacancia: qué decide cada cámara del Congreso",
         seo="Censura, interpelación y vacancia en el Perú",
         desc="Qué cámara interpela y censura ministros, quién decide la vacancia presidencial y quién resuelve las acusaciones constitucionales.",
         resumen="Con el Congreso bicameral, solo la Cámara de Diputados puede interpelar y censurar ministros. El Senado resuelve las acusaciones constitucionales y participa en la vacancia presidencial.",
         card="Qué controla la Cámara de Diputados y qué el Senado.",
         html="""<h2>Dos cámaras, funciones distintas</h2>
<p>Desde el 27 de julio de 2026 el Congreso tiene dos cámaras: la Cámara de Diputados y el Senado. Cada una tiene poderes de control propios. Esta es la distribución, según la Agencia Andina.</p>
<div class="tablewrap"><table>
<thead><tr><th>Mecanismo</th><th>Qué es</th><th>Dónde se decide</th></tr></thead>
<tbody>
<tr><td>Interpelación</td><td>El Congreso cita a un ministro para que explique su gestión.</td><td>Cámara de Diputados, la única que puede hacerlo</td></tr>
<tr><td>Censura</td><td>Retiro de la confianza a un ministro.</td><td>Cámara de Diputados, la única que puede hacerlo</td></tr>
<tr><td>Cuestión de confianza</td><td>El Consejo de Ministros pide el respaldo del Congreso a una política.</td><td>Cámara de Diputados</td></tr>
<tr><td>Acusación constitucional</td><td>Denuncia contra un alto funcionario por infracciones a la Constitución o delitos en el cargo.</td><td>La formula la Cámara de Diputados y la resuelve el Senado</td></tr>
<tr><td>Vacancia presidencial</td><td>Terminar el mandato del presidente en los casos que fija la Constitución.</td><td>Senado, según Andina. Ver abajo</td></tr>
</tbody></table></div>
<p class="upd">La columna «Dónde se decide» sale de la Agencia Andina. Las definiciones son explicaciones generales.</p>
<h2>Qué puede decidir el Senado</h2>
<p>Cuando la Cámara de Diputados presenta una acusación constitucional, el Senado la resuelve. Puede suspender, destituir o inhabilitar al funcionario hasta por diez años, según Andina.</p>
<h2>La vacancia por incapacidad moral</h2>
<p>La República explicó en noviembre de 2025 que la vacancia presidencial por incapacidad moral permanente requerirá la aprobación de ambas cámaras. Según esa nota, en cada una hace falta el voto de al menos dos tercios del número legal de miembros, según los artículos 193 del reglamento de la Cámara de Diputados y 194 del reglamento del Senado. La nota calcula que en el Senado equivalen a 40 senadores.</p>
<p class="upd">Las reglas del Congreso pueden cambiar. Antes de citar estas cifras, confirma el texto vigente en el <a href="https://www.congreso.gob.pe/" rel="noopener" target="_blank">portal del Congreso</a>.</p>
<h2>Y César Revilla</h2>
<p>César Revilla es diputado por Piura. Por eso trabaja en la cámara que interpela, censura y formula las acusaciones constitucionales. Conoce <a href="~/guias/que-hace-un-diputado-del-peru.html">qué hace un diputado</a> y <a href="~/guias/que-hace-un-senador-del-peru.html">qué hace un senador</a>.</p>""",
         faq=[("¿Qué cámara puede interpelar y censurar ministros?",
               "Solo la Cámara de Diputados, según la Agencia Andina."),
              ("¿Quién resuelve una acusación constitucional?",
               "La formula la Cámara de Diputados y la resuelve el Senado, que puede suspender, destituir o inhabilitar al funcionario hasta por diez años."),
              ("¿Cuántos votos hacen falta para la vacancia por incapacidad moral?",
               "Según La República (noviembre de 2025), al menos dos tercios del número legal de miembros en cada cámara. En el Senado serían 40 votos."),
              ("¿Qué es la cuestión de confianza?",
               "Es el pedido del Consejo de Ministros para que el Congreso respalde una política. En el Congreso bicameral la debate la Cámara de Diputados.")],
         keys=["andinabicam", "larep1117"]),
    dict(slug="iniciativa-legislativa-ciudadana-como-presentar-un-proyecto-de-ley", tema="ciudadania", iso="2026-11-14",
         h1="Cómo presentar un proyecto de ley como ciudadano en el Perú",
         seo="Cómo presentar un proyecto de ley ciudadano",
         desc="Qué es la iniciativa legislativa ciudadana: cuántas firmas se necesitan, qué verifica la ONPE y cómo avanza un proyecto de ley en el Congreso.",
         resumen="Una persona puede proponer una ley al Congreso reuniendo firmas de al menos el 0.3% de la población electoral. La ONPE verifica las firmas antes de que el proyecto llegue al Congreso.",
         card="Firmas necesarias y pasos del trámite.",
         html="""<h2>Quiénes pueden proponer una ley</h2>
<p>Según el folleto del Congreso, pueden presentar proyectos de ley el Presidente de la República y los congresistas. También los otros poderes del Estado, las instituciones públicas autónomas, los gobiernos regionales y locales y los colegios profesionales, en las materias que les corresponden. Los ciudadanos pueden hacerlo si ejercen el derecho de iniciativa conforme a ley.</p>
<h2>Qué necesita una iniciativa ciudadana</h2>
<ul class="clean">
<li>Firmas de al menos el 0.3% de la población electoral, según el artículo 11 de la Ley 26300.</li>
<li>Una resolución de la ONPE que declare expedito el procedimiento, después de comprobar las firmas.</li>
<li>Un oficio de envío firmado por uno o por los diez primeros ciudadanos que suscriben la iniciativa.</li>
</ul>
<h2>Cómo avanza un proyecto</h2>
<ol class="clean">
<li><strong>Presentación.</strong> Se registra en la Oficialía Mayor y se publica en el portal del Congreso.</li>
<li><strong>Comisiones.</strong> Lo estudian una o dos comisiones, que tienen hasta 30 días útiles para emitir un dictamen.</li>
<li><strong>Publicación del dictamen.</strong> Se difunde en el portal, en la Gaceta del Congreso o en El Peruano.</li>
<li><strong>Debate en el Pleno</strong> y aprobación con doble votación. La segunda se realiza al menos siete días calendario después de la primera.</li>
<li><strong>Promulgación.</strong> El Presidente tiene 15 días útiles para promulgar u observar la ley.</li>
<li><strong>Publicación en El Peruano.</strong> La ley rige desde el día siguiente, salvo que diga otra cosa.</li>
</ol>
<p class="upd">El folleto es anterior al Congreso bicameral. Hoy los proyectos ingresan por la Cámara de Diputados; mira la <a href="~/guias/como-se-crea-una-ley-en-el-peru.html">guía de cómo se crea una ley</a>.</p>
<h2>Otra vía: plantear tu idea a un parlamentario</h2>
<p>Reunir las firmas requiere organización. Otra forma de hacer llegar una propuesta es plantearla a un congresista, que puede presentarla con el respaldo de su grupo parlamentario. Si quieres que el despacho de César Revilla conozca tu caso, escríbele desde la página de <a href="~/contacto.html">contacto</a>. No es garantía de que se convierta en proyecto, pero queda registrado.</p>""",
         faq=[("¿Cuántas firmas se necesitan para presentar un proyecto de ley ciudadano?",
               "Al menos el 0.3% de la población electoral, según la Ley 26300 y el folleto del Congreso."),
              ("¿Quién revisa las firmas?",
               "La ONPE comprueba las firmas y emite una resolución que declara expedito el procedimiento."),
              ("¿Cuánto demora una comisión en dictaminar?",
               "Tiene un máximo de 30 días útiles para emitir dictamen, según el folleto del Congreso."),
              ("¿Puedo pedirle a un congresista que presente mi idea?",
               "Sí. Los congresistas tienen iniciativa legislativa y presentan proyectos a través de su grupo parlamentario.")],
         keys=["folletoproy"]),
    dict(slug="estado-de-emergencia-peru-que-es-y-que-derechos-restringe", tema="seguridad-ciudadana", iso="2026-11-14",
         h1="Estado de emergencia en el Perú: qué es y qué derechos restringe",
         seo="Estado de emergencia: qué es y qué restringe",
         desc="Qué es un estado de emergencia, quién lo decreta, cuánto dura y qué derechos pueden restringirse, con fuentes oficiales y de prensa.",
         resumen="Es un régimen de excepción que el Presidente decreta por un plazo máximo de 60 días ante alteraciones del orden interno o catástrofes. Permite restringir algunos derechos, pero nunca desterrar a nadie.",
         card="Quién lo decreta, plazos y derechos restringidos.",
         html="""<h2>Qué es</h2>
<p>El estado de emergencia es un régimen de excepción. Puede aplicarse en todo el territorio nacional o en parte de él, por un plazo determinado, según la Agencia Andina.</p>
<h2>Cuándo se declara</h2>
<p>Se declara ante la perturbación de la paz o del orden interno, una catástrofe o graves circunstancias que afecten la vida de la Nación.</p>
<h2>Quién lo decreta y por cuánto tiempo</h2>
<ul class="clean">
<li>Lo decreta el Presidente de la República, con acuerdo del Consejo de Ministros, y da cuenta al Congreso o a la Comisión Permanente.</li>
<li>Dura como máximo 60 días. Para prorrogarlo hace falta un nuevo decreto.</li>
<li>Si el Presidente lo dispone, las Fuerzas Armadas pueden asumir el control del orden interno.</li>
</ul>
<h2>Qué derechos pueden restringirse</h2>
<p>Durante un estado de emergencia pueden restringirse o suspenderse:</p>
<ul class="clean">
<li>la libertad y la seguridad personales,</li>
<li>la inviolabilidad del domicilio,</li>
<li>la libertad de reunión,</li>
<li>la libertad de tránsito en el territorio.</li>
</ul>
<p>Bajo ninguna circunstancia se puede desterrar a nadie.</p>
<p class="upd">Las notas de Andina son de septiembre de 2023. Para saber qué zonas están hoy en emergencia y con qué reglas, revisa el decreto vigente en <a href="https://www.elperuano.pe/" rel="noopener" target="_blank">El Peruano</a>.</p>
<h2>El trabajo de César Revilla contra el crimen organizado</h2>
<p>En 2025 César Revilla presidió la comisión del Congreso contra el terrorismo y el crimen organizado transnacional. Mira la <a href="~/gestion/comision-crimen-organizado-presidencia-2025.html">ficha de su presidencia</a> y la <a href="~/gestion/crimen-organizado-sesion-descentralizada-piura-2025.html">sesión descentralizada en Piura</a>.</p>""",
         faq=[("¿Quién declara el estado de emergencia?",
               "El Presidente de la República, con acuerdo del Consejo de Ministros, y da cuenta al Congreso o a la Comisión Permanente."),
              ("¿Cuánto dura un estado de emergencia?",
               "Hasta 60 días. Para prorrogarlo se necesita un nuevo decreto."),
              ("¿Qué derechos se pueden restringir?",
               "La libertad y seguridad personales, la inviolabilidad del domicilio, la libertad de reunión y la libertad de tránsito. Nunca se puede desterrar a una persona."),
              ("¿Las Fuerzas Armadas pueden controlar el orden interno?",
               "Sí, cuando el Presidente lo dispone en el decreto.")],
         keys=["andinaemerg", "andinaemerg2"]),
    dict(slug="presupuesto-publico-2027-que-es-como-se-aprueba-y-que-incluye", tema="economia-y-empleo", iso="2026-11-17",
         h1="Presupuesto público 2027: qué incluye y cómo se vota esta semana en el Congreso",
         seo="Presupuesto 2027: qué incluye y cómo se vota",
         desc="El Presupuesto 2027 suma S/ 266,506 millones. Qué incluye, cuánto va a educación y salud, y el cronograma del debate en el Pleno del 17 al 20 de noviembre.",
         resumen="El dictamen del Presupuesto 2027 suma S/ 266,506 millones. El Pleno lo debate del 17 al 20 de noviembre y lo vota el viernes 20.",
         card="Cuánto es, qué incluye y qué día se vota.",
         html="""<h2>Qué es el presupuesto público</h2>
<p>La Ley de Presupuesto fija cuánto dinero podrá gastar el Estado en el año y en qué: salarios, hospitales, colegios, carreteras y programas sociales. Esta semana el Pleno del Congreso debate la del año fiscal 2027.</p>
<h2>Cuánto es y cómo se reparte</h2>
<p>El 5 de noviembre de 2026 la Comisión Bicameral de Presupuesto aprobó el dictamen con 29 votos a favor, 1 en contra y 4 abstenciones. Según La República, el monto es de S/ 266,506 millones, 3.5% más que el presupuesto inicial de 2026 (unos S/ 8,945 millones adicionales).</p>
<div class="tablewrap"><table>
<thead><tr><th>Nivel de gobierno</th><th>Monto (millones de soles)</th></tr></thead>
<tbody>
<tr><td>Gobierno nacional</td><td>166,613</td></tr>
<tr><td>Gobiernos regionales</td><td>58,672</td></tr>
<tr><td>Gobiernos locales</td><td>41,222</td></tr>
</tbody></table></div>
<p>Entre los sectores, La República reporta S/ 52,198 millones para educación, S/ 32,208 millones para salud y S/ 26,014 millones para transporte. La nota menciona también recursos para seguridad ciudadana, programas sociales y prevención frente al Fenómeno El Niño, sin montos.</p>
<p class="upd">Los totales por nivel suman S/ 1 millón más que el total, probablemente por redondeo, según la propia nota.</p>
<h2>Qué medidas incluye el dictamen</h2>
<ul class="clean">
<li><strong>Trabajadores CAS:</strong> las entidades podrán modificar su presupuesto hasta el 31 de marzo de 2027 para pagar gratificaciones, CTS y aportes a EsSalud de 226,401 trabajadores CAS.</li>
<li><strong>Personal de salud:</strong> prevé incorporar unos 5,010 profesionales, técnicos y auxiliares asistenciales por concurso público de méritos, en plazas vacantes. Prohíbe nuevos contratos CAS y por locación de servicios para labores asistenciales permanentes, sin afectar la renovación de los CAS vigentes.</li>
<li><strong>Programa Contigo:</strong> el Midis podrá transferir recursos a la ONP para pensiones y gastos operativos de más de 142,000 personas con discapacidad severa en situación de pobreza.</li>
<li><strong>Control del gasto:</strong> prohíbe usar presupuesto en celebraciones y agasajos en 2027, salvo los vinculados a las funciones de cada entidad, y refuerza los controles sobre compromisos que pasan a años siguientes.</li>
<li><strong>Compras a mypes:</strong> facilidades para financiar los núcleos ejecutores de compras del Ministerio de la Producción, según Andina.</li>
</ul>
<h2>Cuándo se debate y se vota</h2>
<p>Según el cronograma que publicó Gestión, el Pleno trabaja así:</p>
<div class="tablewrap"><table>
<thead><tr><th>Día</th><th>Qué ocurre</th></tr></thead>
<tbody>
<tr><td>Martes 17</td><td>Se sustentan los dictámenes de presupuesto, endeudamiento y equilibrio financiero. Intervienen el presidente del Consejo de Ministros y el ministro de Economía.</td></tr>
<tr><td>Miércoles 18</td><td>Se sustentan los pliegos de los sectores y de organismos autónomos, como la Corte Suprema, la Fiscalía, el Tribunal Constitucional, el JNE y la Defensoría.</td></tr>
<tr><td>Jueves 19</td><td>Debate en el Senado y en la Cámara de Diputados: tres horas por cámara, repartidas entre los seis grupos parlamentarios.</td></tr>
<tr><td>Viernes 20</td><td>Se presenta el texto final y se vota el Presupuesto, el Endeudamiento y el Equilibrio Financiero para 2027.</td></tr>
</tbody></table></div>
<p class="upd">Este cronograma puede cambiar. Confirma las sesiones en el <a href="https://www.congreso.gob.pe/" rel="noopener" target="_blank">portal del Congreso</a>.</p>
<h2>Y César Revilla</h2>
<p>César Revilla es diputado por Piura y presidió la Comisión de Economía entre 2023 y 2024. Revisa las <a href="~/explica/economia-y-empleo.html">leyes económicas</a> de esa comisión y cómo <a href="~/guias/como-se-crea-una-ley-en-el-peru.html">se crea una ley</a>.</p>""",
         faq=[("¿De cuánto es el Presupuesto 2027?",
               "El dictamen suma S/ 266,506 millones, 3.5% más que el presupuesto inicial de 2026, según La República."),
              ("¿Cuándo se vota el Presupuesto 2027 en el Pleno?",
               "El debate va del 17 al 20 de noviembre de 2026 y la votación está prevista el viernes 20, según Gestión."),
              ("¿Cuánto se destina a educación y salud en 2027?",
               "S/ 52,198 millones a educación y S/ 32,208 millones a salud, según La República."),
              ("¿Cuánto recibirán los gobiernos regionales y locales?",
               "Los gobiernos regionales S/ 58,672 millones y los gobiernos locales S/ 41,222 millones, según La República.")],
         keys=["larep1105", "andinapres", "gestioncron"]),
    dict(slug="agenda-19-noviembre-2026-canal-n-liga-corea-pleno-presupuesto", tema="economia-y-empleo", iso="2026-11-19",
         h1="Agenda del 19 de noviembre de 2026: Canal N, Liga Perú–Corea del Sur y debate del Presupuesto 2027",
         seo="Agenda de Revilla: 19 de noviembre de 2026",
         desc="Qué tenía programado el diputado César Revilla el 19 de noviembre de 2026 y qué ocurrió ese día en el Pleno y en la Liga Perú–Corea del Sur.",
         resumen="El 19 de noviembre de 2026, César Revilla tenía tres actividades: entrevista en Canal N, instalación de la Liga Perú–Corea del Sur y el Pleno Bicameral sobre el Presupuesto 2027.",
         card="Su agenda del jueves 19 y lo que pasó en el Congreso ese día.",
         html="""<figure class="agenda"><img src="~/img/agenda-2026-11-19.jpg" alt="Agenda de actividades del diputado César Revilla del jueves 19 de noviembre de 2026: entrevista en Canal N, Liga Parlamentaria de Amistad Perú–Corea del Sur y Pleno Bicameral" width="800" loading="lazy" style="max-width:100%;height:auto;border-radius:12px"><figcaption>Agenda difundida por el despacho del diputado César Revilla.</figcaption></figure>
<h2>Su agenda del jueves 19 de noviembre de 2026</h2>
<p>Según la agenda difundida por su despacho, el diputado por Piura César Revilla (Fuerza Popular) tenía tres actividades:</p>
<div class="tablewrap"><table>
<thead><tr><th>Hora</th><th>Actividad</th><th>Lugar</th></tr></thead>
<tbody>
<tr><td>8:00 a. m.</td><td>Entrevista en Canal N con la periodista Melissa Peschiera</td><td>Montero Rosas 1050, Santa Beatriz, Lima</td></tr>
<tr><td>9:00 a. m.</td><td>Elección e instalación del Comité Ejecutivo de la Liga Parlamentaria de Amistad Perú–Corea del Sur</td><td>Sala 5 «Gustavo Mohme Llona», Edificio Víctor Raúl Haya de la Torre</td></tr>
<tr><td>10:00 a. m.</td><td>Pleno Bicameral: debate del Presupuesto del Estado para 2027</td><td>Hemiciclo del Congreso</td></tr>
</tbody></table></div>
<h2>Liga Parlamentaria de Amistad Perú–Corea del Sur</h2>
<p>El Congreso informó el 19 de noviembre que la Liga quedó instalada y que eligió por unanimidad a María Candelaria Ramos Rosales (Fuerza Popular) como presidenta. La vicepresidenta es Milagros Takayama Jiménez (Fuerza Popular) y el secretario, Leo Miguel De Paz Lancho (Renovación Popular). Sus integrantes acordaron elaborar un plan de trabajo para presentarlo a la Asamblea General. La Liga busca estrechar los vínculos de amistad y cooperación entre ambos países.</p>
<h2>El debate del Presupuesto 2027 en el Pleno</h2>
<p>Según el Congreso, el Pleno retomó el 19 de noviembre, a las 10:12 h, el debate de los dictámenes de la Ley de Presupuesto 2027, la Ley de Equilibrio Financiero y la Ley de Endeudamiento del Sector Público. Por acuerdo de la Junta de Portavoces Conjunta, senadores y diputados tienen tres horas cada grupo de cámara para intervenir, repartidas entre los grupos parlamentarios.</p>
<p>Durante el debate, diputados de Piura plantearon pedidos para la región, entre ellos fondos para reactivar obras paralizadas en la sierra, la culminación de establecimientos de salud en Ayabaca, Huancabamba, Huarmaca y Los Algarrobos, y el nombramiento de docentes de la Universidad Nacional de Piura. Después, la sesión pasó a cuarto intermedio y continuará el viernes 20 de noviembre a las 4:00 p. m., para elaborar un texto sustitutorio de los dictámenes.</p>
<p class="upd">César Revilla intervino en este debate: <a href="~/explica/cesar-revilla-pleno-19-noviembre-2026-propuestas-presupuesto-2027.html">lee lo que propuso para el Presupuesto 2027</a> (video desde 6:48:57).</p>
<h2>Para entender el tema</h2>
<p>Lee <a href="~/explica/presupuesto-publico-2027-que-es-como-se-aprueba-y-que-incluye.html">qué incluye el Presupuesto 2027 y cómo se vota</a> y <a href="~/guias/como-se-crea-una-ley-en-el-peru.html">cómo se crea una ley en el Perú</a>.</p>""",
         faq=[("¿Qué actividades tuvo César Revilla el 19 de noviembre de 2026?",
               "Según la agenda de su despacho, una entrevista en Canal N a las 8:00 a. m., la elección e instalación del Comité Ejecutivo de la Liga Parlamentaria de Amistad Perú–Corea del Sur a las 9:00 a. m. y el Pleno Bicameral sobre el Presupuesto 2027 a las 10:00 a. m."),
              ("¿Quién preside la Liga Parlamentaria de Amistad Perú–Corea del Sur?",
               "María Candelaria Ramos Rosales (Fuerza Popular), elegida por unanimidad el 19 de noviembre de 2026, según el Congreso."),
              ("¿Se votó el Presupuesto 2027 el 19 de noviembre?",
               "No. El Pleno debatió los dictámenes y pasó a cuarto intermedio. Según el Congreso, la sesión continúa el viernes 20 de noviembre a las 4:00 p. m.")],
         keys=["conglc1119", "congre1119", "congdip1119"]),
    dict(slug="cesar-revilla-pleno-19-noviembre-2026-propuestas-presupuesto-2027", tema="economia-y-empleo", iso="2026-11-20",
         h1="César Revilla en el Pleno del 19 de noviembre de 2026: lo que propuso para el Presupuesto 2027",
         seo="César Revilla en el Pleno: Presupuesto 2027",
         desc="Qué dijo César Revilla en el Pleno del 19-nov-2026: propuestas de articulado para el Presupuesto 2027, con transcripción del video oficial.",
         resumen="En dos minutos, el diputado César Revilla planteó al Pleno propuestas de articulado para el Presupuesto 2027: drenaje pluvial, obras por impuestos, personal de salud, Fuerzas Armadas y empleo temporal.",
         card="Sus propuestas para el Presupuesto 2027, con transcripción.",
         html="""<h2>En pocas palabras</h2>
<p>El 19 de noviembre de 2026, durante el debate del Presupuesto 2027, el presidente de la sesión le dio la palabra al diputado César Revilla por dos minutos (desde 6:48:57 del video). Leyó una serie de propuestas de articulado para incorporar en las leyes en debate. Habló hasta las 6:51:26.</p>
<h2>Lo que propuso</h2>
<ul class="clean">
<li><strong>Drenaje pluvial:</strong> financiamiento de proyectos de drenaje pluvial en las ciudades de Sullana, Talara y Chiclayo.</li>
<li><strong>Obras paralizadas:</strong> reactivar inversiones paralizadas y acelerar intervenciones estratégicas con el mecanismo de obras por impuestos.</li>
<li><strong>Personal de salud:</strong> cambio de grupo ocupacional y de línea de carrera, y nombramiento progresivo del personal contratado por emergencia COVID.</li>
<li><strong>Fuerzas Armadas:</strong> que las operaciones de endeudamiento en trámite al 31 de diciembre de 2026 puedan aprobarse en el primer trimestre de 2027 para la operatividad de las Fuerzas Armadas.</li>
<li><strong>Tribunal Constitucional:</strong> financiamiento para su transformación digital y renovación tecnológica.</li>
<li><strong>Recuperación económica:</strong> transferencias financieras para el plan de inversiones en transmisión de recuperación post COVID.</li>
<li><strong>Sechura:</strong> una disposición complementaria al Decreto Legislativo 996 (recursos de la promoción de la inversión privada en programas sociales) para ayudar a la provincia de Sechura.</li>
<li><strong>Junta Nacional de Justicia:</strong> autorización para financiar el fortalecimiento de sus funciones constitucionales.</li>
<li><strong>Empleo temporal:</strong> que el Ministerio de Economía asigne S/ 261 millones adicionales al programa Trabaja Perú (unidad ejecutora 005, pliego 012 del Ministerio de Trabajo).</li>
</ul>
<h2>Transcripción del tramo</h2>
<blockquote>
<p>«Presidente, la propuesta de articulado para el financiamiento de los proyectos de drenajes pluviales en la ciudad de [Sullana], Talara y Chiclayo. Presidente, la propuesta de articulado para la reactivación de obras de inversiones paralizadas y ejecución acelerada de intervenciones estratégicas mediante el mecanismo de obras por impuestos. La propuesta de la disposición complementaria final del cambio de grupo ocupacional, cambio de línea de carrera del personal de salud y el nombramiento progresivo de los [CAS] COVID. La incorporación en la ley de endeudamiento 2027 [para] disponer que las operaciones de endeudamiento comprendidas en los alcances del numeral 4 del 3.2 del artículo [de la] ley 32515, ley de endeudamiento del sector público para el año fiscal 2026, que al 31 de diciembre del 2026 se encuentren en trámite puedan ser aprobadas durante el primer trimestre del año fiscal 2027 para la operatividad de las Fuerzas Armadas. Presidente, propuesta de artículo para el financiamiento para la transformación digital y la renovación de tecnología en el Tribunal Constitucional; propuesta de artículo para transferencias financieras para el plan de inversiones en transmisión de recuperación económica post COVID en Perú; la modificación del decreto legislativo 996 […] incorporándose una disposición complementaria final […] para ayudar a la provincia de [Sechura]. Presidente, la autorización para el financiamiento del fortalecimiento de las funciones constitucionales de la Junta Nacional de Justicia. […] Autorizar al Ministerio de Economía y Finanzas a asignar en el presupuesto del sector público para el año 2027 recursos adicionales a la unidad ejecutora 005, programa para la generación de empleo social inclusivo Trabaja Perú, en el pliego 012 del Ministerio de Trabajo y Promoción del Empleo, por la suma de 261 millones de soles. Eso es todo, presidente. Muchas gracias.»</p>
</blockquote>
<p class="upd">Cómo leer esta transcripción: se obtuvo de los subtítulos generados automáticamente del video oficial del Congreso y puede tener errores. Los corchetes marcan palabras corregidas por contexto y los puntos suspensivos, tramos omitidos por ser ininteligibles; los nombres de lugares ([Sullana], [Sechura]) los transcribió mal el sistema automático. Para el texto exacto, escucha el video desde <a href="https://www.youtube.com/watch?v=ehMRuO8zzls&t=24537s" rel="noopener" target="_blank">6:48:57</a>.</p>
<h2>Contexto</h2>
<p>Estas propuestas se presentaron en el debate de la Ley de Presupuesto 2027, la Ley de Equilibrio Financiero y la Ley de Endeudamiento del Sector Público. Lee <a href="~/explica/pleno-19-noviembre-2026-que-se-dijo-presupuesto-2027.html">de qué se habló en el Pleno y qué dijo cada bancada</a> y <a href="~/en-vivo.html">sigue las sesiones en vivo</a>.</p>""",
         faq=[("¿Qué dijo César Revilla en el Pleno del 19 de noviembre de 2026?",
               "Planteó propuestas de articulado para el Presupuesto 2027: drenaje pluvial en Sullana, Talara y Chiclayo, obras por impuestos, carrera del personal de salud, operatividad de las Fuerzas Armadas, fondos para el Tribunal Constitucional y la Junta Nacional de Justicia, ayuda a Sechura y S/ 261 millones para Trabaja Perú."),
              ("¿Cuánto tiempo habló César Revilla en el Pleno?",
               "Tuvo dos minutos y su intervención va de 6:48:57 a 6:51:26 del video oficial de la sesión."),
              ("¿Dónde puedo ver la intervención de César Revilla?",
               "En el video oficial de la sesión del Pleno del 19 de noviembre de 2026 en el canal de YouTube del Congreso, desde la hora 6:48:57.")],
         keys=["ytpleno1119", "congre1119", "congdip1119"]),
    dict(slug="pleno-19-noviembre-2026-que-se-dijo-presupuesto-2027", tema="economia-y-empleo", iso="2026-11-20",
         h1="Pleno del 19 de noviembre de 2026: de qué se habló y qué dijo cada bancada sobre el Presupuesto 2027",
         seo="Pleno del 19-nov: qué dijo cada bancada",
         desc="Resumen con fuentes de la sesión del Pleno del 19 de noviembre de 2026: temas, pedidos por bancada, pedidos para Piura y cómo terminó el debate.",
         resumen="El 19 de noviembre de 2026, senadores y diputados de seis bancadas pidieron obras, más salud y educación y derechos laborales al debatir el Presupuesto 2027. La sesión pasó a cuarto intermedio.",
         card="De qué se habló, qué pidió cada bancada y cómo terminó.",
         html="""<h2>En pocas palabras</h2>
<p>El jueves 19 de noviembre de 2026 el Pleno Bicameral debatió los dictámenes de la Ley de Presupuesto 2027 (S/ 266,506 millones), la Ley de Equilibrio Financiero y la Ley de Endeudamiento del Sector Público. Según el Congreso, intervinieron 28 diputados de seis bancadas y numerosos senadores. Casi todos pidieron lo mismo: dinero para obras concretas en sus regiones. Las bancadas Juntos por el Perú, Partido del Buen Gobierno y Renovación Popular además criticaron recortes en salud, vivienda y educación. La sesión pasó a cuarto intermedio y continúa el viernes 20 de noviembre a las 4:00 p. m.</p>
<h2>Los temas que más se repitieron</h2>
<ul class="clean">
<li><strong>Obras paralizadas, agua y saneamiento:</strong> pedidos de fondos para terminar obras en Cusco, Piura, Huancavelica, Loreto, Puno, Tumbes y otras regiones.</li>
<li><strong>Salud:</strong> hospitales y centros de salud sin terminar, y nombramiento del personal que trabajó durante la pandemia (ex CAS COVID).</li>
<li><strong>Trabajadores del Estado:</strong> pase de CAS al régimen 728, negociación colectiva, escalas salariales y CTS pendiente.</li>
<li><strong>Educación y universidades:</strong> nombramiento de docentes, pago de sentencias judiciales y fondos para universidades públicas.</li>
<li><strong>Control del gasto:</strong> críticas a obras sin uso o sin terminar y pedidos de más supervisión de la Contraloría.</li>
<li><strong>Distribución regional:</strong> reclamos por cómo se reparte el dinero entre regiones.</li>
</ul>
<h2>Qué dijo cada bancada: diputados</h2>
<div class="tablewrap"><table>
<thead><tr><th>Bancada</th><th>Qué plantearon (según el Congreso)</th></tr></thead>
<tbody>
<tr><td>Fuerza Popular</td><td>Diethell Columbus pidió al MEF evaluar siete inversiones de agua y desagüe en la macrorregión sur. Javier Castro dijo que el nuevo Congreso ahorró S/ 700 millones para obras (300 millones iniciales y 400 millones más esta semana). Auristela Obando pidió obras de movilidad en el Callao. Carmela Paucará pidió reactivar obras paralizadas en la sierra de Piura. Pier Figari cuestionó obras que llamó «elefantes blancos», entre ellas el Museo de Pachacamac.</td></tr>
<tr><td>Juntos por el Perú</td><td>Oswar Cahuasa cuestionó que salud reciba S/ 32,208 millones y pidió restituir S/ 608 millones y concluir el Hospital de Pucallpa. Amalia Palomino pidió financiar pensiones dignas y pagar la CTS 2025, y reclamó por el reparto de obras entre regiones. Luis Jibaja insistió en rehabilitar la pista del aeropuerto de Jaén. Analí Márquez priorizó Cusco, el aeropuerto de Chinchero y el Gasoducto Sur Peruano. Jacqueline Tapullima pidió inversiones preventivas ante El Niño en San Martín. Ernesto Zunini cuestionó que no se renueve la autorización para financiar servicios en centros poblados.</td></tr>
<tr><td>Partido del Buen Gobierno</td><td>Neri Fernández pidió no recortar inversión en colegios, carreteras y agua para pagar gasto corriente. Romina Uribe pidió fondos para la búsqueda de personas desaparecidas. Fernando Huby rechazó artículos que, según él, flexibilizan el régimen laboral. Luis Quispe pidió destrabar vías en la selva central y cuestionó el gasto en el Viaducto Santa Rosa. Miguel Huamán recordó cuatro puestos de salud de Piura sin terminar. Rossana Alayza cuestionó el recorte en infraestructura educativa en riesgo.</td></tr>
<tr><td>Renovación Popular</td><td>Diego Bazán pidió mejoras para trabajadores de la Sunat y transferencias a universidades públicas. José Baella pidió actualizar el incentivo CAFAE de los trabajadores del INPE.</td></tr>
<tr><td>Partido Cívico Obras</td><td>Arturo Eusebio propuso destinar al menos 50% de ciertos saldos al pago de sentencias a docentes. Heber López pidió ejecutar la Ley 32390 sobre plazas docentes. Henry Albañil pidió titular a 27 docentes de la Universidad Nacional de Piura. Dina Hancco pidió inversiones en la sierra sur. Juan Cabrera pidió financiar el canal de Tacalaya (Tacna).</td></tr>
<tr><td>Ahora Nación</td><td>Marleny Arminta pidió agua y camino vecinal en Arequipa. Ángel Meneses pidió incorporar a trabajadores de Sunarp al régimen 728. Helard Sonco pidió vías y saneamiento en Puno. José Marcelo Salazar propuso mecanismos ágiles para financiar proyectos locales en ejecución.</td></tr>
</tbody></table></div>
<h2>Qué dijo cada bancada: senadores</h2>
<div class="tablewrap"><table>
<thead><tr><th>Bancada</th><th>Qué plantearon (según el Congreso)</th></tr></thead>
<tbody>
<tr><td>Fuerza Popular</td><td>Martha Moyano pidió acelerar obras paralizadas y priorizar proyectos de gran escala. Rafael Yamashiro pidió mantener las compras centralizadas de equipos médicos y reforzar la lucha contra el cáncer. Víctor Flores pidió agua y alcantarillado en Utcubamba (Amazonas). Héctor Ventura pidió reconstruir el hospital de Zarumilla (Tumbes) y mejorar el agua en La Palma.</td></tr>
<tr><td>Partido del Buen Gobierno</td><td>Flavio Figallo calificó la propuesta de «inercial» y planteó que municipios creen sus propias empresas de agua. Susana Matute pidió mejorar las pensiones de docentes jubilados con cáncer. Patricia Iturregui advirtió que el presupuesto no financia la Ley de Acceso Universal al Agua.</td></tr>
<tr><td>Ahora Nación</td><td>Mirtha Vásquez pidió terminar obras de agua en Loreto y Cusco y fondos para personas afectadas por metales pesados y ollas comunes. Jaime Delgado pidió S/ 4.6 millones para la Universidad Nacional de Música.</td></tr>
<tr><td>Juntos por el Perú</td><td>Silvana Robles pidió continuar inversiones rurales de agua y nombrar progresivamente al personal ex CAS de salud. Jaime Quito advirtió recortes en seguridad ciudadana, TBC y VIH. Wilfredo Verano, Serafín Luján, Hugo Ccahuana y Víctor Cutipa pidieron obras en Cusco, Huánuco y Madre de Dios. Percy Osorio criticó el aumento de Defensa (28.5%) frente a recortes en vivienda, saneamiento y salud.</td></tr>
<tr><td>Renovación Popular</td><td>Lourdes Alcorta cuestionó un gasto de S/ 11 millones en equipos para la misa del papa y pidió más control de la Contraloría. Absalón Vásquez pidió revertir un recorte de S/ 22 millones a la Universidad Agraria. Katherine Ampuero criticó recortes frente a El Niño. Francisco Calisto pidió autorizar S/ 482 millones de deuda para un submarino peruano.</td></tr>
<tr><td>Partido Cívico Obras</td><td>Daniel Barragán pidió atender demandas laborales de Reniec y Sunat y seguir el pase de CAS a 728 en el Ministerio Público. Francisco Gagó pidió agua y alcantarillado en Pedregal, Pueblo Nuevo y Chihuahua (Buenos Aires, Morropón, Piura).</td></tr>
</tbody></table></div>
<h2>Qué se pidió para Piura</h2>
<ul class="clean">
<li><strong>Carmela Paucará</strong> (diputada, Fuerza Popular): partidas para reactivar obras paralizadas en la sierra de Piura.</li>
<li><strong>Miguel Huamán</strong> (diputado, Partido del Buen Gobierno): terminar los puestos de salud de Ayabaca, Huancabamba, Huarmaca y Los Algarrobos, previstos tras el Niño Costero de 2017.</li>
<li><strong>Henry Albañil</strong> (diputado, Partido Cívico Obras): recursos para titular a 27 docentes de la Universidad Nacional de Piura (Ley 32618).</li>
<li><strong>Ernesto Zunini</strong> (diputado, Juntos por el Perú): nombramiento de docentes de la Universidad de Piura y renovar la autorización para financiar servicios en centros poblados.</li>
<li><strong>Francisco Gagó</strong> (Partido Cívico Obras): agua y alcantarillado en Pedregal, Pueblo Nuevo y Chihuahua, distrito de Buenos Aires (Morropón).</li>
</ul>
<h2>Cifras que se citaron y no coinciden</h2>
<p>Los legisladores citaron cifras distintas sobre los mismos sectores. Por ejemplo, para salud se mencionaron una reducción de S/ 608 millones, de 10%, de 3% y de 2% (S/ 679 millones), y para Defensa, aumentos de 21% y de 28.5%. Son afirmaciones de cada parlamentario y no se han verificado contra el texto del dictamen. Para comparar, usa el <a href="~/explica/presupuesto-publico-2027-que-es-como-se-aprueba-y-que-incluye.html">resumen del dictamen</a>.</p>
<h2>Cómo terminó la sesión</h2>
<p>Según el Congreso, el Pleno pasó a cuarto intermedio a pedido de la presidencia de la Comisión Bicameral de Presupuesto, para evaluar los pedidos de senadores y diputados. Se reanuda el viernes 20 de noviembre a las 4:00 p. m. para avanzar en un texto sustitutorio de los dictámenes. Según Andina, ese día habrá una intervención final de la Presidencia del Consejo de Ministros y la votación; la nota no precisa la hora. No hubo votación el 19 de noviembre.</p>
<h2>Y César Revilla</h2>
<p>César Revilla intervino por dos minutos: <a href="~/explica/cesar-revilla-pleno-19-noviembre-2026-propuestas-presupuesto-2027.html">estas fueron sus propuestas para el Presupuesto 2027</a>. La nota del Congreso sobre los diputados no lo menciona, pero el video oficial de la sesión sí lo registra. Su agenda del día está en <a href="~/explica/agenda-19-noviembre-2026-canal-n-liga-corea-pleno-presupuesto.html">Agenda del 19 de noviembre</a>. Puedes ver la sesión completa en <a href="~/en-vivo.html">En vivo</a>.</p>
<p class="upd">Resumen elaborado a partir de dos notas oficiales del Congreso y de Andina. Los nombres y pedidos son los que esas notas recogen; no es una transcripción. Para la sesión completa, usa el video del canal oficial del Congreso.</p>""",
         faq=[("¿De qué se habló en el Pleno del 19 de noviembre de 2026?",
               "Del Presupuesto 2027, la Ley de Equilibrio Financiero y la Ley de Endeudamiento. Senadores y diputados pidieron obras de agua, salud y educación, derechos laborales y más control del gasto."),
              ("¿Qué dijo Fuerza Popular en el debate del Presupuesto 2027?",
               "Según el Congreso, sus parlamentarios pidieron obras en sus regiones, como agua y desagüe en el sur, movilidad en el Callao y obras paralizadas en la sierra de Piura. Javier Castro habló de un ahorro de S/ 700 millones para obras."),
              ("¿Qué criticaron Juntos por el Perú, el Partido del Buen Gobierno y Renovación Popular?",
               "Cuestionaron recortes en salud, vivienda, saneamiento y educación, la distribución regional del gasto y algunos gastos puntuales. Cada parlamentario citó sus propias cifras."),
              ("¿Qué se pidió para Piura?",
               "Reactivar obras en la sierra, terminar puestos de salud en Ayabaca, Huancabamba, Huarmaca y Los Algarrobos, titular docentes de la Universidad Nacional de Piura y financiar agua y alcantarillado en Buenos Aires (Morropón)."),
              ("¿Se votó el Presupuesto 2027 el 19 de noviembre?",
               "No. La sesión pasó a cuarto intermedio y continúa el 20 de noviembre a las 4:00 p. m., según el Congreso."),
              ("¿Dónde puedo ver la sesión completa?",
               "En la página En vivo de este sitio, que incrusta la transmisión oficial del canal de YouTube del Congreso.")],
         keys=["congdip1119", "congsen1119", "congre1119", "andina1119"]),
    dict(slug="noveno-retiro-afp-2026-en-que-va-el-proyecto-de-4-uit", tema="economia-y-empleo", iso="2026-11-20",
         h1="Noveno retiro de AFP 2026: en qué va el proyecto de hasta 4 UIT (S/ 22,000)",
         seo="Noveno retiro AFP 2026: en qué va",
         desc="Estado del proyecto de nuevo retiro de AFP de hasta 4 UIT (S/ 22,000): quién lo presentó, en qué comisión está, qué falta y cuándo podría debatirse.",
         resumen="El proyecto de un noveno retiro de AFP de hasta S/ 22,000 está en la Comisión de Economía, sin dictamen y sin fecha de debate, según La República (10 de noviembre de 2026).",
         card="En qué comisión está, qué falta y quién lo propone.",
         html="""<h2>En qué va</h2>
<p>Según La República (10 de noviembre de 2026), el proyecto de ley 00469-2026-2031-CD, de la diputada Catherin Palomino (Juntos por el Perú), ingresó el 1 de octubre y pasó al día siguiente a la Comisión de Economía. Al 10 de noviembre no tenía dictamen ni fecha de debate.</p>
<h2>Qué propone</h2>
<ul class="clean">
<li><strong>Monto:</strong> hasta 4 UIT, equivalentes a S/ 22,000.</li>
<li><strong>Cuotas:</strong> cuatro desembolsos de hasta S/ 5,500, con 30 días calendario entre cada uno.</li>
<li><strong>Plazo para pedirlo:</strong> 90 días para presentar la solicitud.</li>
<li><strong>Desistimiento:</strong> se podría desistir una sola vez, avisando a la AFP con al menos 10 días de anticipación.</li>
</ul>
<h2>Qué falta para que se apruebe</h2>
<ol class="clean">
<li><strong>Opiniones de las entidades.</strong> El 13 de octubre la comisión pidió su opinión al MEF, la SBS, el BCRP, la SMV, el Ministerio de Justicia y Cenepred. El plazo inicial de 15 días venció el 9 de noviembre y la nota no informa que alguna entidad haya enviado su opinión.</li>
<li><strong>Sustentación y dictamen.</strong> La autora sustenta el proyecto en la comisión y esta vota un dictamen, que puede recomendar aprobar o archivar.</li>
<li><strong>Cámara de Diputados y Senado.</strong> Si lo aprueba Diputados, pasa a la Comisión de Economía del Senado y luego al Pleno del Senado.</li>
<li><strong>Poder Ejecutivo.</strong> El Gobierno puede promulgarlo u observarlo. Si lo observa, el Congreso puede aprobarlo por insistencia.</li>
</ol>
<h2>Qué han dicho el Gobierno y el BCRP</h2>
<p>Según La República, el ministro de Economía, Elmer Cuba, rechazó la propuesta en una entrevista. Según Infobae (28 de octubre), el BCRP ha dicho que no ve sentido en la medida.</p>
<h2>Cuidado con las noticias falsas</h2>
<p>Hasta la fecha de las fuentes citadas, ningún retiro nuevo está aprobado. Si ves anuncios con fechas para cobrar, verifica en el portal del Congreso y en la página de tu AFP antes de dar datos personales o pagar a terceros.</p>
<h2>Y César Revilla</h2>
<p>Las notas consultadas no mencionan a César Revilla en este trámite. En 2024, la Comisión de Economía que presidía aprobó el retiro de hasta 4 UIT que hoy es la Ley 32002: <a href="~/gestion/retiro-afp-2024-ley-32002.html">lee cómo fue</a>.</p>
<p class="upd">Estado según las fuentes del 28 de octubre y del 10 de noviembre de 2026. Puede haber cambiado; confirma en el <a href="https://www.congreso.gob.pe/" rel="noopener" target="_blank">portal del Congreso</a>.</p>""",
         faq=[("¿Hay un nuevo retiro de AFP aprobado en 2026?",
               "No. Según La República (10 de noviembre de 2026), el proyecto de hasta 4 UIT sigue en la Comisión de Economía, sin dictamen ni fecha de debate."),
              ("¿De cuánto sería el noveno retiro de AFP?",
               "Hasta 4 UIT (S/ 22,000), en cuatro desembolsos de hasta S/ 5,500 cada 30 días, según el proyecto."),
              ("¿Quién presentó el proyecto de nuevo retiro de AFP?",
               "La diputada Catherin Palomino, de Juntos por el Perú, el 1 de octubre de 2026 (proyecto 00469-2026-2031-CD)."),
              ("¿Qué falta para que se apruebe un nuevo retiro de AFP?",
               "Las opiniones de las entidades consultadas, un dictamen favorable de la Comisión de Economía, la aprobación de Diputados y del Senado y la promulgación del Ejecutivo.")],
         keys=["larep1110", "infobae1028"]),
]

# Explicaciones de hechos del día (nivel 1 y 2 del protocolo): se agregan a EXPLICA con su `iso` real.
# COYUNTURA queda reservada para un futuro índice cronológico (no se genera mientras esté vacía).
COYUNTURA = []
