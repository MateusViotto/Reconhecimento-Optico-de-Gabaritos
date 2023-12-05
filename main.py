import cv2
import utils


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
imagem_binarizada_gabarito = utils.binarizar(gabarito)
print('Prova do aluno: ')
imagem_binarizada = utils.binarizar(imagem)


# Inverter as cores
print('Invertendo as cores. . .')
print('Gabarito:')
gabarito_invertido = utils.inverter_imagem(imagem_binarizada_gabarito)
print('Prova do aluno:')
imagem_invertida = utils.inverter_imagem(imagem_binarizada)


# Obtém as partes da imagem separadas por linhas horizontais
print('Separando as imagens horizontalmente. . .')
print('Gabarito:')
partes_da_imagem_gabarito = utils.separar_por_linhas_horizontais(gabarito_invertido, altura_minima)
print('Prova do aluno:')
partes_da_imagem = utils.separar_por_linhas_horizontais(imagem_invertida, altura_minima)


#Separar as boxes
print('Separando as partes por boxes. . .')
print('Gabarito:')
valorPixels_gabarito = utils.separar_boxes(partes_da_imagem_gabarito)
print('Prova do aluno:')
valorPixels = utils.separar_boxes(partes_da_imagem)

#Separar indices
print('Conferindo os índices. . .\n')
resp = utils.armazenar_indices(valorPixels_gabarito, questoes)
indices = utils.armazenar_indices(valorPixels, questoes)


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

