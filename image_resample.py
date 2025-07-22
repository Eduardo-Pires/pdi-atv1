from PIL import Image
import numpy as np
import os

dpi_og = 1250
dpi_resamples = [300,150,72]

#carregando a imagem e convertendo para uma matriz numpy
try:
    relogio_PILL = Image.open("relogio.tif")
    array_OG = np.array(relogio_PILL)

    altura_OG, largura_OG = array_OG.shape[:2]

except FileNotFoundError:
    print("Arquivo 'relogio.tif' não encontrado.")
    exit()

# Criando pasta para as imagens reamostradas
pasta_reamostrada = "imagens_reamostradas"
if not os.path.exists(pasta_reamostrada):
    os.makedirs(pasta_reamostrada)

for dpi in dpi_resamples:
    # Calculando as novas dimensões
    # Dimensão Original(pixels) * DPI de destino / DPI original
    largura_RS = int(largura_OG * dpi / dpi_og)
    altura_RS = int(altura_OG * dpi / dpi_og)

    # Criando uma matriz vazia com as novas dimensões
    # o dtype=array_OG.dtype garante que a matriz tenha o mesmo tipo de dados que a imagem original
    array_resampled = np.zeros((altura_RS, largura_RS), dtype=array_OG.dtype)

    # calculando as novas proporções
    escala_y = altura_OG / altura_RS
    escala_x = largura_OG / largura_RS

    # mapeando os pixels utilizando a lógica de nearest neighbor
    for y_RS in range(altura_RS):
        for x_RS in range(largura_RS):
            # Calculando os índices correspondentes na imagem original, encontrando a posição correspondente.
            y_OG = int(y_RS * escala_y)
            x_OG = int(x_RS * escala_x)

            # Garantindo que os índices não saiam dos limites da imagem original
            y_OG = min(y_OG, altura_OG - 1)
            x_OG = min(x_OG, largura_OG - 1)

            # Copia o pixel do vizinho mais próximo
            array_resampled[y_RS, x_RS] = array_OG[y_OG, x_OG]

    # convertendo a matriz numpy de volta para uma imagem e salvando 
    imagem_resampled = Image.fromarray(array_resampled)
    imagem_resampled.save(os.path.join(pasta_reamostrada, f"relogio_{dpi}.tif"))