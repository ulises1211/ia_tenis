# 🎾 Proyecto TENIS

Este proyecto tiene como objetivo analizar datos de partidos de tenis, construir modelos predictivos y realizar predicciones basadas en características clave de los jugadores y los partidos. El proyecto abarca desde la descarga y procesamiento de datos hasta la creación de modelos de aprendizaje automático.

---

## 📁 Estructura del Proyecto

```
tenis_project/
│
├── raw/                          # Datos crudos descargados
├── processed_bronze/            # Datos limpios (nivel Bronze)
├── processed_silver/            # Datos enriquecidos (nivel Silver)
├── modelos/                     # Modelos entrenados
├── scripts/
│   ├── 1_raw_descargar_datasets.py
│   ├── 2_tennis_bronze.py
│   ├── 3_tennis_silver.py
│   ├── 4_tennis_silver_enriched.py
│   ├── 5_atp_modelo_puro_enriched.py
│   ├── 5_wta_modelo_puro_enriched.py
│   ├── 6_atp_predictor_modelo_tenis.py
│   ├── 6_wta_predictor_modelo_tenis.py
│   └── mini_EDA.py
├── requirements.txt
├── notas.txt
└── README.md
```

---

## 🛠️ Requisitos

Antes de ejecutar el proyecto, asegúrate de contar con:

- Python 3.8 o superior
- Instalación de dependencias:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn joblib requests beautifulsoup4 openpyxl xlrd
```

---

## 🚀 Flujo del Proyecto

1. **Descarga de Datos Crudos**
   - Ejecuta `1_raw_descargar_datasets.py`
   - Guarda los datos en la carpeta `raw/`

2. **Procesamiento Inicial (Bronze)**
   - Ejecuta `2_tennis_bronze.py` para combinar y limpiar los datos
   - Salida: carpeta `processed_bronze/`

3. **Procesamiento Intermedio (Silver)**
   - Ejecuta `3_tennis_silver.py` y `4_tennis_silver_enriched.py`
   - Salida: carpeta `processed_silver/`

4. **Entrenamiento de Modelos**
   - ATP: `5_atp_modelo_puro_enriched.py`
   - WTA: `5_wta_modelo_puro_enriched.py`
   - Modelos guardados en `modelos/`

5. **Predicción**
   - ATP: `6_atp_predictor_modelo_tenis.py`
   - WTA: `6_wta_predictor_modelo_tenis.py`

6. **Análisis Exploratorio (EDA)**
   - Ejecuta `mini_EDA.py` para visualizar los datos procesados

---

## 🧠 Modelos Entrenados

### Logistic Regression

- **Características**:
  - `rank_diff`, `points_diff`
  - `surface_Hard`, `surface_Clay`, `surface_Grass`
  - `is_grand_slam`, `round_importance`
- **Evaluación**:
  - Accuracy aproximado: ~85%

### Random Forest

- **Características**: mismas que Logistic Regression
- **Evaluación**:
  - Accuracy aproximado: ~90%

---

## 📝 Notas Adicionales

- Los datos provienen de [Tennis Data](http://www.tennis-data.co.uk/)
- Consulta `notas.txt` para más detalles sobre las columnas y su significado

---

## 🤝 Contribuciones

¿Quieres contribuir? Abre un issue o haz un pull request. ¡Toda ayuda es bienvenida!

---

## 📜 Licencia

Este proyecto es de uso personal y educativo. Para uso comercial, contacta al autor.

---

## ✍️ Autor

Jose Ulises Martinez Jimenez  
Proyecto desarrollado como parte de un análisis de datos y modelado predictivo en tenis.
