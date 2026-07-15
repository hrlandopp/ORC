import os
import pandas as pd
from paddleocr import PPStructure, save_structure_res

# 1. Inicializar el motor de tablas en modo CPU (ideal para tus 4GB de RAM)
# 'layout=False' si solo vas a pasar imágenes que son PUREMENTE una tabla.
table_engine = PPStructure(show_log=False, image_orientation=False, layout=True)

# 2. Ruta de la imagen que quieres procesar
image_path = 'factura_o_tabla.jpg'
output_folder = './resultado'

# 3. Ejecutar el análisis de la estructura
result = table_engine(image_path)

# 4. Guardar los resultados visuales y HTML en una carpeta
save_structure_res(result, output_folder, os.path.basename(image_path).split('.')[0])

# 5. Buscar la tabla detectada y convertirla a Excel
for region in result:
    if region['type'] == 'table':
        # PP-Structure extrae la estructura directamente en formato HTML
        html_table = region['res']['html']
        
        # Pandas puede leer código HTML de tablas e indexarlo de forma nativa
        dfs = pd.read_html(html_table)
        
        if dfs:
            df = dfs[0]
            # Guardar en formato Excel listo para abrir
            excel_path = os.path.join(output_folder, "tabla_extraida.xlsx")
            df.to_excel(excel_path, index=False)
            print(f"¡Éxito! Tabla exportada correctamente en: {excel_path}")