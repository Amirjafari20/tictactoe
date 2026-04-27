
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from BACKEND_NAME_PLACEHOLDER.schema import UserCreate, UserFull
from BACKEND_NAME_PLACEHOLDER.model import User
from BACKEND_NAME_PLACEHOLDER.utils.auth import hash_password, verify_password
from BACKEND_NAME_PLACEHOLDER.utils.jwt import create_access_token
from BACKEND_NAME_PLACEHOLDER.engine import get_engine
from sqlalchemy.orm import sessionmaker



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.user_name == username).first()
    if not user or not user.password_hash:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    from BACKEND_NAME_PLACEHOLDER.utils.jwt import decode_access_token
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return payload["sub"]

def define_routes(app: FastAPI) -> None:

    from BACKEND_NAME_PLACEHOLDER.schema import GameCreate, GameFull, MoveCreate, MoveFull
    from BACKEND_NAME_PLACEHOLDER.model import Game, Move
    from BACKEND_NAME_PLACEHOLDER.crud import GameCrud
    from BACKEND_NAME_PLACEHOLDER.service import check_win, check_draw, is_valid_move, apply_move

    def get_gamecrud(db: Session = Depends(get_db)):
        return GameCrud(db)

    @app.post("/games", response_model=GameFull)
    def create_game(game: GameCreate, db: Session = Depends(get_db)):
        crud = GameCrud(db)
        db_game = crud.create_game(game)
        return GameFull(
            id=db_game.id,
            player_x=db_game.player_x,
            player_o=db_game.player_o,
            board=db_game.board,
            current_player=db_game.current_player,
            status=db_game.status,
            winner=db_game.winner,
            move_history=db_game.move_history
        )

    @app.get("/games", response_model=list[GameFull])
    def list_games(db: Session = Depends(get_db)):
        crud = GameCrud(db)
        games = crud.get_games()
        return [GameFull(
            id=g.id,
            player_x=g.player_x,
            player_o=g.player_o,
            board=g.board,
            current_player=g.current_player,
            status=g.status,
            winner=g.winner,
            move_history=g.move_history
        ) for g in games]

    @app.get("/games/{game_id}", response_model=GameFull)
    def get_game(game_id: int, db: Session = Depends(get_db)):
        crud = GameCrud(db)
        g = crud.get_game(game_id)
        if not g:
            raise HTTPException(status_code=404, detail="Game not found")
        return GameFull(
            id=g.id,
            player_x=g.player_x,
            player_o=g.player_o,
            board=g.board,
            current_player=g.current_player,
            status=g.status,
            winner=g.winner,
            move_history=g.move_history
        )

    @app.put("/games/{game_id}/move/{position}", response_model=GameFull)
    def make_move(game_id: int, position: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
        crud = GameCrud(db)
        game = crud.get_game(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        if game.status == "finished":
            raise HTTPException(status_code=400, detail="Game already finished")
        if not is_valid_move(game.board, position-1):
            raise HTTPException(status_code=400, detail="Invalid move: position occupied or out of bounds")
        # Determine player symbol
        if current_user == game.player_x:
            player = "X"
        elif current_user == game.player_o:
            player = "O"
        else:
            raise HTTPException(status_code=403, detail="Not a player in this game")
        if player != game.current_player:
            raise HTTPException(status_code=400, detail="Not your turn")
        # Apply move
        game.board = apply_move(game.board, position-1, player)
        game.move_history = (game.move_history + "," if game.move_history else "") + str(position)
        winner = check_win(game.board)
        if winner:
            game.status = "finished"
            game.winner = winner
        elif check_draw(game.board):
            game.status = "finished"
            game.winner = None
        else:
            game.current_player = "O" if game.current_player == "X" else "X"
            game.status = "in_progress"
        db.commit()
        db.refresh(game)
        return GameFull(
            id=game.id,
            player_x=game.player_x,
            player_o=game.player_o,
            board=game.board,
            current_player=game.current_player,
            status=game.status,
            winner=game.winner,
            move_history=game.move_history
        )


    @app.get("/")
    def get_root():
        return {"message": "TicTacToe API Root"}

    @app.post("/register", response_model=UserFull)
    def register(user: UserCreate, db: Session = Depends(get_db)):
        existing = db.query(User).filter(User.user_name == user.user_name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_pw = hash_password(user.password)
        db_user = User(user_name=user.user_name, password_hash=hashed_pw, entity_id=1)  # TODO: set entity_id properly
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserFull(user_name=db_user.user_name, entity_id=db_user.entity_id, password_hash=db_user.password_hash)

    @app.post("/token")
    def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": user.user_name})
        return {"access_token": access_token, "token_type": "bearer"}

    @app.get("/users/me")
    def read_users_me(current_user: str = Depends(get_current_user)):
        return {"user_name": current_user}
