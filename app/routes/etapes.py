from fastapi import Depends, APIRouter
from schemas import PronoCreate
from sqlalchemy.orm import Session 
from database import get_db
from models import Prono, Etape
from sqlalchemy.orm import Session 
from datetime import datetime


router = APIRouter()

#Lister toutes les étapes
@router.get("/api/etapes")
def lister_etapes(db: Session = Depends(get_db)):
    return db.query(Etape).all() 


#Récupérer l'étape en fonction du time
@router.get("/api/current_etape")
def get_etape(db: Session = Depends(get_db)):
    now = datetime.now()  
    etape = db.query(Etape).filter(Etape.cloture >= now).order_by(Etape.cloture.asc()).first()
    if etape:
        print(etape.cloture)
        print(etape)
        return etape
    return None