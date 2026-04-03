# Backend — Python + FastAPI

---

## Responsabilidades

- Autenticación y gestión de usuarios (JWT)
- Recepción y almacenamiento de lecturas del ESP32
- Procesamiento de diagnósticos (foto + componentes + lecturas)
- Integración con Ollama/LLM para recomendaciones y chat
- Generación de alertas preventivas
- Jobs programados para agregación de lecturas
- API REST consumida por la app Flutter

---

## Estructura de carpetas

```
backend/
├── main.py                  # Entrada de la app FastAPI
├── config.py                # Variables de entorno (.env)
├── database.py              # Conexión a PostgreSQL (SQLAlchemy)
├── models/                  # Modelos ORM (tablas de la DB)
│   ├── user.py
│   ├── dispositivo.py
│   ├── diagnostico.py
│   ├── componente.py
│   ├── lectura.py
│   ├── alerta.py
│   ├── recomendacion.py
│   ├── chat.py
│   ├── perfil_voltaje.py
│   └── sesion.py
├── routers/                 # Endpoints agrupados por dominio
│   ├── auth.py              # Login, registro, refresh token
│   ├── dispositivos.py      # CRUD de dispositivos ESP32
│   ├── diagnosticos.py      # Crear y consultar diagnósticos
│   ├── lecturas.py          # Recibir y consultar lecturas
│   ├── alertas.py           # Consultar y marcar alertas
│   ├── chat.py              # Chat con LLM (streaming)
│   └── estadisticas.py      # Consultas de agregados
├── services/                # Lógica de negocio
│   ├── llm_service.py       # Integración con Ollama
│   ├── alerta_service.py    # Detección de anomalías
│   ├── contexto_service.py  # Construcción de contexto para el LLM
│   └── agregacion_service.py # Jobs de agregación de lecturas
├── schemas/                 # Pydantic schemas (validación de datos)
│   ├── auth.py
│   ├── dispositivo.py
│   ├── diagnostico.py
│   ├── lectura.py
│   ├── chat.py
│   └── estadisticas.py
├── jobs/                    # APScheduler jobs
│   └── agregacion.py        # Job de agregación hora/día/mes/año
└── requirements.txt
```

---

## Endpoints

### Auth — `/auth`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/auth/registro` | Crear cuenta nueva |
| POST | `/auth/login` | Login, retorna access + refresh token |
| POST | `/auth/refresh` | Renovar access token con refresh token |
| POST | `/auth/logout` | Revocar refresh token |

---

### Dispositivos — `/dispositivos`

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/dispositivos` | Listar dispositivos del usuario |
| POST | `/dispositivos` | Vincular nuevo dispositivo ESP32 |
| PUT | `/dispositivos/{id}` | Renombrar dispositivo |
| DELETE | `/dispositivos/{id}` | Desvincular dispositivo |

---

### Diagnósticos — `/diagnosticos`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/diagnosticos` | Crear diagnóstico (foto + componentes + lecturas) |
| GET | `/diagnosticos` | Historial de diagnósticos del usuario |
| GET | `/diagnosticos/{id}` | Detalle de un diagnóstico |

**Flujo interno de `POST /diagnosticos`:**
```
1. Recibe: lista de componentes validada + lecturas ESP32 + foto_url + dispositivo_id
2. Guarda diagnóstico en DB
3. Evalúa lecturas contra umbrales del perfil → genera alertas si aplica
4. Construye contexto para el LLM (componentes + lecturas + historial reciente)
5. Llama a Ollama → obtiene recomendaciones
6. Guarda recomendaciones en DB
7. Retorna diagnóstico completo con recomendaciones
```

---

### Lecturas — `/lecturas`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/lecturas` | Recibir lectura del ESP32 (llamada frecuente) |
| GET | `/lecturas/{dispositivo_id}` | Lecturas crudas recientes (últimas horas) |
| GET | `/lecturas/{dispositivo_id}/hora` | Agregados por hora |
| GET | `/lecturas/{dispositivo_id}/dia` | Agregados por día |
| GET | `/lecturas/{dispositivo_id}/mes` | Agregados por mes |
| GET | `/lecturas/{dispositivo_id}/anio` | Agregados por año |

---

### Alertas — `/alertas`

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/alertas` | Alertas del usuario (con filtro de no vistas) |
| PUT | `/alertas/{id}/vista` | Marcar alerta como vista |

---

### Chat — `/chat`

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/chat/{dispositivo_id}` | Enviar mensaje, respuesta en streaming |
| GET | `/chat/{dispositivo_id}/historial` | Historial de conversación |
| DELETE | `/chat/{dispositivo_id}/historial` | Limpiar historial |

**Flujo interno de `POST /chat/{dispositivo_id}`:**
```
1. Recibe: mensaje del usuario
2. Recupera historial reciente del chat (últimos N mensajes)
3. Construye contexto:
   - Últimas lecturas del dispositivo
   - Alertas recientes
   - Componentes del último diagnóstico
   - Perfil de voltaje configurado
4. Construye prompt: sistema + contexto + historial + pregunta
5. Llama a Ollama con StreamingResponse
6. Guarda mensaje usuario + respuesta en DB
7. Retorna stream de texto a la app
```

---

### Estadísticas — `/estadisticas`

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/estadisticas/{dispositivo_id}` | Resumen estadístico (avg, min, max por variable) |

---

### Perfiles de voltaje — `/perfiles`

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/perfiles` | Listar perfiles custom del usuario |
| POST | `/perfiles` | Crear perfil custom |
| PUT | `/perfiles/{id}` | Editar perfil |
| DELETE | `/perfiles/{id}` | Eliminar perfil |

---

## Integración con Ollama (LLM)

```python
# services/llm_service.py — esquema básico

async def generar_recomendaciones(contexto: dict) -> dict:
    prompt = construir_prompt_diagnostico(contexto)
    response = await ollama.chat(model="llama3.2", messages=[
        {"role": "system", "content": SYSTEM_PROMPT_DIAGNOSTICO},
        {"role": "user", "content": prompt}
    ])
    return parsear_respuesta_json(response)

async def chat_stream(historial: list, pregunta: str, contexto: dict):
    messages = construir_messages_chat(historial, pregunta, contexto)
    async for chunk in ollama.chat(model="llama3.2", messages=messages, stream=True):
        yield chunk["message"]["content"]
```

---

## Jobs de agregación (APScheduler)

```
Cada hora  → Agrupa lecturas de la última hora → inserta en lecturas_hora
Cada día   → Agrupa lecturas_hora del día      → inserta en lecturas_dia
Cada mes   → Agrupa lecturas_dia del mes       → inserta en lecturas_mes
Cada año   → Agrupa lecturas_mes del año       → inserta en lecturas_anio
Cada día   → Elimina lecturas crudas > 7 días
```

---

## Variables de entorno (.env)

```env
# Base de datos
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT
JWT_SECRET_KEY=tu_clave_secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Almacenamiento de fotos
FOTO_STORAGE=local          # "local" o "s3"
FOTO_LOCAL_PATH=./uploads
# S3_BUCKET=nombre-bucket   # Solo en producción
```

> Cambiar `OLLAMA_BASE_URL` y `DATABASE_URL` es todo lo que se necesita para migrar de laptop a AWS.

---

## Dependencias principales (requirements.txt)

```
fastapi
uvicorn
sqlalchemy
asyncpg
pydantic
python-jose[cryptography]
passlib[bcrypt]
ollama
apscheduler
python-multipart
python-dotenv
```

---

## Pendientes

- [ ] Definir SYSTEM_PROMPT base para diagnósticos y chat
- [ ] Definir umbrales de alerta por perfil de voltaje
- [ ] Definir cuántos mensajes de historial se incluyen en el contexto del chat
- [ ] Esquema de subida de fotos (local para MVP, S3 para producción)
