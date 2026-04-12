"""
Test de ARGOS — Validación del modelo TFLite
Uso: python test_argos.py --imagen ruta/a/imagen.jpg
"""

import argparse
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import yaml

# Intentar importar tflite
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow as tf
    tflite = tf.lite


MODEL_PATH = "best_float32.tflite"
DATA_YAML  = "data.yaml"
IMG_SIZE   = 512
CONF_THRESHOLD = 0.35


def cargar_clases(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    names = data.get("names", [])
    # Soporta tanto lista como diccionario
    if isinstance(names, list):
        return {i: name for i, name in enumerate(names)}
    return names


def preprocesar(imagen_path, size):
    img = Image.open(imagen_path).convert("RGB")
    orig_w, orig_h = img.size
    img_resized = img.resize((size, size))
    arr = np.array(img_resized, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0), img, orig_w, orig_h


def xywh2xyxy(cx, cy, w, h, orig_w, orig_h, size):
    """Convierte coordenadas normalizadas YOLO a píxeles de la imagen original."""
    x1 = (cx - w / 2) * orig_w
    y1 = (cy - h / 2) * orig_h
    x2 = (cx + w / 2) * orig_w
    y2 = (cy + h / 2) * orig_h
    return x1, y1, x2, y2


def inferencia(model_path, input_data):
    interp = tflite.Interpreter(model_path=model_path)
    interp.allocate_tensors()

    inp  = interp.get_input_details()[0]
    out  = interp.get_output_details()[0]

    interp.set_tensor(inp["index"], input_data)
    interp.invoke()

    return interp.get_tensor(out["index"])  # shape: (1, num_clases+4, num_anchors)


def nms(detecciones, iou_threshold=0.45):
    """Elimina detecciones duplicadas del mismo componente."""
    if not detecciones:
        return []

    boxes = np.array([d["bbox"] for d in detecciones])
    scores = np.array([d["confianza"] for d in detecciones])

    x1, y1, x2, y2 = boxes[:,0], boxes[:,1], boxes[:,2], boxes[:,3]
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        inter = np.maximum(0, xx2 - xx1) * np.maximum(0, yy2 - yy1)
        iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)
        order = order[1:][iou < iou_threshold]

    return [detecciones[i] for i in keep]


def parsear_detecciones(output, clases, conf_thresh, orig_w, orig_h):
    """
    Output YOLOv8 TFLite: (1, 4 + num_clases, num_anchors)
    Cada anchor: [cx, cy, w, h, score_clase0, score_clase1, ...]
    """
    preds = output[0]          # (4 + num_clases, num_anchors)
    preds = preds.T             # (num_anchors, 4 + num_clases)

    detecciones = []
    for pred in preds:
        cx, cy, w, h = pred[:4]
        scores = pred[4:]
        clase_id = int(np.argmax(scores))
        confianza = float(scores[clase_id])

        if confianza < conf_thresh:
            continue

        nombre = clases.get(clase_id, str(clase_id))
        x1, y1, x2, y2 = xywh2xyxy(cx, cy, w, h, orig_w, orig_h, IMG_SIZE)
        detecciones.append({
            "clase": nombre,
            "confianza": confianza,
            "bbox": (x1, y1, x2, y2)
        })

    # Ordenar por confianza descendente
    detecciones.sort(key=lambda d: d["confianza"], reverse=True)

    # Aplicar NMS para eliminar duplicados
    detecciones = nms(detecciones)
    detecciones.sort(key=lambda d: d["confianza"], reverse=True)

    return detecciones


def dibujar(img, detecciones, salida="resultado.jpg"):
    draw = ImageDraw.Draw(img)
    colores = ["#FF4444", "#44FF44", "#4444FF", "#FFFF44", "#FF44FF", "#44FFFF"]

    for i, det in enumerate(detecciones):
        color = colores[i % len(colores)]
        x1, y1, x2, y2 = det["bbox"]
        draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
        label = f"{det['clase']} {det['confianza']:.0%}"
        draw.text((x1, max(0, y1 - 15)), label, fill=color)

    img.save(salida)
    print(f"\nImagen con detecciones guardada en: {salida}")


def main():
    parser = argparse.ArgumentParser(description="Test ARGOS TFLite")
    parser.add_argument("--imagen", required=True, help="Ruta a la imagen de prueba")
    parser.add_argument("--conf", type=float, default=CONF_THRESHOLD, help="Umbral de confianza (default: 0.35)")
    parser.add_argument("--salida", default="resultado.jpg", help="Ruta de imagen con detecciones")
    args = parser.parse_args()

    print(f"Cargando modelo: {MODEL_PATH}")
    print(f"Imagen: {args.imagen}")
    print(f"Umbral de confianza: {args.conf}\n")

    clases = cargar_clases(DATA_YAML)
    print(f"Clases cargadas: {len(clases)}")

    input_data, img_orig, orig_w, orig_h = preprocesar(args.imagen, IMG_SIZE)
    print(f"Imagen original: {orig_w}x{orig_h}px")

    output = inferencia(MODEL_PATH, input_data)
    print(f"Output shape: {output.shape}")

    detecciones = parsear_detecciones(output, clases, args.conf, orig_w, orig_h)

    if not detecciones:
        print(f"\nNo se detectaron componentes con confianza >= {args.conf}")
        print("Intenta bajar el umbral con --conf 0.2")
        return

    print(f"\n{len(detecciones)} componente(s) detectado(s):\n")
    print(f"{'Componente':<30} {'Confianza':>10}")
    print("-" * 42)
    for det in detecciones:
        print(f"{det['clase']:<30} {det['confianza']:>9.1%}")

    dibujar(img_orig, detecciones, args.salida)


if __name__ == "__main__":
    main()
