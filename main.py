from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import authenticate_user, create_access_token, get_current_user, get_password_hash
from database import ContDateBase
from models import users
from schemas import User, UserCreate
from databases import Database

ACCESS_TOKEN_EXPIRE_MINUTES = 10


app: FastAPI = FastAPI()
ContDateBase.get_metadata().create_all(bind=ContDateBase.get_engine())
database: Database = ContDateBase.get_database()


@app.on_event("startup")
async def startup():
    """при запуске приложения подключаем бд"""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """при выключении приложения отключаем бд"""
    await database.disconnect()


@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    """добавляем нового пользователя в бд"""
    hashed_password = get_password_hash(user.password)
    query = users.insert().values(username=user.username, hashed_password=hashed_password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Создаём токен для авторизации пользователя """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """возвращаем пользователю информацию о нём из бд"""
    return current_user


# @app.post("/recognize", response_model=RecognitionResponse)
# async def recognize(image: UploadFile = File(...), location: str = Form(...), description: str = Form(...)):
#     # Здесь должна быть ваша логика распознавания объектов
#
#     model = resnet18()
#
#     # Load the model state dictionary
#     state_dict = torch.load("model_path/my_model_weights.pth")
#
#     # Load the state dictionary into the model
#     model.load_state_dict(state_dict)
#
#     return {"objects": [{"objectId": "object1", "probability": 0.95}]}
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=8000)
