from fastapi import FastAPI, Request, Depends, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.security import OAuth2PasswordBearer
from schemas import PronoCreate, UserCreate, UserResponse
from routes import coureurs, etapes, prono, users, statistiques
from jose import JWTError, jwt
import uvicorn
from dotenv import load_dotenv
import os



load_dotenv() 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
DATABASE_URL = os.getenv("DATABASE_URL")

# Security settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



# Create FastAPI app and include routers
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router) 
app.include_router(coureurs.router)
app.include_router(etapes.router)
app.include_router(prono.router)
app.include_router(statistiques.router)


if __name__ == "__main__":
    # http://127.0.0.1:8000/api/coureurs
    uvicorn.run(app, host="0.0.0.0", port=8000)