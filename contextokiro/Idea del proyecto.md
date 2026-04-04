# Sistema Inteligente de Diagnóstico y Mantenimiento de Placas Electrónicas

## Nombre tentativo
**ElectroScan** — Sistema IoT con IA para diagnóstico de circuitos electrónicos
*(nombre final por definir)*

---

## Categoría InnovaTecNM 2026
**Categoría 2: Industria Eléctrica y Electrónica**

Eje transversal: Tecnologías Emergentes (IA + IoT)

---

## Problema que resuelve

El diagnóstico de fallas en circuitos electrónicos es un proceso lento, manual y que depende fuertemente de la experiencia del técnico. En entornos industriales, un fallo no detectado a tiempo puede generar tiempos muertos costosos y pérdidas de producción. No existe una herramienta accesible que combine identificación visual de componentes con monitoreo eléctrico en una sola solución portátil orientada al mantenimiento preventivo.

---

## Público objetivo

**Principal:** Técnicos de mantenimiento industrial y de electrónica
**Secundario:** Estudiantes de ingeniería electrónica y técnicos en formación

---

## Solución propuesta

### App móvil (Flutter)
- El técnico toma una foto de la placa
- El modelo de IA detecta componentes y los marca con bounding boxes
- Se genera una lista editable: el técnico puede corregir, agregar o eliminar componentes
- La lista validada se guarda como el "inventario" de esa placa
- Visualización de datos eléctricos en tiempo real desde el módulo ESP32
- Historial de diagnósticos, tendencias y alertas preventivas
- Generación de reportes de mantenimiento exportables

### Módulo de hardware (ESP32-S3)
- Conexión al circuito mediante sondas de prueba tipo pogo pin (precisas y profesionales)
- Pinzas caimán incluidas como accesorio para cables gruesos
- Medición no invasiva de voltaje, corriente y temperatura
- Sensores: INA219/INA3221 (voltaje/corriente), DS18B20 o NTC (temperatura)
- Pantalla OLED 0.96" (SSD1306) para lectura local sin necesidad del teléfono
- Comunicación WiFi/BLE con la app móvil

### Servidor / Backend (Python + FastAPI)
- Recepción y procesamiento de imágenes y datos eléctricos
- Modelo de visión artificial (YOLOv8/YOLOv11) entrenado desde cero
- Comparación de lecturas contra rangos normales por tipo de componente
- Detección de tendencias: "este circuito se calienta más cada semana"
- Generación de alertas preventivas antes de que ocurra una falla
- Almacenamiento de historial por placa/dispositivo en PostgreSQL

---

## Enfoque de diagnóstico: Mantenimiento Preventivo

El sistema no solo detecta fallas activas, sino que anticipa problemas antes de que ocurran:

- Monitorea voltaje, corriente y temperatura continuamente
- Compara contra rangos óptimos por tipo de componente
- Genera alertas cuando una variable se acerca al límite (no solo cuando lo supera)
- El historial permite ver tendencias a lo largo del tiempo
- Ejemplo de alerta: *"El capacitor C3 lleva 3 sesiones operando por encima del rango de temperatura recomendado. Se recomienda revisión."*

---

## Flujo de uso

1. El técnico conecta las sondas del módulo ESP32-S3 al circuito
2. Abre la app y toma una foto de la placa
3. El modelo de IA identifica los componentes y genera una lista editable
4. El técnico valida o corrige la lista de componentes
5. El módulo envía lecturas eléctricas en tiempo real al servidor
6. El backend analiza los datos y detecta anomalías o tendencias
7. La app muestra alertas preventivas y recomendaciones
8. El técnico guarda el diagnóstico y exporta el reporte

---

## Stack tecnológico

| Componente | Tecnología |
|---|---|
| App móvil | Flutter (Android/iOS) |
| Microcontrolador | ESP32-S3 |
| Conexión al circuito | Sondas pogo pin + pinzas caimán (accesorio) |
| Sensores | INA219, DS18B20/NTC |
| Pantalla local | OLED 0.96" SSD1306 |
| Modelo de visión | YOLOv8 / YOLOv11 |
| Backend | Python + FastAPI |
| Base de datos | PostgreSQL |
| Comunicación IoT | WiFi / BLE / MQTT |

---

## Modelo de negocio

**Producto físico + App** — el usuario compra el dispositivo y descarga la app gratuitamente.

| Fuente de ingreso | Descripción |
|---|---|
| Venta del dispositivo | Hardware ensamblado listo para usar con sondas incluidas |
| Suscripción (futuro) | Historial en la nube, reportes avanzados, múltiples dispositivos |
| Licencia empresarial (futuro) | Para plantas industriales con varios técnicos |

---

## Alcance del MVP (Etapa Local InnovaTecNM)

Para la etapa local se requiere una **prueba de concepto**:

1. Identificación de 5-8 componentes comunes: resistencias, capacitores, LEDs, transistores, ICs
2. Lista editable de componentes detectados en la app
3. Lectura de voltaje y corriente con el módulo ESP32-S3
4. Alerta básica cuando una variable eléctrica sale del rango normal
5. Pantalla OLED mostrando lecturas locales
6. App Flutter mostrando foto analizada + datos eléctricos en tiempo real

Fuera del MVP (etapas posteriores):
- Historial en la nube y tendencias
- Reportes exportables
- Modelo de visión con alta precisión
- Múltiples usuarios / licencia empresarial

---

## Valor e innovación

- Combina visión artificial + monitoreo eléctrico en una sola herramienta portátil
- Enfoque preventivo: anticipa fallas antes de que ocurran
- Solución no invasiva con sondas profesionales
- Inventario editable de componentes que mejora con el uso
- Reduce tiempos de diagnóstico y dependencia de experiencia manual
- Potencial de escalar a modelo SaaS o herramienta profesional comercial

---

## Pendientes

- [ ] Nombre final del proyecto
- [ ] Dataset para entrenar el modelo de visión (Roboflow Universe + fotos propias)
- [ ] Protocolo de comunicación principal: WiFi vs BLE vs MQTT
- [ ] Diseño del módulo ESP32-S3 (protoboard para MVP, PCB a futuro)
