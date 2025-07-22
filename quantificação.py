from PIL import Image
import numpy as np
import os

bits_OG = 8

#carregando a imagem e convertendo para uma matriz numpy
try:
    relogio_PILL = Image.open('ctskull-256.tif')
    array_OG = np.array(relogio_PILL)

    altura_OG, largura_OG = array_OG.shape[:2]

except FileNotFoundError:
    print("Arquivo 'relogio.tif' não encontrado.")
    exit()

# Criando pasta para as imagens quantizadas
pasta_quantizada = "imagens_quantizadas"
if not os.path.exists(pasta_quantizada):
    os.makedirs(pasta_quantizada)

# Realiza a quantização da imagem original para diferentes profundidades de bits
for bits in range(7, 0, -1):
    # Calcula o fator de redução com base na diferença entre os bits originais e os desejados
    fator_reducao = 2 ** (bits_OG - bits)

    # Aplicando a quantização, reduzindo o número de níveis de cinza da imagem
    # Dividindo e multiplicando pelo fator de redução, os valores dos pixels são agrupados
    array_quantizado = (array_OG // fator_reducao) * fator_reducao

    # convertendo a matriz numpy de volta para uma imagem e salvando
    imagem_resampled = Image.fromarray(array_quantizado)
    imagem_resampled.save(os.path.join(pasta_quantizada, f"ctskull_{bits}.tif"))