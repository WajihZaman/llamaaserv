from pathlib import Path
from chromadb.config import Settings
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

collection_name = "about_CAM"

BASE_DIR = Path(__file__).resolve().parents[1]  # CAM/
DB_dir = BASE_DIR / "central" / "database"  # database directory
DB_PATH = (
    BASE_DIR / "central" / "database" / "vectordb"
).as_posix()  #  chroma database directory

connectionstring = os.getenv("SQL_DB")
url = os.getenv("url", "http://localhost:5001/v1/chat/completions")

# url="http://localhost:5001/v1/chat/completions"


chromaclient = chromadb.PersistentClient(
    path=DB_PATH,
    settings=Settings(allow_reset=True),  # Must be True to use reset()
)
