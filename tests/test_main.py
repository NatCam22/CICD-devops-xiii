from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app, games

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Mensaje de inicio, CI/CD!"}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- piedra papel tijeras ---

def test_ppt_win():
    with patch("app.main.random.choice", return_value="tijeras"):
        response = client.get("/game/ppt/piedra")
        assert response.status_code == 200
        assert response.json()["resultado"] == "ganas"


def test_ppt_lose():
    with patch("app.main.random.choice", return_value="papel"):
        response = client.get("/game/ppt/piedra")
        assert response.status_code == 200
        assert response.json()["resultado"] == "pierdes"


def test_ppt_tie():
    with patch("app.main.random.choice", return_value="piedra"):
        response = client.get("/game/ppt/piedra")
        assert response.status_code == 200
        assert response.json()["resultado"] == "empate"


def test_ppt_invalid_choice():
    response = client.get("/game/ppt/banana")
    assert response.status_code == 200
    assert "error" in response.json()


# --- Guess the number ---

def test_start_number_game():
    with patch("app.main.random.randint", side_effect=[1234, 42]):
        response = client.get("/game/number/start")
        assert response.status_code == 200
        data = response.json()
        assert data["game_id"] == "1234"
        assert "hint" in data


def test_guess_too_low():
    games["9999"] = 50
    response = client.get("/game/number/guess/9999/30")
    assert response.json()["resultado"] == "mayor"


def test_guess_too_high():
    games["9999"] = 50
    response = client.get("/game/number/guess/9999/80")
    assert response.json()["resultado"] == "menor"


def test_guess_correct():
    games["9999"] = 50
    response = client.get("/game/number/guess/9999/50")
    assert response.json()["resultado"] == "correcto!"
    assert "9999" not in games


def test_guess_game_not_found():
    response = client.get("/game/number/guess/0000/50")
    assert "error" in response.json()


# --- Dice ---

def test_roll_dice():
    with patch("app.main.random.randint", return_value=4):
        response = client.get("/game/dice/3")
        assert response.status_code == 200
        data = response.json()
        assert data["rolls"] == [4, 4, 4]
        assert data["total"] == 12


def test_roll_dice_invalid():
    response = client.get("/game/dice/0")
    assert "error" in response.json()

    response = client.get("/game/dice/11")
    assert "error" in response.json()
