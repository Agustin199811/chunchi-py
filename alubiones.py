import pdfplumber
import re
import json
import pandas as pd

def extract_data_from_pdf(pdf_path):
    data = {}
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)

        # Imprimir texto extraído para depuración
        print("Texto extraído del PDF:\n", text)

        # Patrón general para campos simples
        patterns = {
            "Fecha y Hora de actualización": r"Fecha y Hora de actualización:\s*(.+)",
            "Fallecidos": r"Fallecidos:\s*(-|\d+)",
            "Heridos": r"Heridos:\s*(-|\d+)",
            "Viviendas destruidas": r"Viviendas destruidas:\s*(-|\d+)",
            "Bien público afectado": r"Bien público afectado:\s*(-|\d+)",
            "Bien público destruido": r"Bien público destruido:\s*(-|\d+)",
            "Puentes afectados": r"Puentes afectados:\s*(-|\d+)",
            "Vías destruidas": r"Vías destruidas:\s*(-|\d+)",
            "Productores afectados por pérdidas agrícolas": r"Productores afectados por pérdidas agrícolas:\s*(-|\d+)",
            "Productores afectados por pérdidas en animales": r"Productores afectados por pérdidas en animales:\s*(-|\d+)"
        }

        # Buscar valores simples
        for key, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                value = match.group(1).strip()
                data[key] = None if value in ["-", ""] else value
            else:
                data[key] = None

        # Capturar valores específicos en tablas o texto contextual
        table_patterns = {
            "Personas afectadas": r"(\d+)\s+personas afectadas",
            "Personas damnificadas": r"(\d+)\s+damnificadas",
            "Viviendas afectadas": r"Viviendas afectadas.*?(\d+)",
            "Superficie agrícola con afectación total o perdida": r"Superficie agrícola.*?(\d+)\s*ha",
            "Animales con afectación": r"Animales con afectación\s+(\d+)",
            "Animales muertos": r"Animales muertos\s+(\d+)"
        }

        for key, pattern in table_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                data[key] = match.group(1).strip()

    return data




def process_pdf_to_json(pdf_path, output_json):
    data = extract_data_from_pdf(pdf_path)
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump([data], f, ensure_ascii=False, indent=4)

def json_to_csv(json_file, output_csv):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False, encoding='utf-8')

# Uso del script
pdf_path = "pdf/Informe-de-Situacion-No-10-Chunchi-01032021.pdf"  
output_json = "output_data.json"
output_csv = "output_data.csv"

process_pdf_to_json(pdf_path, output_json)
json_to_csv(output_json, output_csv)
