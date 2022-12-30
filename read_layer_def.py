
def read_vectorQ(ruta, capas):
    for i in capas:
       uri= f'{ruta}/{i}.shp'
       vlayer= QgsVectorLayer(uri, i, 'ogr')
       QgsProject.instance().addMapLayer(vlayer)
     
    
    
ruta= '/home/cristian/Prog_qgis'
capas= ['Clip_canal', 'Buffeer_rio']

read_vectorQ(ruta, capas)

