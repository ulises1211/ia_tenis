import pandas as pd
import os

# Rutas
input_folder = "./data/processed_bronze/"
output_folder = "./data/processed_silver/"
os.makedirs(output_folder, exist_ok=True)

# Archivos a procesar
files = {
    "ATP": os.path.join(input_folder, "atp_matches.csv"),
    "WTA": os.path.join(input_folder, "wta_matches.csv")
}

# Columnas de apuestas antiguas a eliminar
columns_to_drop = [
    'B&WW', 'B&WL', 'GBW', 'GBL', 'CBW', 'CBL', 'EXW', 'EXL',
    'LBW', 'LBL', 'SBW', 'SBL', 'SJW', 'SJL', 'IWW', 'IWL',
    'UBW', 'UBL'
]

# Función para limpiar y preparar dataset
def limpiar_preparar(df, tour_name):
    print(f"\n🧹 Limpiando y preparando {tour_name}...")

    # Eliminar columnas antiguas si existen
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

    # Convertir columnas de ranking, puntos y cuotas a numérico
    for col in ['WRank', 'LRank', 'WPts', 'LPts', 'B365W', 'B365L']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Crear nueva columna: diferencia de ranking
    df['rank_diff'] = df['WRank'] - df['LRank']

    # Crear nueva columna: diferencia de puntos
    df['points_diff'] = df['WPts'] - df['LPts']

    # Crear nueva columna: favorito por apuestas
    if 'B365W' in df.columns and 'B365L' in df.columns:
        df['fav_winner'] = (df['B365W'] < df['B365L']).astype('Int64')  # 'Int64' para permitir NaNs
    else:
        df['fav_winner'] = None

    # Convertir superficies en dummies (Hard, Clay, Grass)
    if 'Surface' in df.columns:
        surface_dummies = pd.get_dummies(df['Surface'], prefix='surface')
        df = pd.concat([df, surface_dummies], axis=1)

    # Opcional: eliminar partidas con Surface desconocida
    df = df[df['Surface'].isin(['Hard', 'Clay', 'Grass'])]

    # Resetear índice
    df = df.reset_index(drop=True)

    return df


# Procesar ambos datasets
for tour, filepath in files.items():
    print(f"📂 Procesando {tour}...")
    df = pd.read_csv(filepath)

    # Limpiar y preparar
    df_ready = limpiar_preparar(df, tour)

    # Guardar
    output_path = os.path.join(output_folder, f"{tour.lower()}_matches_ready.csv")
    df_ready.to_csv(output_path, index=False)
    print(f"✅ {tour} preparado y guardado en {output_path}")

print("\n🏁 Limpieza y preparación terminada para ATP y WTA.")
