import pandas as pd
import os

# Paths
input_folder = "./data/processed_silver/"
output_folder = "./data/processed_silver_enriched/"
os.makedirs(output_folder, exist_ok=True)

# Archivos a procesar
files = {
    "ATP": os.path.join(input_folder, "atp_matches_ready.csv"),
    "WTA": os.path.join(input_folder, "wta_matches_ready.csv")
}

# Torneos Grand Slam
GRAND_SLAMS = ['Australian Open', 'French Open', 'Wimbledon', 'US Open']

# Función para calcular la importancia de la ronda
def calcular_importancia_ronda(ronda):
    ronda = ronda.lower()
    if "final" in ronda and "semi" not in ronda:
        return 5  # Final
    elif "semi" in ronda:
        return 4  # Semifinal
    elif "quarter" in ronda or "4th round" in ronda:
        return 3  # Cuartos
    elif "3rd round" in ronda:
        return 2  # Tercera Ronda
    elif "2nd round" in ronda:
        return 1  # Segunda Ronda
    elif "1st round" in ronda:
        return 0  # Primera Ronda
    else:
        return -1  # Otro (clasificatorias, retirados, walkover, etc.)

# Función para enriquecer
def enriquecer_dataset(df, tour_name):
    print(f"\n🔧 Enriqueciendo {tour_name}...")

    # Agregar si el torneo es Grand Slam
    df['is_grand_slam'] = df['Tournament'].apply(lambda x: 1 if x in GRAND_SLAMS else 0)

    # Agregar importancia de la ronda
    df['round_importance'] = df['Round'].apply(calcular_importancia_ronda)

    # Opcional: eliminar filas raras con round_importance -1
    df = df[df['round_importance'] >= 0]

    # Resetear índice
    df = df.reset_index(drop=True)

    return df

# Procesar ambos datasets
for tour, filepath in files.items():
    print(f"📂 Procesando {tour}...")
    df = pd.read_csv(filepath)

    # Enriquecer
    df_enriched = enriquecer_dataset(df, tour)

    # Guardar
    output_path = os.path.join(output_folder, f"{tour.lower()}_matches_enriched.csv")
    df_enriched.to_csv(output_path, index=False)
    print(f"✅ {tour} enriquecido y guardado en {output_path}")

print("\n🏁 Feature Engineering terminado.")
