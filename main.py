import cv2
import numpy as np
import matplotlib.pyplot as plt

def separar_por_linhas_horizontais(imagem, altura_minima):
    # Converte a imagem para escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplica um desfoque para reduzir o ruído
    cinza = cv2.GaussianBlur(cinza, (5, 5), 0)

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

def mostrar_imagem(img):
    # Exiba a imagem usando matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_rgb)
    plt.axis('off')  # Desliga os eixos
    plt.show()

# Função para separar as alternativas em cada parte da imagem
def separar_alternativas(img):
    boxes = []
    cols = np.hsplit(img, 5)
    for box in cols:
        boxes.append(box)
    return boxes


def separar_boxes(partes_da_imagem):
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
          # Converte a caixa para escala de cinza
          cinza = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
          # Conta o número de pixels não pretos na caixa
          totalPixels = cv2.countNonZero(cinza)
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

def binarizar(img):
    # Define um limiar para a binarização (no caso, 128)
    limiar, imagem_binarizada = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
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

# Carrega a imagem
imagem = cv2.imread('Imagens/imagem2.jpg')
gabarito = cv2.imread('Imagens/gabarito.jpg')

# Define a altura mínima para separação das linhas horizontais
altura_minima = 25

# Número de questões, escolhas e vetor de respostas corretas (gabarito)
questoes = 14
escolhas = 5

# Binarizar a imagem usando um limiar
print('Binarizando a imagem . . .\n')
print('Gabarito:')
imagem_binarizada_gabarito = binarizar(gabarito)
print('Prova do aluno: ')
imagem_binarizada = binarizar(imagem)


# Inverter as cores
print('Invertendo as cores. . .')
print('Gabarito:')
gabarito_invertido = inverter_imagem(imagem_binarizada_gabarito)
print('Prova do aluno:')
imagem_invertida = inverter_imagem(imagem_binarizada)


# Obtém as partes da imagem separadas por linhas horizontais
print('Separando as imagens horizontalmente. . .')
print('Gabarito:')
partes_da_imagem_gabarito = separar_por_linhas_horizontais(gabarito_invertido, altura_minima)
print('Prova do aluno:')
partes_da_imagem = separar_por_linhas_horizontais(imagem_invertida, altura_minima)


#Separar as boxes
print('Separando as partes por boxes. . .')
print('Gabarito:')
valorPixels_gabarito = separar_boxes(partes_da_imagem_gabarito)
print('Prova do aluno:')
valorPixels = separar_boxes(partes_da_imagem)

#Separar indices
print('Conferindo os índices. . .\n')
resp = armazenar_indices(valorPixels_gabarito, questoes)
indices = armazenar_indices(valorPixels, questoes)


# Lista para armazenar as notas de cada questão
notas = []

print('Gabarito:           ', resp)
print('Respostas do aluno: ', indices)
print('\n')

# Loop para verificar as respostas e calcular as notas
print('Corrigindo os exercícios. . .\n')
for x in range(0, questoes):
    if resp[x] == indices[x]:
        notas.append(1)
        print('Acertou a ' + str(x+1) + '!')
    else:
        notas.append(0)
        print('Errou a ' + str(x+1) + '!')

# Calcula a nota final do aluno
nota = (sum(notas)/questoes) * 100

# Imprime a nota final
print('\n\nAcertos: ', sum(notas))
print('Erros: ', questoes - sum(notas))
print('Nota do aluno: {:.2f}'.format(nota/10))

