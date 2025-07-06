# database/py
from google.oauth2 import service_account
from google.cloud import firestore
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()


key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not key_path:
    raise RuntimeError("Defina GOOGLE_APPLICATION_CREDENTIALS no .env")

key_abspath = Path(__file__).parent.joinpath(key_path).resolve()
if not key_abspath.exists():
    raise FileNotFoundError(f"Chave não encontrada em: {key_abspath}")

creds = service_account.Credentials.from_service_account_file(str(key_abspath))
project_id = creds.project_id
db = firestore.Client(credentials=creds, project=project_id)

if __name__ == "__main__":
    db.collection("teste").document("ping").set({"pong": True})
    doc = db.collection("teste").document("ping").get()
    print("Firestore responde:", doc.to_dict())
