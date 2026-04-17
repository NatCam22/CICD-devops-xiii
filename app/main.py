from fastapi import FastAPI
import random

app = FastAPI(title="FastAPI CI/CD Jueguitos", version="1.0.0")
games = {}


@app.get("/")
def read_root():
    return {"message": "Mensaje de inicio, CI/CD!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/game/ppt/{eleccion}")
def piedra_papel_tijeras(eleccion: str):
    optiones = ["piedra", "papel", "tijeras"]
    if eleccion not in optiones:
        return {"error": "Elección inválida. Use piedra, papel o tijeras"}

    computer = random.choice(optiones)

    if eleccion == computer:
        resultado = "empate"
    elif (
        (eleccion == "piedra" and computer == "tijeras")
        or (eleccion == "papel" and computer == "piedra")
        or (eleccion == "tijeras" and computer == "papel")
    ):
        resultado = "ganas"
    else:
        resultado = "pierdes"

    return {"tu_eleccion": eleccion, 
        "computador": computer, 
        "resultado": resultado}


@app.get("/game/number/start")
def elegir_numero():
    game_id = str(random.randint(1000, 9999))
    secret = random.randint(1, 100)
    games[game_id] = secret
    return {"game_id": game_id, "hint": "Adivina un número entre 1 y 100"}


@app.get("/game/number/guess/{game_id}/{guess}")
def adivinar_numero(game_id: str, guess: int):
    if game_id not in games:
        return {"error": "No se encontró el juego con ese id"}

    secret = games[game_id]

    if guess < secret:
        return {"resultado": "mayor"}
    elif guess > secret:
        return {"resultado": "menor"}
    else:
        del games[game_id]
        return {"resultado": "correcto!"}


@app.get("/game/dice/{num_dice}")
def girar_dados(num_dice: int):
    if num_dice < 1 or num_dice > 5:
        return {"error": "Solo puedes elegir entre 1 y 5 dados"}

    rolls = [random.randint(1, 6) for _ in range(num_dice)]
    return {"rolls": rolls, "total": sum(rolls)}
