import cv2
import time
import math

p1 = 530
p2 = 300

xs = []
ys = []

video = cv2.VideoCapture("footvolleyball.mp4")
# Carregue o rastreador
tracker = cv2.TrackerCSRT_create()

# Leia o primeiro quadro do vídeo
success, img = video.read()

# Selecione a caixa delimitadora na imagem
bbox = cv2.selectROI("tracking", img, False)

# Inicialize o rastreador em img e na caixa delimitadora
tracker.init(img, bbox)

def goal_track(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    c1 = x + int(w / 2)
    c2 = y + int(h / 2)
    cv2.circle(img, (c1, c2), 2, (0, 0, 255), 5)

    cv2.circle(img, (int(p1), int(p2)), 2, (0, 255, 0), 3)
    dist = math.sqrt(((c1 - p1) ** 2) + (c2 - p2) ** 2)
    print(dist)

    if dist <= 20:
        cv2.putText(img, "Ponto", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    xs.append(c1)
    ys.append(c2)

    for i in range(len(xs) - 1):
        cv2.circle(img, (xs[i], ys[i]), 2, (0, 0, 255), 5)

def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)
    cv2.putText(img, "Rastreando", (75, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

while True:
    # Ler o vídeo e armazenar os valores nas variáveis check e img
    check, img = video.read()

    # Usar tracker.update() e armazenar os valores nas variáveis success e bbox
    success, bbox = tracker.update(img)

    if success:
        # Se o rastreamento for bem-sucedido, chame drawBox() passando img e bbox
        drawBox(img, bbox)
    else:
        # Se o rastreamento falhar, exiba "Errou" e chame goal_track() passando img e bbox
        cv2.putText(img, "Errou", (300, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        goal_track(img, bbox)

    # Mostrar o frame com a caixa delimitadora
    cv2.imshow("Tracking", img)

    # Aguarde por 30 milissegundos e verifique se a tecla 'q' é pressionada para sair do loop
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Liberar recursos
video.release()
cv2.destroyAllWindows()
