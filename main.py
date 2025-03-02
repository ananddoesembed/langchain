import os

from dotenv import load_dotenv
from pydantic import SecretStr
from ui import ui

load_dotenv()

KEY = SecretStr(os.getenv("KEY"))
if KEY is None:
    KEY = ""



if __name__ == "__main__":
    print("Hello, World!")
    demo = ui()
    demo.launch()