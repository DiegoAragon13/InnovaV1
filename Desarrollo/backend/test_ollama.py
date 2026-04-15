"""
Test interactivo de Ollama con contexto del dispositivo.
Uso: python test_ollama.py

Simula el flujo real del chat del backend:
- Construye contexto con lecturas y alertas
- Permite chatear con el LLM en la terminal
"""

import ollama
import json
from config import settings

SYSTEM_PROMPT = """Eres un asistente técnico experto en electrónica y mantenimiento de circuitos.
Tienes acceso al historial de lecturas y diagnósticos del dispositivo del usuario.
Responde en español de forma clara y concisa."""

def construir_contexto(voltaje, corriente, temperatura, vibracion, alertas, componentes):
    return f"""Contexto del dispositivo:
- Lecturas actuales: V={voltaje}V | I={corriente}A | T={temperatura}°C | Vib={vibracion}g
- Alertas recientes: {alertas if alertas else 'Ninguna'}
- Componentes detectados: {', '.join(componentes) if componentes else 'No disponible'}"""

def simular_diagnostico(voltaje, corriente, temperatura, componentes):
    prompt = f"""Circuito analizado:
- Componentes detectados: {componentes}
- Voltaje: {voltaje}V
- Corriente: {corriente}A
- Temperatura: {temperatura}°C
- Perfil de voltaje: 5V

Genera el análisis y recomendaciones."""

    print("\n Generando diagnóstico...\n")
    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": """Eres un experto en electrónica y mantenimiento de circuitos.
Analiza los datos del circuito y genera recomendaciones de mantenimiento preventivo en español.
Responde SIEMPRE en JSON con este formato exacto:
{
  "estado_general": "normal|advertencia|critico",
  "componentes_en_riesgo": ["etiqueta1"],
  "recomendaciones": ["recomendación 1"]
}"""},
            {"role": "user", "content": prompt}
        ],
        options={"think": False}
    )
    try:
        resultado = json.loads(response["message"]["content"])
        print(f" Estado: {resultado.get('estado_general', '?').upper()}")
        print(f" Componentes en riesgo: {resultado.get('componentes_en_riesgo', [])}")
        print(" Recomendaciones:")
        for r in resultado.get("recomendaciones", []):
            print(f"   • {r}")
    except json.JSONDecodeError:
        print(response["message"]["content"])

def chat_interactivo(voltaje, corriente, temperatura, vibracion, alertas, componentes):
    historial = []
    contexto = construir_contexto(voltaje, corriente, temperatura, vibracion, alertas, componentes)

    print("\n Chat con el asistente (escribe 'salir' para terminar)\n")
    print("-" * 50)

    while True:
        pregunta = input("\n Tú: ").strip()
        if pregunta.lower() in ("salir", "exit", "q"):
            break
        if not pregunta:
            continue

        historial.append({"role": "user", "content": pregunta})

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": contexto},
        ] + historial

        print("\n Asistente: ", end="", flush=True)
        respuesta_completa = ""
        for chunk in ollama.chat(model=settings.OLLAMA_MODEL, messages=messages, stream=True, options={"think": False}):
            texto = chunk["message"]["content"]
            print(texto, end="", flush=True)
            respuesta_completa += texto

        print()
        historial.append({"role": "assistant", "content": respuesta_completa})


def main():
    print("=" * 50)
    print("  Test interactivo de Ollama")
    print(f"  Modelo: {settings.OLLAMA_MODEL}")
    print("=" * 50)

    # Verificar conexión
    try:
        ollama.list()
        print(" Ollama conectado\n")
    except Exception as e:
        print(f" No se pudo conectar a Ollama: {e}")
        print(f"  Asegúrate de que Ollama esté corriendo en {settings.OLLAMA_BASE_URL}")
        return

    # Configurar escenario de prueba
    print("Escenario de prueba:")
    print("  Dispositivo: Módulo Taller 1")

    voltaje = float(input("  Voltaje (default 5.1): ") or "5.1")
    corriente = float(input("  Corriente (default 0.3): ") or "0.3")
    temperatura = float(input("  Temperatura (default 35): ") or "35")
    vibracion = float(input("  Vibración (default 0.01): ") or "0.01")

    alertas_input = input("  Alertas (ej: 'voltaje alto', o Enter para ninguna): ").strip()
    alertas = [alertas_input] if alertas_input else []

    componentes_input = input("  Componentes (ej: 'R1,C1,LED1', o Enter para default): ").strip()
    componentes = componentes_input.split(",") if componentes_input else ["R1", "C1", "LED1", "IC1"]

    print("\n¿Qué quieres hacer?")
    print("  1. Generar diagnóstico automático")
    print("  2. Chat interactivo")
    print("  3. Ambos")

    opcion = input("\nOpción (1/2/3): ").strip()

    if opcion in ("1", "3"):
        simular_diagnostico(voltaje, corriente, temperatura, componentes)

    if opcion in ("2", "3"):
        chat_interactivo(voltaje, corriente, temperatura, vibracion, alertas, componentes)

    print("\n Sesión terminada.")


if __name__ == "__main__":
    main()
