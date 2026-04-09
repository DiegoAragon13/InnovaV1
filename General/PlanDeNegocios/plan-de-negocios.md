# Plan de Negocios

> Alineado con los criterios del Certamen de Proyectos InnovaTecNM 2026
> Categoría: Industria Eléctrica y Electrónica
> Ejes transversales: Tecnologías Emergentes · Impacto Social · Sustentabilidad

---

## 1. Problema y oportunidad

El diagnóstico de fallas en circuitos electrónicos en entornos industriales es:
- Lento y dependiente de la experiencia del técnico
- Reactivo: se actúa cuando la falla ya ocurrió
- Sin documentación ni trazabilidad de mantenimientos

En México, la industria manufacturera representa más del 17% del PIB. Los tiempos muertos por fallas eléctricas no detectadas a tiempo generan pérdidas millonarias. No existe una herramienta accesible, portátil y con IA que combine identificación visual de componentes con monitoreo eléctrico en tiempo real.

---

## 2. Solución

Sistema portátil de diagnóstico y mantenimiento preventivo de placas electrónicas que integra:
- Módulo de hardware (ESP32-S3) con sensores de voltaje, corriente, temperatura y vibración
- App móvil Flutter con visión artificial (YOLO) para identificar componentes
- Backend con LLM que genera recomendaciones de mantenimiento preventivo
- Historial, estadísticas y reportes por dispositivo

---

## 3. Propuesta de valor

| Para quién | Qué problema resuelve | Cómo lo resuelve |
|---|---|---|
| Técnico industrial | Diagnóstico lento y sin documentación | Identifica componentes y genera reporte en minutos |
| Jefe de mantenimiento | Fallas imprevistas y costosas | Alertas preventivas antes de que ocurra la falla |
| Estudiante de electrónica | Aprendizaje sin retroalimentación | Identifica y explica componentes en tiempo real |

---

## 4. Mercado objetivo

### Mercado primario
- Técnicos de mantenimiento industrial en plantas manufactureras
- Talleres de reparación de electrónica
- Empresas con equipos electrónicos críticos

### Mercado secundario
- Instituciones educativas con programas de electrónica e ingeniería
- Técnicos independientes

### Tamaño de mercado (referencia)
- México cuenta con más de 5,000 parques industriales y zonas manufactureras
- El mercado global de mantenimiento predictivo industrial se estima en USD $23.5B para 2026 (MarketsandMarkets)
- Segmento accesible inicial: talleres y técnicos independientes en México

---

## 5. Modelo de negocio

El modelo principal se basa en **venta de hardware con margen** y **licenciamiento B2B**, evitando depender de suscripciones de consumidor que son difíciles de sostener en este mercado.

### Tier 1 — Técnico / Taller independiente
Venta directa del dispositivo. El software va incluido sin costo adicional.

| Producto | Costo estimado manufactura | Precio de venta | Margen |
|---|---|---|---|
| Kit básico (1 módulo + sondas + app) | ~$300 MXN | $1,200 MXN | ~$900 MXN |
| Kit profesional (2 módulos + accesorios) | ~$550 MXN | $2,200 MXN | ~$1,650 MXN |

> El software (app + historial básico en la nube) va incluido en la compra del hardware. Sin suscripciones.

---

### Tier 2 — Empresa / Planta industrial (B2B Cloud)
Para empresas que quieren múltiples técnicos y dispositivos con gestión centralizada. Aquí sí aplica un modelo de licencia porque el valor es claro y medible.

| Plan | Incluye | Precio estimado |
|---|---|---|
| Empresarial básico | Hasta 5 técnicos, 10 dispositivos, historial ilimitado | $2,500 MXN/mes |
| Empresarial avanzado | Técnicos ilimitados, API, reportes personalizados | $6,000 MXN/mes |

> Una planta que evita un solo paro de producción recupera el costo anual del plan en minutos.

---

### Tier 3 — On-Premise (entorno aislado para máxima privacidad)
Para empresas que **no pueden** mandar sus datos fuera de sus instalaciones por políticas de seguridad, regulaciones o confidencialidad industrial (automotriz, farmacéutica, defensa, gobierno).

El sistema corre en una **VPC dedicada en AWS**, completamente aislada de otros clientes. Los datos nunca se mezclan con otros tenants. La empresa se conecta a su entorno mediante VPN.

**Arquitectura del tenant aislado:**
```
Red interna del cliente
        ↓
AWS Site-to-Site VPN
        ↓
VPC dedicada (solo para ese cliente)
├── EC2 FastAPI (subred privada)
├── RDS PostgreSQL (subred privada, sin acceso público)
├── S3 bucket privado (solo accesible desde su VPC)
├── Bedrock Claude (región dedicada)
└── Security Groups + NACLs (firewall por capas)
```

- Cada cliente tiene su propia VPC, RDS, S3 y acceso a Bedrock — completamente aislados
- Nosotros administramos la infraestructura desde AWS Organizations (cuenta maestra)
- El cliente se conecta desde su red interna vía VPN, sin exponer nada a internet público
- Opción de migrar a sus propios servidores en el futuro si lo requieren

| Concepto | Descripción | Precio estimado |
|---|---|---|
| Setup inicial | Configuración de VPC, VPN, RDS, EC2, S3 | $25,000 – $40,000 MXN (único) |
| Licencia anual | Uso del software + soporte + actualizaciones | $144,000 – $240,000 MXN/año |
| Hardware (módulos ESP32) | Por dispositivo | $1,200 MXN/unidad |
| Infraestructura AWS | EC2 + RDS + S3 + VPN (incluida en licencia) | ~$86 USD/mes internos |

### Justificación del precio de licencia anual

| Concepto | Costo mensual estimado |
|---|---|
| Infraestructura AWS (EC2 + RDS + S3 + VPN) | ~$1,720 MXN (~$86 USD) |
| Soporte técnico y mantenimiento (4 hrs/mes) | ~$4,000 MXN |
| Actualizaciones de software y modelo IA | ~$2,000 MXN |
| Costo operativo total | ~$7,720 MXN/mes |
| **Precio cobrado (plan básico: hasta 10 técnicos)** | **$12,000 MXN/mes ($144,000/año)** |
| **Precio cobrado (plan avanzado: ilimitado + API)** | **$20,000 MXN/mes ($240,000/año)** |
| Margen plan básico | ~$4,280 MXN/mes (~55%) |
| Margen plan avanzado | ~$12,280 MXN/mes (~63%) |

> Para una planta industrial donde un paro de producción cuesta entre $50,000 y $500,000 MXN, una licencia de $12,000/mes se recupera evitando un solo incidente al año.

---

### Resumen de fuentes de ingreso

| Fuente | Mercado | Etapa |
|---|---|---|
| Venta de hardware (Kit básico/pro) | Técnicos, talleres | MVP y producción |
| Licencia empresarial (cloud) | Plantas industriales, empresas | V1.0 |
| On-premise (entorno aislado) | Industria regulada, gobierno | V2.0 |
| Soporte y actualizaciones | Todos los tiers | Continuo |

---

## 6. Análisis competitivo

### Multímetro tradicional
Un multímetro mide en el momento. No guarda historial, no detecta tendencias, no identifica componentes, no genera alertas. El técnico decide manualmente si la lectura es normal o no. **Un multímetro mide, este sistema predice.**

### Fracttal (CMMS con IoT)
Fracttal es un sistema de gestión de mantenimiento (CMMS) con sus propios dispositivos IoT (Fracttal Sense, Fracttal Box). Monitorea maquinaria industrial grande: motores, bombas, compresores. Empieza en $195 USD/mes solo de software, sin hardware incluido.

| Aspecto | Fracttal | Este sistema |
|---|---|---|
| Enfoque | Gestión de mantenimiento (órdenes, calendarios, técnicos) | Diagnóstico de placas electrónicas |
| Hardware | Sensores para maquinaria industrial fija | Dispositivo portátil para cualquier placa |
| Visión artificial | No | Sí — ARGOS identifica componentes |
| LLM | No | Sí — cruza componentes + lecturas y recomienda |
| Portabilidad | Instalación fija | Lo llevas a cualquier tablero o panel |
| Precio entrada | $195 USD/mes + hardware industrial | $1,200 MXN kit completo |
| Mercado | Plantas con presupuesto de infraestructura | Técnicos, talleres, industria mediana |

**Relación con Fracttal:** son complementarios. En una planta industrial, Fracttal gestiona las órdenes de trabajo y este dispositivo hace el diagnóstico electrónico de las tarjetas y PLCs. Un argumento de venta para Tier 2 y 3: "integrable con tu CMMS actual".

---

## 7. Ventaja competitiva

- No existe en el mercado una solución que combine visión artificial + monitoreo eléctrico + LLM en un solo dispositivo portátil accesible
- Enfoque preventivo vs reactivo: el sistema anticipa fallas, no solo las detecta
- Historial y trazabilidad: genera documentación de mantenimiento automáticamente
- Escalable: de protoboard a PCB, de servidor local a AWS, de app a plataforma SaaS

---

## 8. Ejes transversales InnovaTecNM

### Tecnologías Emergentes
- Visión artificial con YOLOv8 on-device
- LLM para generación de recomendaciones (Ollama / AWS Bedrock)
- IoT con ESP32-S3 y comunicación BLE
- Arquitectura cloud-ready en AWS

### Impacto Social
- Reduce tiempos de diagnóstico y costos de mantenimiento para pequeños talleres
- Democratiza el acceso a herramientas de diagnóstico profesional
- Aplicación educativa en instituciones técnicas y de ingeniería

### Sustentabilidad
- El mantenimiento preventivo extiende la vida útil de equipos electrónicos
- Reduce el desperdicio electrónico al evitar reemplazos innecesarios por fallas no diagnosticadas correctamente
- Menor consumo de recursos al optimizar intervenciones de mantenimiento

---

## 9. Estrategia de propiedad intelectual

*(Requerida para etapa nacional)*

| Figura jurídica | Aplicación |
|---|---|
| Secreto industrial | Algoritmo de análisis y prompt engineering del LLM |
| Registro de software | App móvil y backend FastAPI |
| Modelo de utilidad | Diseño del módulo de hardware (PCB final) |
| Marca | Nombre y logotipo del producto *(pendiente definir)* |

---

## 10. Escalabilidad

```
MVP (Competencia)          →    V1.0 B2B Cloud          →    On-Premise Enterprise
─────────────────────────────────────────────────────────────────────────────────────
Protoboard + laptop         →    PCB + AWS               →    Instalación en cliente
5-8 componentes YOLO        →    +30 componentes         →    Modelo fine-tuned
Ollama local                →    AWS Bedrock             →    Ollama en servidor cliente
1 usuario / 1 dispositivo   →    Multi-técnico cloud     →    Entorno 100% aislado
```

---

## 11. Roadmap

| Fase | Periodo | Hitos |
|---|---|---|
| MVP | Ahora → Etapa local | Protoboard funcional, app básica, YOLO 5-8 clases, demo |
| V1.0 | Post-competencia | PCB, modelo mejorado, backend en AWS, app publicada |
| V2.0 | 6-12 meses | Suscripciones, multi-usuario, fine-tuning del modelo |
| SaaS | 12-24 meses | Plataforma empresarial, API pública, expansión regional |

---

## Pendientes

- [ ] Nombre final del producto (afecta marca y registro)
- [ ] Investigar costos reales de manufactura del hardware para precio de venta
- [ ] Identificar posibles clientes piloto (talleres o plantas industriales locales)
- [ ] Preparar pitch deck para etapa regional
