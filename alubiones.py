import pdfplumber
import re
import json
import os
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
            "Superficie agrícola con afectación total o perdida": r"Superficie agrícola con afectación total o pérdida \(ha\).*?(\d+)",
            "Animales con afectación": r"Animales con afectación\s+(\d+)",
            "Animales muertos": r"Animales muertos\s+(\d+)"
        }

        for key, pattern in table_patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                data[key] = match.group(1).strip()

    return data

def process_pdfs_in_folder(folder_path, output_json, output_csv):
    all_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file_name)
            print(f"Procesando archivo: {pdf_path}")
            data = extract_data_from_pdf(pdf_path)
            data["Archivo"] = file_name  # Agregar nombre del archivo al registro
            all_data.append(data)
    
    # Guardar en JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    
    # Convertir a CSV
    df = pd.DataFrame(all_data)
    df.to_csv(output_csv, index=False, encoding='utf-8')


# Uso del script
folder_path = "pdf/"  # Carpeta con los PDFs
output_json = "output_data.json"
output_csv = "output_data.csv"

process_pdfs_in_folder(folder_path, output_json, output_csv)
