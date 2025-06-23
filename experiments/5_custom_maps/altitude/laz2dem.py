import laspy
import numpy as np
from scipy.interpolate import griddata
import rasterio
from rasterio.transform import from_origin

# converts a `.laz` LiDAR file into a Digital Elevation Model (DEM)

def laz_to_dem_int16(input_laz, i, output_tif=None, resolution=1.0):
    # Ler arquivo .laz
    with laspy.open(input_laz) as laz_file:
        las = laz_file.read()
        x = las.x
        y = las.y
        z = las.z

    print(f"Pontos lidos: {len(x)}")

    # Definir os limites da grade
    min_x, max_x = x.min(), x.max()
    min_y, max_y = y.min(), y.max()

    # Criar grade
    grid_x, grid_y = np.meshgrid(
        np.arange(min_x, max_x, resolution),
        np.arange(min_y, max_y, resolution)
    )

    # Interpolar elevação (z) na grade
    grid_z = griddata(
        points=(x, y),
        values=z,
        xi=(grid_x, grid_y),
        method='linear'
    )

    # Substituir valores NaN por 0 ou outro valor padrão
    grid_z = np.nan_to_num(grid_z, nan=0)

    # Converter para int16
    grid_z_int16 = grid_z.astype(np.int16)

    if output_tif:
        transform = from_origin(min_x, max_y, resolution, resolution)
        with rasterio.open(
            output_tif,
            'w',
            driver='GTiff',
            height=grid_z_int16.shape[0],
            width=grid_z_int16.shape[1],
            count=1,
            dtype='int16',
            crs='EPSG:4326',
            transform=transform,
        ) as dst:
            dst.write(grid_z_int16, 1)

    np.save(f"ipiranga/dem/out/dem_{i}.npy", grid_z_int16)
    np.save(f"ipiranga/dem/out/dem_x_coords{i}.npy", grid_x[0, :])
    np.save(f"ipiranga/dem/out/dem_y_coords{i}.npy", grid_y[:, 0])

    i += 1
    return grid_z_int16

if __name__ == "__main__":
    i = 0
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-121_1000.laz", i, output_tif="ipiranga/dem/saida_dem_0.tif", resolution=1.0)
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-122_1000.laz", i, output_tif="ipiranga/dem/saida_dem_1.tif", resolution=1.0)
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-131_1000.laz", i, output_tif="ipiranga/dem/saida_dem_2.tif", resolution=1.0)
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-123_1000.laz", i, output_tif="ipiranga/dem/saida_dem_3.tif", resolution=1.0)
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-124_1000.laz", i, output_tif="ipiranga/dem/saida_dem_4.tif", resolution=1.0)
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-133_1000.laz", i, output_tif="ipiranga/dem/saida_dem_5.tif", resolution=1.0)
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-151_1000.laz", i, output_tif="ipiranga/dem/saida_dem_6.tif", resolution=1.0)
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-152_1000.laz", i, output_tif="ipiranga/dem/saida_dem_7.tif", resolution=1.0)
    laz_to_dem_int16("ipiranga/lidar/MDT_3325-161_1000.laz", i, output_tif="ipiranga/dem/saida_dem_8.tif", resolution=1.0)