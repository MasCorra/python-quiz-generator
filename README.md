# Python Quiz Generator

Generate study quizzes from notes, a passage, or a topic. The project combines a FastAPI backend, structured responses from OpenAI, and **Folia**, an Italian-language web interface.

## Features

- Generate a quiz with 10 multiple-choice questions and four options per question.
- Navigate between questions, confirm each answer, and get immediate feedback.
- See a summary of correct, incorrect, and unconfirmed answers.
- Keep notes and progress in the current browser tab using `sessionStorage`.
- Try the built-in photosynthesis quiz by opening [static/app.html](static/app.html) directly in your browser. The demo runs without the API server.

## Run locally

You need **Python 3.15 or later** as specified in [pyproject.toml](pyproject.toml), **uv** to install dependencies, and an OpenAI API key to generate new quizzes.

From the repository root, prepare the configuration file and install the dependencies.

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
uv sync --locked
```

In `.env`, set your API key and the ID of an OpenAI model that supports structured outputs through Chat Completions.

```dotenv
OPENAI_API_KEY="your-api-key"
OPENAI_MODEL="your-model-id"
```

Start the server from PowerShell.

```powershell
$env:PYTHONPATH = "src"
uv run --locked python main.py
```

On macOS or Linux, run `PYTHONPATH=src uv run --locked python main.py`. The router imports the service through `features.quiz`, so Python needs `src` on its module search path. Run the server from the repository root so it can resolve the `static` directory.

- [Folia](http://127.0.0.1:8000/app.html) lets you paste notes, generate a quiz, and take it.
- [Swagger UI](http://127.0.0.1:8000/docs) lets you try the API directly.

When you generate a quiz, the server sends the text you entered to the configured OpenAI model. The browser grades your answers.

## API

`POST /api/quizzes` accepts a JSON request body with a required `text` field.

```json
{
  "text": "La fotosintesi clorofilliana"
}
```

The response contains `quiz.questions`, a list of exactly 10 items. Each item has the following structure.

```json
{
  "id_question": 1,
  "question": "Quale pigmento assorbe la luce nella fotosintesi?",
  "options": {
    "a": "Clorofilla",
    "b": "Emoglobina",
    "c": "Melanina",
    "d": "Cheratina"
  },
  "correct_answer": "a"
}
```

The service assigns each `id_question` sequentially from 1 to 10. The `correct_answer` field identifies the correct option by its key, from `a` to `d`.

## Project structure

| File | Role |
| --- | --- |
| [main.py](main.py) | Loads configuration, registers the router, and serves the frontend using FastAPI and Uvicorn. |
| [quiz_router.py](src/routers/quiz_router.py) | Handles the HTTP request and returns the generated quiz in the `quiz` field. |
| [quiz_service.py](src/features/quiz/quiz_service.py) | Builds the prompt, calls OpenAI with a response schema, and numbers the questions. |
| [quiz_models.py](src/features/quiz/quiz_models.py) | Defines the Pydantic models for requests, responses, questions, and options. |
| [static/app.html](static/app.html) | Contains the Folia interface in HTML, CSS, and JavaScript, including the demo and answer grading. |
| [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock) | Declare and lock the project dependencies. |

The Pydantic schema validates the quiz structure. Question relevance and difficulty distribution depend on the prompt and the model's response.
