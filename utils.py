import cv2
import numpy as np
import matplotlib.pyplot as plt

def mostrar_imagem(img):
    # Exiba a imagem usando matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis('off')  # Desliga os eixos
    plt.show()

#==========================Utils======================================
def binarizar(img):
    # Converte a imagem para escala de cinza
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Define um limiar para a binarização (no caso, 128)
    limiar, imagem_binarizada = cv2.threshold(cinza, 128, 255, cv2.THRESH_BINARY)
    # Chama a função mostrar_imagem para exibir a imagem binarizada
    mostrar_imagem(imagem_binarizada)
    # Retorna a imagem binarizada
    return imagem_binarizada

def inverter_imagem(img):
    # Utiliza a função cv2.bitwise_not para inverter os valores dos pixels na imagem
    img = cv2.bitwise_not(img)
    # Chama a função mostrar_imagem para exibir a imagem invertida
    mostrar_imagem(img)
    # Retorna a imagem invertida
    return img

def separar_por_linhas_horizontais(imagem, altura_minima):

    # Aplica um desfoque para reduzir o ruído
    cinza = cv2.GaussianBlur(imagem, (5, 5), 0)

    # Detecta bordas na imagem
    bordas = cv2.Canny(cinza, 50, 150)

    # Detecta linhas usando a transformada de Hough
    linhas = cv2.HoughLinesP(bordas, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Coordenadas y dos pontos finais das linhas horizontais
    coordenadas_y = [linha[0][1] for linha in linhas if linha[0][1] == linha[0][3]]

    # Ordena as coordenadas y
    coordenadas_y.sort()

    # Separa a imagem com base nas linhas horizontais
    # Lista para armazenar as imagens separadas
    imagens_separadas = []

    # Itera sobre as coordenadas verticais (coordenadas_y)
    for i in range(len(coordenadas_y) - 1):
        # Calcula a altura da parte da imagem entre as coordenadas y
        altura_parte = coordenadas_y[i + 1] - coordenadas_y[i]
        # Verifica se a altura atende ao critério mínimo
        if altura_parte >= altura_minima:
            # Extrai a parte da imagem entre as coordenadas y
            parte_da_imagem = imagem[coordenadas_y[i]:coordenadas_y[i + 1], :]
            # Adiciona a parte da imagem à lista de imagens separadas
            imagens_separadas.append(parte_da_imagem)

    # Calcula a altura da última parte da imagem
    altura_ultima_parte = imagem.shape[0] - coordenadas_y[-1]

    # Verifica se a altura da última parte atende ao critério mínimo
    if altura_ultima_parte >= altura_minima:
        # Extrai a última parte da imagem
        imagens_separadas.append(imagem[coordenadas_y[-1]:, :])
    # Exibe a primeira imagem da lista (assumindo que exista pelo menos uma imagem)

    mostrar_imagem(imagens_separadas[0])
    # Retorna a lista de imagens separadas
    return imagens_separadas


# Função para separar as alternativas em cada parte da imagem
def separar_alternativas(img):
    boxes = []
    cols = np.hsplit(img, 5)
    for box in cols:
        boxes.append(box)
    return boxes


def separar_boxes(partes_da_imagem, questoes, escolhas):
  # Array para armazenar os valores de pixels
  valorPixels = np.zeros((questoes, escolhas))

  # Contadores para percorrer a matriz de pixels
  countC = 0
  countR = 0
  # Loop para percorrer cada parte da imagem
  for i, parte in enumerate(partes_da_imagem):
      # Separa as alternativas em cada parte
      boxes = separar_alternativas(parte)
      # Loop para percorrer cada caixa (alternativa)
      for im in boxes:
          # Conta o número de pixels não pretos na caixa
          totalPixels = cv2.countNonZero(im)
          # Armazena o número de pixels na matriz myPixelVal
          valorPixels[countR][countC] = totalPixels
          countC += 1
          if countC == escolhas:
              countR += 1
              countC = 0
  mostrar_imagem(boxes[2])
  return valorPixels

def armazenar_indices(valorPixels, questoes):
  # Lista para armazenar os índices das respostas escolhidas pelo aluno
  indices = []
  # Loop para determinar as respostas escolhidas
  for x in range(0, questoes):
      arr = valorPixels[x]
      #O primeiro box deve ser maior do que todos os outros quando estão em branco, dessa maneira se o aluno não preencher a resposta ela será considerada errada.
      arr[0] = 200
      # Obtém o índice da resposta com o maior número de pixels
      maioresIndices = np.where(arr == np.amax(arr))
      indices.append(maioresIndices[0][0])
  return indices
