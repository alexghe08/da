import requests
import json
import os

# Start the server in background if not already running, but assuming we run this against localhost:8000
API_URL = "http://localhost:8000/generate-document"

def test_generate_contract():
    print("Testing /generate-document for Contract...")

    payload = {
        "template_name": "contract_lucrari.docx",
        "context_data": {
            "nr_contract": "1234/2023",
            "data_contract": "20.10.2023",
            "autoritate_contractanta": "Primăria Municipiului Test",
            "adresa_autoritate": "Str. Principala Nr. 1",
            "contractant": "SC Constructii SRL",
            "adresa_contractant": "Str. Industriilor Nr. 5",
            "titlu_proiect": "Renovare Școală Generală Nr. 1",
            "valoare_contract": "1.500.000",
            "moneda": "RON",
            "durata_luni": "12",
            "garantie_buna_executie_necesara": True,
            "procent_garantie": "10"
        }
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            output_file = "test_contract_output.docx"
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"Success! Document saved to {output_file}")
            # Optional: Check file size > 0
            if os.path.getsize(output_file) > 0:
                print("File is valid (non-empty).")
            else:
                print("Error: File is empty.")
        else:
            print(f"Error: Status {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_generate_contract()
