- Obter dados LIDAR
    
    - https://geosampa.prefeitura.sp.gov.br/PaginasPublicas/_SBC.aspx
    
    - lupa→Download Imagens/MDC → Tipo MDT 2020
    
    - Selecionar regiões e baixar os .laz
    
- Achar as coordenadas inicial e final da área (coords.py)
- Baixar o mapa do OpenStreetMap da área a partir das coordenadas
- Converter o mapa do OpenStreetMap de osm para xodr (osm2xodr.py)
- Converter cada .laz para um mapa de elevação .tif (laz2dem.py)
- Juntar os .tif em um único .las por meio do CloudCompare
- Converter o novo .las para .tif (conv.py)
- Rotacionar .tif (rotacao.py)
- Juntar o mapa do OSM com o .tif (elevacao2.py)
- Importar mapa para o CARLA