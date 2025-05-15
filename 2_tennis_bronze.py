import os
import pandas as pd

# Carpeta de archivos ATP y WTA
atp_folder = "./data/raw/atp/"
wta_folder = "./data/raw/wta/"

# Función para leer y combinar archivos
def cargar_y_unir_archivos(folder_path, tour_name):
    all_data = []
    total_rows = 0
    for file in os.listdir(folder_path):
        if file.endswith('.xls') or file.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file)
            try:
                if file.endswith('.xls'):
                    df = pd.read_excel(file_path, engine='xlrd')
                elif file.endswith('.xlsx'):
                    df = pd.read_excel(file_path, engine='openpyxl')
                df['tour'] = tour_name  # Añadimos la columna tour
                total_rows += len(df)
                all_data.append(df)
                print(f"📄 {file} -> {len(df)} filas")
            except Exception as e:
                print(f"⚠️ Error leyendo {file}: {e}")
    df_final = pd.concat(all_data, ignore_index=True)
    print(f"🔢 Registros esperados para {tour_name}: {total_rows}")
    print(f"📊 Registros unificados para {tour_name}: {len(df_final)}")
    return df_final

# Cargar y combinar ATP
print("📂 Procesando archivos ATP...")
df_atp = cargar_y_unir_archivos(atp_folder, "ATP")

# Cargar y combinar WTA
print("📂 Procesando archivos WTA...")
df_wta = cargar_y_unir_archivos(wta_folder, "WTA")

# Crear carpeta de salida si no existe
os.makedirs("./data/processed_bronze/", exist_ok=True)

# Guardar archivos finales
print("💾 Guardando archivos unificados...")
df_atp.to_csv("./data/processed_bronze/atp_matches.csv", index=False)
df_wta.to_csv("./data/processed_bronze/wta_matches.csv", index=False)

print("✅ Unificación completa: ATP y WTA disponibles en /data/processed_bronze/")
