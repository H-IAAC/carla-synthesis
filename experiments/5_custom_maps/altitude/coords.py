import os
import laspy
from pyproj import Transformer

# Este código lê arquivos .laz de uma pasta específica, calcula os limites extremos
# das coordenadas X e Y (em um sistema de coordenadas como UTM) e os converte para
# coordenadas geográficas (latitude e longitude) usando a biblioteca pyproj.

# O código percorre todos os arquivos .laz na pasta especificada, calcula os valores
# mínimos e máximos de X e Y, e os exibe tanto no sistema original quanto em latitude/longitude.

# Caminho para a pasta contendo os arquivos .laz
caminho_pasta = "ipiranga"

# Inicializar valores extremos
min_x, min_y = float('inf'), float('inf')
max_x, max_y = float('-inf'), float('-inf')

# Leia todos os arquivos .laz da pasta
for nome_arquivo in os.listdir(caminho_pasta):
    if nome_arquivo.endswith(".laz"):
        caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
        las = laspy.read(caminho_completo)
        
        min_x = min(min_x, las.x.min())
        max_x = max(max_x, las.x.max())
        min_y = min(min_y, las.y.min())
        max_y = max(max_y, las.y.max())

# Exibir coordenadas em sistema original (geralmente UTM)
print(f"Coordenadas (UTM ou outro sistema):")
print(f"X: {min_x} a {max_x}")
print(f"Y: {min_y} a {max_y}")

epsg_origem = "EPSG:31983" 
transformer = Transformer.from_crs(epsg_origem, "EPSG:4326", always_xy=True)

# Converter os cantos do retângulo
min_lon, min_lat = transformer.transform(min_x, min_y)
max_lon, max_lat = transformer.transform(max_x, max_y)

print("\nCoordenadas geográficas (latitude/longitude):")
print(f"Latitude: {min_lat} a {max_lat}")
print(f"Longitude: {min_lon} a {max_lon}")