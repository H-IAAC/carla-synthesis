import xml.etree.ElementTree as ET
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from math import cos, sin

def add_elevation_to_xodr(xodr_path, output_path):
    # Carrega DEM
    dem = np.load("ipiranga/dem/out/dem_0.npy")
    x_coords = np.load("ipiranga/dem/out/dem_x_coords0.npy")
    y_coords = np.load("ipiranga/dem/out/dem_y_coords0.npy")
    interp = RegularGridInterpolator((y_coords, x_coords), dem)

    # Abre o .xodr
    tree = ET.parse(xodr_path)
    root = tree.getroot()

    for road in root.findall(".//road"):
        planview = road.find("planView")
        if planview is None:
            continue

        elevation_profile = ET.SubElement(road, "elevationProfile")

        for geometry in planview.findall("geometry"):
            length = float(geometry.attrib["length"])
            x0 = float(geometry.attrib["x"])
            y0 = float(geometry.attrib["y"])
            hdg = float(geometry.attrib["hdg"])
            s0 = float(geometry.attrib["s"])

            # Interpola ponto inicial
            try:
                z0 = float(interp((y0, x0)))
            except:
                z0 = 0.0

            # Ponto final
            x1 = x0 + length * cos(hdg)
            y1 = y0 + length * sin(hdg)

            try:
                z1 = float(interp((y1, x1)))
            except:
                z1 = z0

            slope = (z1 - z0) / length if length > 0 else 0.0

            ET.SubElement(elevation_profile, "elevation", {
                "s": str(s0),
                "a": str(z0),
                "b": str(slope),
                "c": "0.0",
                 "d": "0.0"
            })

    tree.write(output_path)


add_elevation_to_xodr("ipiranga/ipiranga.xodr", "ipiranga/ipiranga_elevacao.xodr")