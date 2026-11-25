from dotenv import load_dotenv

load_dotenv()

from src.routers.quiz_router import quiz_router
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles


app = FastAPI(
    title="Generatore di quiz",
    description="Permette di generare quiz a partire da un testo",
    version="0.1.0",
)

app.include_router(quiz_router)

app.mount("/", StaticFiles(directory="static"), name="static")

def main():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000
    )


if __name__ == "__main__":
    main()