import json
import asyncio
import ollama
from config import settings

_client = ollama.Client(host=settings.OLLAMA_BASE_URL)
LLM_OPTIONS = {"think": False}

SYSTEM_PROMPT_DIAGNOSTICO = """Eres un experto en electrónica y mantenimiento de circuitos. 
Analiza los datos del circuito y genera recomendaciones de mantenimiento preventivo en español.
Responde SIEMPRE en JSON con este formato exacto:
{
  "estado_general": "normal|advertencia|critico",
  "componentes_en_riesgo": ["etiqueta1", "etiqueta2"],
  "recomendaciones": ["recomendación 1", "recomendación 2"]
}"""

SYSTEM_PROMPT_CHAT = """Eres un asistente técnico experto en electrónica y mantenimiento de circuitos.
Tienes acceso al historial de lecturas y diagnósticos del dispositivo del usuario.
Responde en español de forma clara y concisa."""


async def generar_recomendaciones(contexto: dict) -> dict:
    prompt = f"""Circuito analizado:
- Componentes detectados: {contexto.get('componentes', [])}
- Voltaje: {contexto.get('voltaje')}V
- Corriente: {contexto.get('corriente')}A  
- Temperatura: {contexto.get('temperatura')}°C
- Alertas activas: {contexto.get('alertas', [])}
- Perfil de voltaje: {contexto.get('perfil_voltaje', '5V')}

Genera el análisis y recomendaciones."""

    def _llamar():
        return _client.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_DIAGNOSTICO},
                {"role": "user", "content": prompt}
            ],
            options=LLM_OPTIONS
        )

    try:
        response = await asyncio.to_thread(_llamar)
        return json.loads(response["message"]["content"])
    except Exception:
        return {"estado_general": "normal", "componentes_en_riesgo": [], "recomendaciones": []}


async def chat_stream(historial: list, pregunta: str, contexto: dict):
    messages = [{"role": "system", "content": SYSTEM_PROMPT_CHAT}]

    if contexto:
        ctx_text = f"""Contexto del dispositivo:
- Últimas lecturas: V={contexto.get('voltaje')}V, I={contexto.get('corriente')}A, T={contexto.get('temperatura')}°C
- Alertas recientes: {contexto.get('alertas', [])}
- Componentes detectados: {contexto.get('componentes', [])}"""
        messages.append({"role": "system", "content": ctx_text})

    messages.extend(historial)
    messages.append({"role": "user", "content": pregunta})

    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    def _stream_worker():
        try:
            for chunk in _client.chat(
                model=settings.OLLAMA_MODEL,
                messages=messages,
                stream=True,
                options=LLM_OPTIONS
            ):
                texto = chunk["message"]["content"]
                loop.call_soon_threadsafe(queue.put_nowait, texto)
        except Exception:
            pass
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    loop.run_in_executor(None, _stream_worker)

    while True:
        chunk = await queue.get()
        if chunk is None:
            break
        yield chunk
