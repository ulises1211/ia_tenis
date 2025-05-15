import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuración general
data_processed_folder = "./data/processed/"

# Archivos a analizar
files = {
    "ATP": os.path.join(data_processed_folder, "atp_matches.csv"),
    "WTA": os.path.join(data_processed_folder, "wta_matches.csv")
}

# Función para realizar el EDA
def mini_eda(df, tour_name):
    print(f"\n🎾 Análisis para {tour_name} 🎾")

    # Número total de partidos
    print(f"- Total de partidos: {len(df)}")

    # Año de partidos
    df['Year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
    partidos_por_anio = df['Year'].value_counts().sort_index()
    print("\n- Partidos por año:")
    print(partidos_por_anio)

    # Torneos principales
    print("\n- Top 10 torneos con más partidos:")
    print(df['Tournament'].value_counts().head(10))

    # Distribución de superficie
    print("\n- Distribución de superficies:")
    print(df['Surface'].value_counts())

    # Cuotas de apuestas
    print("\n- Resumen estadístico de cuotas (AvgW - Ganador, AvgL - Perdedor):")
    if 'AvgW' in df.columns and 'AvgL' in df.columns:
        print(df[['AvgW', 'AvgL']].describe())
    else:
        print("⚠️ No se encontraron columnas de cuotas promedio.")

    # Datos nulos
    print("\n- Porcentaje de valores nulos por columna:")
    print((df.isnull().mean() * 100).round(2).sort_values(ascending=False))

    # Opcional: gráficos
    partidos_por_anio.plot(kind='bar', figsize=(12,6), title=f"{tour_name}: Partidos por año")
    plt.xlabel("Año")
    plt.ylabel("Cantidad de partidos")
    plt.show()

    df['Surface'].value_counts().plot(kind='pie', autopct='%1.1f%%', figsize=(6,6), title=f"{tour_name}: Distribución de superficies")
    plt.ylabel('')
    plt.show()

# Ejecutar EDA para ATP y WTA
for tour, filepath in files.items():
    print(f"📂 Cargando {tour}...")
    df = pd.read_csv(filepath)
    mini_eda(df, tour)
