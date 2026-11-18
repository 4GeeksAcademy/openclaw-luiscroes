# SKILL_LOG — Mi Asistente 4Geeks

Registro de cómo enseñé a mi agente OpenClaw (**Kai** 🤖) a seguir mi progreso en el curso de 4Geeks Academy. Todas las skills se construyeron **conversando con Kai por Telegram**, una a la vez: yo describía la pregunta que quería poder hacerle en lenguaje natural, Kai revisaba la API con una llamada real, proponía un diseño, yo lo ajustaba y él creaba y probaba la skill.

- **Agente:** Kai (OpenClaw 2026.10.10, VPS Ubuntu 22.04), canal Telegram.
- **API:** BreatheCode — `https://breathecode.herokuapp.com`, cabecera `Authorization: Token <valor>`.
- **Referencia usada:** [STUDENT_API_CALLS_REFERENCE.es.md](https://github.com/4GeeksAcademy/ai-engineering-syllabus/blob/main/content/projects/openclaw-integration/STUDENT_API_CALLS_REFERENCE.es.md)
- **Fecha:** 18/11/2026.

> En los resultados de prueba se omiten email, IDs y URLs privadas. Las respuestas de Kai se copian tal cual las envió por Telegram.

---

## 0. Configuración inicial y seguridad del token

| Paso | Cómo se hizo |
|---|---|
| Instancia activa | Kai responde por Telegram; gateway `openclaw-gateway` activo en el VPS. |
| Obtener el token | learn.4geeks.com → DevTools → **Application** → **Cookies** → `https://learn.4geeks.com` → filtro `4g_tok` → copiar el valor. |
| Guardarlo | En el VPS, con un prompt oculto (`read -s`), en `~/.openclaw/.env` como `TOKEN_4GEEKS=...`, permisos `600`. El valor nunca se escribió en pantalla, en un chat ni en un archivo del repositorio. |
| Validarlo | Una llamada a `GET /v1/admissions/user/me` devolvió **200** (longitud del token: 40). |
| Cómo lo usan las skills | Cada script auxiliar lee `TOKEN_4GEEKS` del entorno del proceso y, si no existe, lee **solo esa variable** de `~/.openclaw/.env`. Nunca lo imprime, registra ni guarda. |
| Fuera del repo | `~/.openclaw/.env` está fuera del workspace y además `.env` / `.env.*` están en `.gitignore`. |

**Auditoría final** (sin mostrar el token, comparándolo contra los archivos):

```text
Files clean        → el token no aparece en ningún archivo del workspace
History clean      → el token no aparece en el historial de git
CFG=0              → el token no aparece en openclaw.json
```

### Correcciones a la documentación del curso que descubrimos

- La cabecera es `Authorization: Token …` (no `Bearer`).
- `GET /v1/admissions/user/me` **no** trae `profile_academy`; la academia y las cohortes vienen en la lista `cohorts`.
- `GET /v1/admissions/academy/cohort/me` y `GET /v1/activity/me` devuelven **403** con un token de estudiante.
- Los nombres de variables de entorno no pueden empezar por un dígito (`4GEEKS_…` no es válido) ni llevar espacios.

---

## 1. Conversación de descubrimiento

**Mi prompt:**

> Hola Kai. Quiero darte la habilidad de conectarte a mi cuenta de 4Geeks usando mi token de estudiante, sin que tenga que desarrollar código de mi parte. ¿Qué debemos hacer?
>
> Contexto: el token ya está guardado de forma segura en el servidor, en ~/.openclaw/.env como TOKEN_4GEEKS (no lo leas en voz alta ni lo muestres nunca). La referencia de la API de estudiantes está aquí: https://raw.githubusercontent.com/4GeeksAcademy/ai-engineering-syllabus/main/content/projects/openclaw-integration/STUDENT_API_CALLS_REFERENCE.es.md

**Respuesta de Kai:**

> Hola, Luis. Revisé la referencia: la API usa una cabecera Authorization: Token … y ofrece consultas para tu perfil, cohortes y tareas. No he leído ni usado el token.
>
> Para darte esta habilidad sin que programes, recomiendo crear una skill de solo lectura para consultar primero tu perfil, cohorte activa y tareas. Dejaría fuera acciones que modifican o entregan tareas hasta que las autorices expresamente. Antes de conectarla, necesito añadir 4Geeks como servicio permitido en TOOLS.md; ahora mismo ese archivo no lo contempla.
>
> ¿Me autorizas a añadir esa API a TOOLS.md y crear la skill de consulta, usando el token desde el entorno sin mostrarlo ni registrarlo?

**Resumen:**

- **Qué sugirió Kai:** leyó la referencia por su cuenta, identificó el formato de autenticación, propuso empezar **solo con lectura** y dejar fuera los endpoints que modifican o entregan tareas (`PUT`, `POST …/deliver`).
- **Qué me pidió:** autorización para registrar la API de 4Geeks como servicio permitido en `TOOLS.md` y para usar el token desde el entorno.
- **Qué decidí yo:** autoricé `TOOLS.md` en modo solo lectura, pero le pedí **una skill por cada acción de la API** en lugar de una skill grande, para cumplir la regla de una única responsabilidad. Cada nueva pregunta que quería hacerle definió la siguiente skill.

---

## 2. Skills principales

### Skill 1 — `authenticate-4geeks`

**Prompt inicial:**

> Skill 1 — authenticate-4geeks: quiero que puedas verificar que mi token es válido y que la sesión está activa. Debe llamar solo a GET /v1/admissions/user/me con la cabecera Authorization: Token y el valor de TOKEN_4GEEKS (desde el entorno; si no está en el entorno, cárgalo de ~/.openclaw/.env sin imprimirlo). Si responde 200, dime "sesión activa" con mi nombre de usuario; si responde 401/403, dime que el token caducó y que hay que renovarlo. Nunca muestres el token, mi email ni IDs. Guárdala en skills/authenticate-4geeks/SKILL.md. ¿Qué me propones antes de crearla?

**Lo que Kai propuso:**

> - Añadir a TOOLS.md únicamente el acceso de solo lectura a https://breathecode.herokuapp.com.
> - Crear skills/authenticate-4geeks/SKILL.md con un auxiliar que haga exclusivamente GET /v1/admissions/user/me. Tomará TOKEN_4GEEKS del entorno o, si falta, leerá esa variable de ~/.openclaw/.env sin mostrarla, registrar la cabecera ni imprimir la respuesta completa.
> - En caso de 200, confirmar la sesión y mostrar solo el nombre de usuario si la respuesta lo incluye. La referencia no garantiza que exista ese campo; sí menciona el nombre. Recomiendo usarlo como alternativa.
> - Para 401/403, decir que el token fue rechazado y puede haber caducado, no asegurar que caducó: esos códigos no permiten distinguir la causa. Otros errores se informarían como fallo de conexión o del servicio, no como problema del token.

**Ajuste mío:** acepté sus dos mejoras (usar el nombre como alternativa y decir «rechazado, puede haber caducado» en vez de «caducado»).

| | |
|---|---|
| **Qué hace** | Comprueba que el token es válido y que la sesión está activa. |
| **Endpoint** | `GET /v1/admissions/user/me` |
| **Archivos** | `skills/authenticate-4geeks/SKILL.md`, `skills/authenticate-4geeks/scripts/check_session.py` |
| **Salida** | `sesión activa` + nombre; `token rechazado; puede haber caducado…` en 401/403; diagnóstico genérico en otros errores. |

**Prueba** — _«pruébala una vez»_:

> Sesión activa — Luis Carlos

✅ Coincide con mi cuenta.

---

### Skill 2 — `get-my-projects`

**Prompt inicial:**

> Siguiente pregunta que quiero poder hacerte: "¿Cuáles son mis proyectos y en qué estado están?"
>
> Skill 2 — get-my-projects: solo GET /v1/assignment/user/me/task con task_type=PROJECT (y un limit alto para no perder páginas). Quiero la lista de proyectos con su estado en tres categorías: pendiente, entregado o calificado. Antes de crearla, revisa con una llamada real qué campos de estado devuelve la API y propónme cómo mapearlos a esas tres categorías. Muestra solo título y estado (sin IDs ni URLs privadas) y no guardes respuestas en disco. Debe usar el mismo método seguro de token que authenticate-4geeks. ¿Qué me propones?

**Lo que Kai propuso** (tras una llamada real: 200, 21 proyectos):

> Los estados observados fueron task_status=PENDING o DONE, y revision_status=PENDING o APPROVED. No guardé la respuesta en disco.
>
> - task_status=PENDING → **pendiente**.
> - task_status=DONE sin revisión aprobada → **entregado**.
> - revision_status=APPROVED (o task_status=APPROVED, si aparece) → **calificado**.
> - REJECTED → **calificado** — ya fue revisado; lo indicaré como tal dentro de esa categoría.
>
> Para no omitir resultados, usaría paginación con limit alto y offset, siguiendo páginas hasta que no haya más. […] si un estado no reconocido aparece, lo marcaría como desconocido en vez de adivinar.

**Ajuste mío:** agrupar por categoría con el total de cada una y marcar los rechazados con «(rechazado)».

| | |
|---|---|
| **Qué hace** | Lista mis proyectos con su estado: pendiente / entregado / calificado. |
| **Endpoint** | `GET /v1/assignment/user/me/task?task_type=PROJECT` (paginado con `limit` / `offset`) |
| **Archivos** | `skills/get-my-projects/SKILL.md` + script auxiliar |

**Prueba** — _«¿Cuáles son mis proyectos y en qué estado están?»_:

> **Pendiente (1)**
> - My 4Geeks Assistant — Teaching OpenClaw to Track Your Progress
>
> **Entregado (2)**
> - Build a Digital Postcard with HTML/CSS
> - My Agent, My Way: Teaching Your Personal Assistant New Skills
>
> **Calificado (18)**
> - Is This Snack Healthy? — A Nutrition-Check Automation
> - Milestone 0 — Choose Your Company
> - Command Line Challenge
> - My first collaborative professional project
> - Milestone 0 — Choose Your Company
> - Milestone 1 — Your Company's Public Website
> - Building context from an existing project - Financial dashboard
> - Applying Spec Driven Development - Financial dashboard
> - Enhacing development with agent skills - Financial dashboard
> - Milestone — AI-driven Engineering
> - Data modeling and class diagrams
> - Cinema Seat Manager in TypeScript
> - Showcase your friend's artist talent with a website
> - Connect Your Agent: Telegram, Google Drive & Calendar
> - Setting Up Your Personal AI Agent with OpenClaw
> - A simple Dashboard with Tailwind CSS
> - Milestone 2 — Building Scripts to Automate Tasks
> - Music playlist player modeling and class diagrams
>
> No aparecieron proyectos rechazados en esta consulta.

✅ Coincide con lo que muestra la plataforma (21 proyectos, 18 aprobados).

---

### Skill 3 — `get-pending-work`

**Prompt inicial:**

> Siguiente pregunta: "¿Qué me falta por entregar?"
>
> Skill 3 — get-pending-work: a diferencia de get-my-projects, esta debe cubrir todos los tipos de tarea (proyectos, ejercicios, lecciones, quizzes), pero solo lo que aún no he completado. Usa el mismo endpoint GET /v1/assignment/user/me/task filtrado por task_status=PENDING. Agrupa por tipo y ordena los proyectos primero, porque son los que cuentan para la evaluación. Mismas reglas: sin IDs, sin guardar en disco, token seguro. ¿Qué me propones? ¿Deberíamos incluir también los proyectos rechazados que hay que corregir?

**Lo que Kai propuso:**

> Sí, incluiría los proyectos rechazados: requieren corrección y no deberían desaparecer de tu lista de pendientes. Pero el filtro task_status=PENDING probablemente los excluye si su tarea figura como DONE y su revision_status es REJECTED.
>
> Propongo que la skill haga dos consultas de solo lectura al mismo endpoint: una con task_status=PENDING para todo el trabajo pendiente y otra con task_status=DONE para detectar revisiones rechazadas. De esa segunda respuesta incluiría únicamente las rechazadas, marcadas «rechazado; requiere corrección». Agruparía por tipo, con proyectos primero, y no mostraría tareas ya entregadas o aprobadas.

**Ajuste mío:** acepté las dos consultas (mismo endpoint, una sola responsabilidad: _lo que me falta_) y pedí el total al principio.

| | |
|---|---|
| **Qué hace** | Dice exactamente qué me falta completar, de todos los tipos, con los proyectos primero. Incluye proyectos rechazados que hay que corregir. |
| **Endpoint** | `GET /v1/assignment/user/me/task?task_status=PENDING` y `?task_status=DONE` (solo para detectar `revision_status=REJECTED`) |
| **Archivos** | `skills/get-pending-work/SKILL.md` + script auxiliar |

**Prueba** — _«¿Qué me falta por entregar?»_:

> Te faltan **6 tareas**:
>
> **Proyectos (1)**
> - My 4Geeks Assistant — Teaching OpenClaw to Track Your Progress — pendiente
>
> **Ejercicios (5)**
> - Master Javascript Practicing — pendiente
> - n8n Glossary — pendiente
> - Visual Workflow Mapping for Beginners with Excalidraw — pendiente
> - Introduction to Coding Agents Work Modes — pendiente
> - Understanding How the Internet Works — pendiente
>
> No aparecieron proyectos rechazados en la consulta. La skill quedó creada y validada.

✅ Correcto: el único proyecto pendiente es justamente este.

---

### Skill 4 — `get-progress-summary`

**Prompt inicial:**

> Siguiente pregunta: "¿Qué tan avanzado estoy en el curso?"
>
> Skill 4 — get-progress-summary: quiero una visión general, no una lista. Con GET /v1/assignment/user/me/task (todas las tareas, paginando), cuenta por tipo (proyectos, ejercicios, lecciones, quizzes) cuántas están completadas sobre el total, el porcentaje global y cuántos proyectos están aprobados. La referencia también menciona /v1/activity/me; ¿vale la pena usarlo o mejor quedarnos solo con las tareas? Mismas reglas de seguridad. ¿Qué me propones?

**Lo que Kai propuso:**

> Recomiendo basar el resumen solo en /v1/assignment/user/me/task, paginando hasta traer todas las tareas. Ese endpoint da el total y los estados necesarios para medir avance; /v1/activity/me refleja actividad o tiempo, no si las tareas están completadas, así que mezclarlo podría confundir la métrica.
>
> Para el cálculo, propongo contar como completadas las tareas DONE o APPROVED, pero no las REJECTED —requieren correcciones—; contar aparte los proyectos aprobados por revision_status=APPROVED. Incluiría los quizzes si aparecen en los resultados y no asumiría tipos que la API no devuelva.

**Ajuste mío:** de acuerdo; además confirmé que `/v1/activity/me` devuelve 403 con mi token, así que quedarnos con las tareas era lo correcto.

| | |
|---|---|
| **Qué hace** | Resumen de avance: completadas / total por tipo, porcentaje global y proyectos aprobados. |
| **Endpoint** | `GET /v1/assignment/user/me/task` (todas, paginado) |
| **Archivos** | `skills/get-progress-summary/SKILL.md` + script auxiliar |

**Prueba** — _«¿Qué tan avanzado estoy en el curso?»_:

> Vas por el **95,3 %: 121 de 127 tareas completadas**.
>
> - Proyectos: 20/21; **18 aprobados**
> - Ejercicios: 88/93
> - Lecciones: 13/13
> - Quizzes: 0/0; no aparecieron en los resultados
>
> Creé y validé get-progress-summary. La consulta paginó las tareas y el resumen se calculó sin guardar respuestas en disco.

✅ Cuadra con las skills 2 y 3 (127 − 6 pendientes = 121).

---

## 3. Skills extendidas (necesidades propias)

### Skill 5 — `get-project-feedback`

**Necesidad:** cuando me califican un proyecto quiero saber el resultado sin entrar en la plataforma.

**Prompt inicial:**

> Ahora dos que necesito yo. La primera: cuando me califican un proyecto, quiero leer el feedback del profesor sin entrar en la plataforma. Por ejemplo: "¿Qué feedback me dieron en Cinema Seat Manager?"
>
> Skill 5 — get-project-feedback: la referencia tiene GET /v1/assignment/task/{task_id} con el detalle (descripción, nota, feedback). Yo conozco mis proyectos por el nombre, no por el ID. ¿Cómo lo resolverías sin que la skill haga más de una cosa? Comprueba con una llamada real qué campos de feedback trae el detalle. Mismas reglas: sin mostrar IDs ni guardar en disco.

**Lo que Kai propuso:**

> Lo resolvería dentro de una única skill: buscar el proyecto por nombre en tus tareas, obtener su ID solo para hacer la consulta de detalle y usar ese ID internamente. La skill seguiría teniendo una sola responsabilidad —buscar feedback de un proyecto por nombre— aunque necesite dos consultas. Si no hay una coincidencia única, te pediría que aclares el título; no mostraría ni guardaría el ID.
>
> Probé el detalle de Cinema Seat Manager in TypeScript: respondió 200, pero no trae campos de feedback ni nota. Sí devuelve estado de revisión y fechas, además de la descripción. Así que la skill no debería inventar feedback; si el detalle no incluye comentarios o nota, te diría claramente que la API no los proporciona para ese proyecto.

**Ajuste mío:** que la respuesta sea el _estado de revisión_ (resultado, fecha de entrega, fecha de revisión) y que el feedback o la nota solo aparezcan si la API los trae; si no, que lo diga.

| | |
|---|---|
| **Qué hace** | Dado el nombre de un proyecto, devuelve el resultado de su revisión, fechas de entrega y revisión, y el feedback/nota si existen. |
| **Endpoint** | `GET /v1/assignment/task/{task_id}` (el ID se resuelve internamente con `GET /v1/assignment/user/me/task?task_type=PROJECT` y no se muestra) |
| **Archivos** | `skills/get-project-feedback/SKILL.md` + script auxiliar |

**Prueba** — _«¿Qué feedback me dieron en Cinema Seat Manager?»_:

> Para **Cinema Seat Manager in TypeScript**:
>
> - Estado de revisión: **aprobado**
> - Entrega: **05/11/2026, 18:46** (Madrid)
> - Revisión: **09/11/2026, 20:39** (Madrid)
> - La API no proporciona feedback ni nota para este proyecto.

✅ Correcto, y no inventa un feedback que no existe.

---

### Skill 6 — `get-my-cohort`

**Necesidad:** saber en qué programa estoy inscrito y cuánto falta para terminarlo.

**Prompt inicial:**

> La última: quiero saber en qué cohortes/módulos estoy inscrito ahora mismo. Por ejemplo: "¿En qué cohorte estoy y cuándo termina?"
>
> Skill 6 — get-my-cohort: la referencia sugiere GET /v1/admissions/academy/cohort/me, pero con mi token devuelve 403. ¿Puedes comprobar si GET /v1/admissions/user/me trae la lista de cohortes con su educational_status, y proponerme cómo mostrar solo las ACTIVE (nombre, fechas de inicio y fin, etapa)? Sin IDs ni email, sin guardar en disco.

**Lo que Kai encontró y propuso:**

> Sí: GET /v1/admissions/user/me respondió 200 e incluye una lista cohorts con educational_status, nombre, fechas (kickoff_date, ending_date) y etapa (stage). No hace falta usar la ruta que te devuelve 403.
>
> Encontré 23 inscripciones ACTIVE. Sin embargo, muchas son módulos con ending_date vacío y etapa INACTIVE; la inscripción del programa spain-aie-pt-6 muestra inicio 05/10/2026, fin 16/04/2027 y etapa STARTED. La respuesta también marca algunos módulos ACTIVE aunque su etapa diga INACTIVE, así que conviene mostrar ambas cosas sin confundir etapa con estado de inscripción.

**Ajuste mío:** mostrar primero el programa principal (etapa `STARTED`: nombre, inicio, fin y días que faltan) y debajo solo el número de módulos activos, nombrando únicamente los que están en `STARTED`.

| | |
|---|---|
| **Qué hace** | Dice en qué cohorte estoy, cuándo empezó, cuándo termina y cuántos días faltan. |
| **Endpoint** | `GET /v1/admissions/user/me` → lista `cohorts`, filtrada por `educational_status=ACTIVE` |
| **Archivos** | `skills/get-my-cohort/SKILL.md` + script auxiliar |

**Prueba** — _«¿En qué cohorte estoy y cuándo termina?»_:

> **Cohorte principal:** spain-aie-pt-6
>
> - Inicio: 05/10/2026
> - Fin: 16/04/2027 (**faltan 149 días**)
> - Módulos con inscripción activa: 23; con etapa STARTED: spain-aie-pt-6

✅ Correcto (del 18/11/2026 al 16/04/2027 hay 149 días).

---

## 4. Resumen

| # | Skill | Pregunta que responde | Endpoint | Prueba |
|---|---|---|---|---|
| 1 | `authenticate-4geeks` | ¿Mi token es válido? | `GET /v1/admissions/user/me` | ✅ |
| 2 | `get-my-projects` | ¿Cuáles son mis proyectos y en qué estado están? | `GET /v1/assignment/user/me/task?task_type=PROJECT` | ✅ |
| 3 | `get-pending-work` | ¿Qué me falta por entregar? | `GET /v1/assignment/user/me/task?task_status=PENDING` | ✅ |
| 4 | `get-progress-summary` | ¿Qué tan avanzado estoy? | `GET /v1/assignment/user/me/task` | ✅ |
| 5 | `get-project-feedback` | ¿Qué feedback me dieron en X? | `GET /v1/assignment/task/{task_id}` | ✅ |
| 6 | `get-my-cohort` | ¿En qué cohorte estoy y cuándo termina? | `GET /v1/admissions/user/me` (`cohorts`) | ✅ |

**Reglas comunes a todas las skills**

- Solo lectura: ninguna usa `PUT` ni `POST …/deliver`.
- Una responsabilidad por skill; cada una documenta su endpoint en `TOOLS.md`.
- El token se lee de `TOKEN_4GEEKS` (entorno o `~/.openclaw/.env`) y nunca se muestra, registra ni guarda.
- No muestran email, IDs ni URLs privadas.
- No guardan respuestas de la API en disco; todo se procesa en memoria. Si en el futuro se cachea algo, irá a `data/`, que está en `.gitignore`.

## 5. Lo que aprendí

- **Conversar antes de construir funciona.** En cada skill Kai hizo una llamada real antes de proponer, y eso destapó cosas que la documentación no decía: los proyectos rechazados no salen con `task_status=PENDING`, el detalle de tarea no trae feedback, y la ruta de cohortes da 403.
- **Kai mejoró mis prompts.** Cambió «el token caducó» por «el token fue rechazado; puede haber caducado» (un 401 no prueba que esté caducado) y se negó a inventar feedback que la API no devuelve.
- **Una skill = una pregunta.** Al dividir por pregunta del usuario, cada skill es pequeña, fácil de probar y fácil de explicar.
- **El secreto vive fuera del repositorio**, y lo comprobé con una auditoría que compara el valor real contra archivos, historial y configuración sin imprimirlo.
