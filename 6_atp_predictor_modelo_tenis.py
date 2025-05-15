# archivo: predictor_modelo_tenis.py

import pandas as pd
import joblib

# ----------------------
# Cargar modelos
# ----------------------
def cargar_modelos():
    print("🔹 Cargando modelos entrenados...")
    logistic_model = joblib.load("./modelos/logistic_model_tenis.joblib")
    #logistic_model = joblib.load("./modelos/wta_logistic_model_tenis.joblib")
    random_forest_model = joblib.load("./modelos/random_forest_model_tenis.joblib")
    #random_forest_model = joblib.load("./modelos/wta_random_forest_model_tenis.joblib")
    return logistic_model, random_forest_model

# ----------------------
# Buscar diferencia de ranking y puntos
# ----------------------
def buscar_diferencias(df_historial, player1, player2):
    # Buscar el último partido de player1
    player1_matches = df_historial[
        (df_historial['Winner'] == player1) | (df_historial['Loser'] == player1)
    ]
    player1_matches = player1_matches.sort_values('Date', ascending=False)

    # Buscar el último partido de player2
    player2_matches = df_historial[
        (df_historial['Winner'] == player2) | (df_historial['Loser'] == player2)
    ]
    player2_matches = player2_matches.sort_values('Date', ascending=False)

    if player1_matches.empty:
        print(f"⚠️ No se encontró historial para {player1}.")
        return None, None
    if player2_matches.empty:
        print(f"⚠️ No se encontró historial para {player2}.")
        return None, None

    # Obtener últimos datos de ranking y puntos
    last_p1 = player1_matches.iloc[0]
    last_p2 = player2_matches.iloc[0]

    # Elegir si el jugador fue Winner o Loser para extraer sus valores
    p1_rank = last_p1['WRank'] if last_p1['Winner'] == player1 else last_p1['LRank']
    p1_pts = last_p1['WPts'] if last_p1['Winner'] == player1 else last_p1['LPts']

    p2_rank = last_p2['WRank'] if last_p2['Winner'] == player2 else last_p2['LRank']
    p2_pts = last_p2['WPts'] if last_p2['Winner'] == player2 else last_p2['LPts']

    # Calcular diferencias
    rank_diff = p1_rank - p2_rank
    points_diff = p1_pts - p2_pts

    return rank_diff, points_diff


# ----------------------
# Función de predicción
# ----------------------
def predecir(modelo, rank_diff, points_diff, round_name, surface):
    # Mapa de importancia de ronda
    round_importance_mapping = {
        "Final": 1.0,
        "Semi-Final": 0.8,
        "Quarter-Final": 0.6,
        "Round of 16": 0.4,
        "Round of 32": 0.2,
        "First Round": 0.1
    }
    round_importance = round_importance_mapping.get(round_name, 0.1)

    # Crear base
    input_data = {
        'rank_diff': rank_diff,
        'points_diff': points_diff,
        'surface_Hard': 0,
        'surface_Clay': 0,
        'surface_Grass': 0,
        'is_grand_slam': 0,  # Asumimos que no es Grand Slam salvo que modifiquemos más adelante
        'round_importance': round_importance
    }

    # Activar la superficie correspondiente || Pucinelli de Almeida M. || Rodriguez M.
    if surface == "Hard":
        input_data['surface_Hard'] = 1
    elif surface == "Clay":
        input_data['surface_Clay'] = 1
    elif surface == "Grass":
        input_data['surface_Grass'] = 1
    else:
        print("⚠️ Superficie no reconocida, se asumirá 'Hard' por defecto.")
        input_data['surface_Hard'] = 1

    # Convertir a DataFrame
    input_data = pd.DataFrame([input_data])

    # Asegurar orden de columnas
    columnas_ordenadas = ['rank_diff', 'points_diff', 'surface_Hard', 'surface_Clay', 'surface_Grass', 'is_grand_slam', 'round_importance']
    input_data = input_data[columnas_ordenadas]

    # Hacer predicción
    return modelo.predict(input_data)[0]


# ----------------------
# Ejecución principal
# ----------------------
if __name__ == "__main__":
    # Cargar modelos
    logistic_model, random_forest_model = cargar_modelos()

    # Cargar historial de partidos
    historial_path = "./data/processed_silver_enriched/atp_matches_enriched.csv"
    #historial_path = "./data/processed_silver_enriched/wta_matches_enriched.csv"
    df_historial = pd.read_csv(historial_path)

    # Input de usuario
    print("\n🎾 Ingrese los datos del partido:")

    player1 = input("Nombre del Jugador 1 (Ej: Enqvist T.): ").strip()
    player2 = input("Nombre del Jugador 2 (Ej: Clement A.): ").strip()

    # Buscar diferencias automáticamente
    rank_diff, points_diff = buscar_diferencias(df_historial, player1, player2)

    if rank_diff is None or points_diff is None:
        print("❌ No se puede hacer la predicción sin datos de historial.")
        exit()
    
    # NUEVO: Verificar que no haya NaN
    if pd.isna(rank_diff) or pd.isna(points_diff):
        print("❌ Los datos de diferencia de ranking o puntos contienen NaN. No se puede hacer la predicción.")
        exit()
    
    print(f"ℹ️ Detalle: rank_diff={rank_diff}, points_diff={points_diff}")

    # Resto del input
    round_name = input("Nombre de la ronda (Ej: Final, Semi-Final, Quarter-Final, Round of 16, etc.): ").strip()
    surface = input("Superficie (Hard, Clay, Grass): ").strip()

    print("\n🔮 Realizando predicciones...\n")

    # Predicción Logistic Regression
    pred_lr = predecir(logistic_model, rank_diff, points_diff, round_name, surface)
    # Predicción Random Forest
    pred_rf = predecir(random_forest_model, rank_diff, points_diff, round_name, surface)

    # Mostrar resultados
    ganador_lr = player1 if pred_lr == 1 else player2
    ganador_rf = player1 if pred_rf == 1 else player2

    print(f"📈 Logistic Regression predice que ganará: **{ganador_lr}**")
    print(f"🌳 Random Forest Mejorado predice que ganará: **{ganador_rf}**")
