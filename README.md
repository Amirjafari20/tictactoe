# TicTacToe FastAPI REST API

## Overview
This project implements a FastAPI-based REST API for a TicTacToe game with user authentication, game management, and move logic.

## Features
- User registration and JWT authentication
- Create, list, and retrieve games
- Make moves, check win/draw, and view game history
- OpenAPI/Swagger documentation

## API Documentation
Run the server and visit `/docs` for interactive Swagger UI or `/redoc` for ReDoc.

## Example Endpoints
- `POST /register` — Register a new user
- `POST /token` — Obtain JWT token
- `POST /games` — Create a new game
- `GET /games` — List all games
- `GET /games/{game_id}` — Get game details
- `PUT /games/{game_id}/move/{position}` — Make a move (1–9)

## Running Tests
```bash
pytest test/
```

## Notes
- All game endpoints require authentication (Bearer token)
- See `/docs` for request/response schemas and examples
