# Firmware — ESP32-S3

Código del módulo de hardware del proyecto.

## Responsables

- Michelle (líder de electrónica)
- Felix
- Diego (apoyo)

## Stack

- Microcontrolador: ESP32-S3
- Framework: Arduino (PlatformIO recomendado)
- Sensores: INA219, DS18B20, MPU6050, SSD1306

## Pendientes

- [ ] Configurar proyecto PlatformIO
- [ ] Leer INA219 (voltaje y corriente)
- [ ] Leer DS18B20 (temperatura)
- [ ] Leer MPU6050 (vibración)
- [ ] Mostrar lecturas en OLED SSD1306
- [ ] Conectar a WiFi
- [ ] HTTP POST al backend `/lecturas` cada segundo
- [ ] Intervalo configurable (modo portátil vs modo fijo)
