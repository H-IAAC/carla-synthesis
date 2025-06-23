import xml.etree.ElementTree as ET
from scipy.interpolate import RegularGridInterpolator
import numpy as np

dem = np.load("dem.npy")
x_coords = np.load("dem_x_coords.npy")
y_coords = np.load("dem_y_coords.npy")

interpolador = RegularGridInterpolator((y_coords, x_coords), dem)

# Abrir o .xodr gerado do OSM
tree = ET.parse("mapa_gerado_do_osm.xodr")
root = tree.getroot()

for road in root.findall(".//road"):
    planview = road.find("planView")
    if planview is None:
        continue

    elevation_profile = ET.SubElement(road, "elevationProfile")

    for geometry in planview.findall("geometry"):
        x = float(geometry.attrib["x"])
        y = float(geometry.attrib["y"])
        s = float(geometry.attrib["s"])
        
        try:
            z = float(interpolador((y, x)))
        except:
            z = 0.0
        
        # Elevação simples com coeficientes zerados (reta)
        ET.SubElement(elevation_profile, "elevation", {
            "s": str(s),
            "a": str(z),
            "b": "0.0",
            "c": "0.0",
            "d": "0.0"
        })

# Salvar arquivo atualizado
tree.write("mapa_com_elevacao.xodr")