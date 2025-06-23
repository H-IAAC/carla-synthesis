import rasterio
from rasterio.enums import Resampling
import numpy as np

with rasterio.open("ipiranga/elevacao_geral.tif") as src:
    data = src.read()
    profile = src.profile

# Rotaciona 180° (inverte linhas)
rotated_data = data[:, ::-1, :]

with rasterio.open("ipiranga/elevacao_geral.tif", "w", **profile) as dst:
    dst.write(rotated_data)
