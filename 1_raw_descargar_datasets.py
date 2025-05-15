import os
import requests
from bs4 import BeautifulSoup
import urllib3

# Desactivar warnings SSL inseguros
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL principal usando HTTP
BASE_URL = "http://www.tennis-data.co.uk/alldata.php"

# Carpeta base
base_output_folder = "./data/raw/"
atp_folder = os.path.join(base_output_folder, "atp")
wta_folder = os.path.join(base_output_folder, "wta")

# Crear carpetas si no existen
os.makedirs(atp_folder, exist_ok=True)
os.makedirs(wta_folder, exist_ok=True)

# Obtener contenido
response = requests.get(BASE_URL)
if response.status_code != 200:
    raise Exception(f"Error al acceder a {BASE_URL}")

soup = BeautifulSoup(response.text, "html.parser")

# Buscar todos los enlaces a archivos .xls o .xlsx
file_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if href.endswith('.xls') or href.endswith('.xlsx'):
        if not href.startswith('http'):
            href = f"http://www.tennis-data.co.uk/{href}"
        file_links.append(href)

print(f"Archivos encontrados: {len(file_links)}")

# Ahora sí vamos a separar ATP y WTA
for idx, url in enumerate(file_links):
    file_name = url.split("/")[-1]

    # Regla de separación ATP y WTA:
    if idx < 26:  # Los primeros 26 archivos son ATP (según inspección de la página actual)
        output_path = os.path.join(atp_folder, file_name)
        current_section = 'ATP'
    else:
        output_path = os.path.join(wta_folder, file_name)
        current_section = 'WTA'

    print(f"[{current_section}] Descargando {file_name}...")

    # Descargar archivo
    try:
        head = requests.head(url, timeout=10)
        if head.status_code == 200:
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(output_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        else:
            print(f"⚠️ Archivo no disponible (status code: {head.status_code}), saltando {file_name}...")
    except Exception as e:
        print(f"⚠️ Error descargando {file_name}: {e}")

print("✅ Descarga completa y organizada por ATP y WTA.")
