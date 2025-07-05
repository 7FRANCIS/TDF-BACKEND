from fastapi import Depends, APIRouter
from database import get_db
from models import Coureur
from sqlalchemy.orm import Session 


router = APIRouter()
# La liste des coureurs
@router.get("/api/coureurs")
def lire_coureurs(db: Session = Depends(get_db)):
    return db.query(Coureur).all() 

#Lister tous les coureurs d’une équipe
@router.get("/api/coureurs/equipe/{equipe}")
def lister_coureurs_equipe(equipe: str, db: Session = Depends(get_db)):
    return db.query(Coureur).filter(Coureur.equipe == equipe).all()