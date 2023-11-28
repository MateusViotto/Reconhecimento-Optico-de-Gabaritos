import cv2
import numpy as np

    
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
    imagens_separadas = []
    for i in range(len(coordenadas_y) - 1):
        altura_parte = coordenadas_y[i + 1] - coordenadas_y[i]
        if altura_parte >= altura_minima:
            parte_da_imagem = imagem[coordenadas_y[i]:coordenadas_y[i + 1], :]
            imagens_separadas.append(parte_da_imagem)

    # Adiciona a última parte da imagem
    altura_ultima_parte = imagem.shape[0] - coordenadas_y[-1]
    if altura_ultima_parte >= altura_minima:
        imagens_separadas.append(imagem[coordenadas_y[-1]:, :])
        
    return imagens_separadas

# Função para separar as alternativas em cada parte da imagem
def separar_alternativas(img):
    boxes = []
    cols = np.hsplit(img, 5)
    for box in cols:
        
        boxes.append(box)
        cv2.imshow('', box)
    return boxes

# Carrega a imagem
imagem = cv2.imread('Imagens/imagem3.jpg')


# Define a altura mínima para separação das linhas horizontais
altura_minima = 25

# Número de questões, escolhas e vetor de respostas corretas (gabarito)
questoes = 14
escolhas = 5
resp = [1,2,3,4,1,2,3,4,1,2,3,4,1,2]

# Array para armazenar os valores de pixels
valorPixels = np.zeros((questoes, escolhas))

# Contadores para percorrer a matriz de pixels
countC = 0
countR = 0

# Binarizar a imagem usando um limiar
limiar, imagem_binarizada = cv2.threshold(imagem, 128, 255, cv2.THRESH_BINARY)

# Inverter as cores
imagem_invertida = cv2.bitwise_not(imagem_binarizada)

# Obtém as partes da imagem separadas por linhas horizontais
partes_da_imagem = separar_por_linhas_horizontais(imagem_invertida, altura_minima)

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

# Lista para armazenar os índices das respostas escolhidas pelo aluno
indices = []
# Loop para determinar as respostas escolhidas
for x in range(0, questoes):
    arr = valorPixels[x]
    # Obtém o índice da resposta com o maior número de pixels
    maioresIndices = np.where(arr == np.amax(arr))
    indices.append(maioresIndices[0][0])

# Lista para armazenar as notas de cada questão
notas = []

print('Gabarito:           ', resp)
print('Respostas do aluno: ', indices)

# Loop para verificar as respostas e calcular as notas
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
print('\n\nNota do aluno: {:.2f}'.format(nota/10))

# Espera pela tecla para fechar as janelas
cv2.waitKey(0)
cv2.destroyAllWindows()