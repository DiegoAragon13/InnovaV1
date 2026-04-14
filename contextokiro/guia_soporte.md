# Guía Soporte — Certamen de Proyectos InnovaTecNM 2026

## Plataforma

URL: https://innova.tecnm.mx/
Usuario: 21041217
Contraseña: 615289X6DP

---

## Categoría del proyecto

Categoría 2: Industria Eléctrica y Electrónica

### Descripción oficial de la categoría

Contempla el hardware y la optimización de sistemas eléctricos y electrónicos de potencia y control. Comprende proyectos orientados al diseño, rediseño, fabricación de dispositivos y componentes de semiconductores, así como sistemas, equipos o procesos eléctricos y electrónicos tanto analógicos como digitales. Su principal característica debe ser la **optimización técnica, funcional, productiva o de desempeño tecnológico** de los circuitos eléctricos y/o electrónicos como servicios o productos de consumo industrial, independientemente del área de aplicación: industrial, comercial o doméstico.

### Por qué aplica nuestro proyecto

El sistema integra hardware electrónico (ESP32-S3, INA219, sensores) con software embebido y una app móvil para el diagnóstico y mantenimiento predictivo de placas electrónicas. El valor central está en el hardware y su integración con IA, no solo en el software.

### Área de aplicación específica

**Digitalización y Automatización** — Uso de IA en la Industria 4.0 para mantenimiento predictivo. Sistemas IoT con énfasis en diseño e integración de hardware electrónico.

### Exclusiones a evitar

- No centrar la presentación en la app o el software como producto principal
- Siempre describir el desarrollo e integración del hardware electrónico
- No presentarlo como gadget o dispositivo portátil de consumo final

### Requisito de validación

Los proyectos deben ser validados por expertos en la Industria Eléctrica y/o Electrónica.
**Asesora técnica:** Dra. Rocío (electrónica)

---

## Estructura de la Memoria Técnica (Categoría 2)

La Memoria Técnica se registra en el SISTEMA InnovaTecNM. Tiene 5 secciones:

### Sección 1 — Descripción de la problemática u oportunidad de negocio
- Máximo 300 palabras + 4 imágenes opcionales (jpg, 300 KB)
- Explicar: origen del problema, a quién afecta, relevancia cuantificable
- Detallar el área de aplicación dentro de la categoría
- Mencionar los ejes transversales: Tecnologías Emergentes, Impacto Social, Sustentabilidad
- Presentar datos duros (estadísticas, fuentes confiables)
- Referencia: páginas 8-12 de la Guía Soporte

**Para nuestro proyecto:**
- Problema: diagnóstico de fallas en circuitos electrónicos es lento, manual y dependiente de experiencia
- Dato duro: industria manufacturera = 17% del PIB de México; paros de producción cuestan $50K-$500K MXN
- Eje transversal principal: Tecnologías Emergentes (IA + IoT)

### Sección 2 — Descripción de la propuesta de valor
- Máximo 300 palabras + 4 imágenes opcionales
- Identificar cómo el cliente resuelve el problema actualmente (dolor)
- Describir los beneficios de la solución
- Evidenciar consulta a usuarios y expertos
- Metodología sugerida: Design Thinking + Mapa de valor de Osterwalder

**Para nuestro proyecto:**
- Dolor actual: técnico usa multímetro manualmente, sin historial, sin alertas
- Beneficio: detección automática de componentes + monitoreo continuo + alertas predictivas + LLM

### Sección 3 — Descripción técnica de la solución y normatividad
- Máximo 350 palabras + 3 imágenes opcionales
- Detallar atributos técnicos en lenguaje claro
- Indicar estatus: simulado / probado / prototipo / listo para escalar
- Especificar tipo y grado de innovación
- Describir riesgos y planes de contingencia
- Mencionar barreras de implementación
- Normatividad aplicable:
  - Ley de la Industria Eléctrica (LIE)
  - Normas Oficiales Mexicanas (NOM)
  - Ley Federal de Protección a la Propiedad Industrial

**Para nuestro proyecto:**
- Estatus: backend implementado y probado, modelo ARGOS entrenado y exportado, app y hardware pendientes
- Innovación: combinación única de visión artificial on-device + monitoreo eléctrico + LLM con RAG
- Riesgo principal: precisión del modelo ARGOS en condiciones reales de campo

### Sección 4 — Propiedad intelectual
- Máximo 200 palabras + 2 imágenes opcionales
- Identificar figuras jurídicas aplicables:
  - Secreto industrial: algoritmo de análisis y prompt engineering del LLM
  - Registro de software: app móvil y backend FastAPI
  - Modelo de utilidad: diseño del módulo hardware (PCB final)
  - Marca: nombre y logotipo (pendiente definir)
- Referencias: https://www.gob.mx/impi / https://www.indautor.gob.mx/

### Sección 5 — Fuentes consultadas
- Máximo 200 palabras + 2 imágenes opcionales
- Formato APA: https://normas-apa.org/
- Nota: la IA no puede ser autora, solo fuente secundaria

---

## Estructura del Modelo de Negocios Preliminar

Aplica para Categoría 2 (Industria Eléctrica y Electrónica). Tiene 4 secciones:

### Sección 1 — Mercado objetivo y cliente potencial
- Máximo 400 palabras + 4 imágenes opcionales
- Definir perfil de cliente ideal (características, hábitos, motivaciones)
- Cuantificar el mercado
- Explicar diferenciador frente a competidores

**Para nuestro proyecto:**
- Cliente primario: técnicos de mantenimiento industrial en plantas manufactureras
- Cliente secundario: talleres de reparación, estudiantes de electrónica
- Mercado: +5,000 parques industriales en México
- Diferenciador: único dispositivo portátil que combina visión artificial + monitoreo eléctrico + LLM

### Sección 2 — Estructura de costos, gastos y precio unitario
- Máximo 350 palabras + 4 imágenes opcionales
- Inversión inicial estimada
- Costo unitario de producción
- Gastos fijos mensuales
- Precio de venta y margen

**Para nuestro proyecto:**
- Costo manufactura kit básico: ~$300 MXN
- Precio de venta: $1,200 MXN
- Margen: ~$900 MXN por kit

### Sección 3 — Modelo de ingresos
- Máximo 400 palabras + 4 imágenes opcionales
- Mecanismo de ingresos (venta directa, suscripción, licencia)
- Canales de distribución
- Estimación de ventas primer año
- Punto de equilibrio

**Para nuestro proyecto:**
- Tier 1: venta de hardware con software incluido
- Tier 2: licencia mensual B2B ($2,500-$6,000 MXN/mes)
- Tier 3: on-premise para industria regulada ($12,000-$20,000 MXN/mes)

### Sección 4 — Bitácora de desarrollo del proyecto
- Máximo 500 palabras + 8 imágenes opcionales
- Lista de 10-15 actividades secuenciales del avance
- Etapa actual del proyecto
- Brechas y plan para resolverlas

**Para nuestro proyecto (actividades completadas):**
1. Definición del problema y propuesta de solución
2. Diseño de arquitectura del sistema (backend, app, hardware, IA)
3. Selección y fusión de datasets en Roboflow (2,976 imágenes)
4. Entrenamiento del modelo ARGOS v2 (mAP50: 0.721)
5. Entrenamiento del modelo ARGOS v3 con clases limpias (mAP50: 0.771)
6. Exportación a TFLite float32 (12 MB)
7. Implementación del backend FastAPI con Docker
8. Pruebas de todos los endpoints (auth, lecturas, diagnósticos, alertas, chat)
9. Validación del modelo con imágenes reales de placas electrónicas

**Pendientes:**
- Desarrollo de app Flutter
- Firmware ESP32
- Protoboard físico
- Integración ARGOS en Flutter

---

## Ejes transversales del proyecto

| Eje | Justificación |
|---|---|
| Tecnologías Emergentes | Visión artificial (YOLOv8), LLM (Ollama), IoT (ESP32), RAG |
| Impacto Social | Democratiza el diagnóstico profesional para técnicos y talleres pequeños |
| Sustentabilidad | Mantenimiento preventivo extiende vida útil de equipos, reduce desperdicio electrónico |

---

## Fechas clave

| Etapa | Periodo |
|---|---|
| Local | Abril — Mayo 2026 |
| Regional | Septiembre 2026 |
| Nacional | 30 noviembre — 4 diciembre 2026 |

---

## Pendientes del concurso

- [ ] Registrar proyecto en https://innova.tecnm.mx/ (usuario: 21041217)
- [ ] Redactar Memoria Técnica (con Ing. Carlos y Dra. Rocío)
- [ ] Redactar Modelo de Negocios (con Ing. Carlos)
- [ ] Definir nombre final del proyecto
- [ ] Preparar pitch (Diego, Michelle, Felix)
- [ ] Tener protoboard físico listo para etapa local
- [ ] Recopilar datos duros para justificar el problema (estadísticas de mantenimiento industrial en México)
- [ ] Consultar a usuarios/expertos para validar propuesta de valor (Design Thinking)
