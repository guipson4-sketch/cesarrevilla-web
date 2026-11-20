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
    "conglc1119": ("Congreso de la República (19 de noviembre de 2026): Liga Parlamentaria de Amistad Perú-Corea del Sur cuenta con nuevo Comité Ejecutivo",
                   "https://comunicaciones.congreso.gob.pe/noticias/liga-parlamentaria-de-amistad-peru-corea-del-sur-cuenta-con-nuevo-comite-ejecutivo/"),
    "congre1119": ("Congreso de la República (19 de noviembre de 2026): Reinició debate parlamentario sobre dictamen de presupuesto del sector público 2027",
                   "https://comunicaciones.congreso.gob.pe/noticias/reinicio-debate-parlamentario-sobre-dictamen-de-presupuesto-del-sector-publico-2027/"),
    "congdip1119": ("Congreso de la República (19 de noviembre de 2026): Diputados fijan posición y transmiten necesidades de pobladores en debate de presupuesto público",
                    "https://comunicaciones.congreso.gob.pe/noticias/diputados-fijan-posicion-y-transmiten-necesidades-de-pobladores-en-debate-de-presupuesto-publico"),
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
<p class="upd">Las notas del Congreso consultadas no mencionan intervenciones de César Revilla. Esta página se actualizará cuando se publique el video o el acta de su participación.</p>
<h2>Para entender el tema</h2>
<p>Lee <a href="~/explica/presupuesto-publico-2027-que-es-como-se-aprueba-y-que-incluye.html">qué incluye el Presupuesto 2027 y cómo se vota</a> y <a href="~/guias/como-se-crea-una-ley-en-el-peru.html">cómo se crea una ley en el Perú</a>.</p>""",
         faq=[("¿Qué actividades tuvo César Revilla el 19 de noviembre de 2026?",
               "Según la agenda de su despacho, una entrevista en Canal N a las 8:00 a. m., la elección e instalación del Comité Ejecutivo de la Liga Parlamentaria de Amistad Perú–Corea del Sur a las 9:00 a. m. y el Pleno Bicameral sobre el Presupuesto 2027 a las 10:00 a. m."),
              ("¿Quién preside la Liga Parlamentaria de Amistad Perú–Corea del Sur?",
               "María Candelaria Ramos Rosales (Fuerza Popular), elegida por unanimidad el 19 de noviembre de 2026, según el Congreso."),
              ("¿Se votó el Presupuesto 2027 el 19 de noviembre?",
               "No. El Pleno debatió los dictámenes y pasó a cuarto intermedio. Según el Congreso, la sesión continúa el viernes 20 de noviembre a las 4:00 p. m.")],
         keys=["conglc1119", "congre1119", "congdip1119"]),
]

# Explicaciones de hechos del día (nivel 1 y 2 del protocolo): se agregan a EXPLICA con su `iso` real.
# COYUNTURA queda reservada para un futuro índice cronológico (no se genera mientras esté vacía).
COYUNTURA = []
