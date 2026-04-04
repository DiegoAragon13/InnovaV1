from sqlalchemy.ext.asyncio import AsyncSession
from models.lectura import Lectura
from models.alerta import Alerta

# Umbrales por defecto (se pueden sobreescribir con perfiles custom)
UMBRALES = {
    "5V":  {"voltaje_min": 4.5, "voltaje_max": 5.5, "corriente_max": 2.0, "temperatura_max": 70.0},
    "3.3V":{"voltaje_min": 3.0, "voltaje_max": 3.6, "corriente_max": 1.0, "temperatura_max": 70.0},
    "12V": {"voltaje_min": 11.0,"voltaje_max": 13.0,"corriente_max": 5.0, "temperatura_max": 85.0},
}

async def evaluar_lectura(lectura: Lectura, db: AsyncSession):
    """Evalúa una lectura y genera alertas si hay anomalías."""
    umbrales = UMBRALES.get("5V")  # TODO: obtener perfil del dispositivo

    alertas = []

    if lectura.voltaje is not None:
        if lectura.voltaje < umbrales["voltaje_min"]:
            alertas.append(Alerta(
                dispositivo_id=lectura.dispositivo_id,
                tipo="voltaje",
                mensaje=f"Voltaje bajo: {lectura.voltaje:.2f}V (mín {umbrales['voltaje_min']}V)",
                severidad="advertencia"
            ))
        elif lectura.voltaje > umbrales["voltaje_max"]:
            alertas.append(Alerta(
                dispositivo_id=lectura.dispositivo_id,
                tipo="voltaje",
                mensaje=f"Voltaje alto: {lectura.voltaje:.2f}V (máx {umbrales['voltaje_max']}V)",
                severidad="critico"
            ))

    if lectura.temperatura is not None and lectura.temperatura > umbrales["temperatura_max"]:
        alertas.append(Alerta(
            dispositivo_id=lectura.dispositivo_id,
            tipo="temperatura",
            mensaje=f"Temperatura alta: {lectura.temperatura:.1f}°C (máx {umbrales['temperatura_max']}°C)",
            severidad="critico"
        ))

    if lectura.corriente is not None and lectura.corriente > umbrales["corriente_max"]:
        alertas.append(Alerta(
            dispositivo_id=lectura.dispositivo_id,
            tipo="corriente",
            mensaje=f"Corriente alta: {lectura.corriente:.2f}A (máx {umbrales['corriente_max']}A)",
            severidad="advertencia"
        ))

    # Determinar estado general de la lectura
    if any(a.severidad == "critico" for a in alertas):
        lectura.estado = "critico"
    elif alertas:
        lectura.estado = "advertencia"

    for alerta in alertas:
        db.add(alerta)
