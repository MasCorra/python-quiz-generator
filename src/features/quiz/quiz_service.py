import os
from openai import OpenAI
from src.features.quiz.quiz_models import Question, Quiz

MODEL =os.getenv("OPENAI_MODEL")
SYSTEM_PROMPT = f"""
Genera 10 domande a risposta multipla basate sul testo dell'utente.

## Regole

- Copri i concetti principali senza ripetizioni.
- Distribuisci la difficoltà: 3 facili, 4 medie e 3 difficili.
- Ogni domanda deve avere 4 risposte plausibili, di cui una sola risposta corretta.
- Varia la posizione della risposta corretta.
- Se l'utente fornisce un brano, usa solo informazioni presenti o deducibili dal brano.
- Se l'utente indica un argomento, usa fatti consolidati e pertinenti all'argomento.

### Formato di output

Restituisci un oggetto JSON con il campo questions.
Il campo questions contiene una lista di esattamente 10 domande.

Ogni domanda ha tre campi.
- question contiene il testo della domanda.
- answer contiene una lista di 4 opzioni.
- correct_answer è una stringa che contiene la lettera a, b, c o d a seconda di qual'è la risposta esatta.

Restituisci soltanto l'oggetto JSON."""

USER_PROMPT = """
{text}
"""

client = OpenAI()

def generate_quiz(text: str):
    user_prompt = (
        USER_PROMPT.replace("{text}", text.strip())
    )
    response = client.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=1,
        response_format= Quiz,

    )
    data = response.choices[0].message.parsed
    if data is None:
        raise RuntimeError("La generazione non ha restituito un quiz.")

    for numero, domanda in enumerate(data.questions, start=1):
        domanda.id_question = numero

    return data