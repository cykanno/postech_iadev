import os
import time

import cv2
from ultralytics import YOLO

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


# Substitua com suas credenciais e informações
remetente = "cykanno@gmail.com"  # Seu e-mail GMail
senha = "jtzq ugxp rxaw ciul"            # Sua senha GMail (ou senha de aplicativo se a autenticação de dois fatores estiver ativada)
destinatario = "floresfacilecom@gmail.com" # E-mail do destinatário
assunto = "Assunto do E-mail"
corpo = """
<html>
    <body>
    <p>Olá,</p>
    <p>Objeto cortante identificado.</p>
    <p>Atenciosamente,<br>
        Claidson
    </p>
    </body>
</html>
"""


def enviar_email(remetente, senha, destinatario, assunto, corpo):
    """
    Envia um e-mail

    Args:
        remetente (str): Endereço de e-mail do remetente.
        senha (str): Senha do remetente.
        destinatario (str): Endereço de e-mail do destinatário.
        assunto (str): Assunto do e-mail.
        corpo (str): Corpo do e-mail (pode ser HTML).
    """

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto

    mensagem.attach(MIMEText(corpo, 'html'))  # 'plain' para texto simples

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:  # Adapte para seu servidor SMTP
            servidor.starttls()
            servidor.login(remetente, senha)
            texto = mensagem.as_string()
            servidor.sendmail(remetente, destinatario, texto)
        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def processarVideo(video, model):    
    emailJaEnviado = False
    # Abre o vídeo
    cap = cv2.VideoCapture(video)

    while True:
        # Lê um frame do vídeo
        success, img = cap.read()
        if not success:
            break

        # Realiza a detecção de objetos no frame
        # results = model.predict(img, conf=0.2, iou=0.3)
        results = model.predict(img)

        # Anota os resultados no frame
        for r in results:
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0].tolist()  # Obtém as coordenadas da caixa delimitadora
                c = box.cls[0].item()  # Obtém a classe do objeto detectado
                
                # Converte as coordenadas para inteiros
                x1, y1, x2, y2 = map(int, b)

                # Desenha a caixa delimitadora
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Adiciona o rótulo da classe
                class_name = model.names[int(c)]
                cv2.putText(img, class_name, (x1+ 10, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                if emailJaEnviado == False:
                    # Enviar e-mail de alerta
                    assunto = f"Objeto cortante identificado"
                    corpo = f"Foi identificado um obejto cortante no vídeo {os.path.basename(video)}."
                    enviar_email(remetente, senha, destinatario, assunto, corpo)
                    emailJaEnviado = True

                time.sleep(0.5)

        # Mostra o vídeo com as detecções
        cv2.imshow("Object Detection", img)


        # Espera por uma tecla 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Libera os recursos
    cap.release()
    cv2.destroyAllWindows()


# Rotina principal
if __name__ == "__main__":
    # Obtém o diretório atual
    current_directory = os.getcwd()

    # Carrega o modelo treinado
    model = YOLO(current_directory + "/Fase_V/Hack/treino/best.pt")

    # Lista de caminhos para os vídeos
    video_paths = [
        os.path.join(current_directory, "Fase_V", "Hack", "video.mp4"),
        os.path.join(current_directory, "Fase_V", "Hack", "video2.mp4"),
    ]

    # Processa o vídeo
    for video_path in video_paths:
        processarVideo(video_path, model)
        