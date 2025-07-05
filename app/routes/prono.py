from fastapi import  Depends, APIRouter
from schemas import PronoCreate
from sqlalchemy.orm import Session 
from database import get_db
from models import Coureur, Prono, Etape
from sqlalchemy.orm import Session
from datetime import datetime
import pytz 


router = APIRouter()

#ajouter un prono
@router.post("/api/pronos")
def creer_prono(prono: PronoCreate, db: Session = Depends(get_db)):
    print("Tentative de création d'un prono :", prono)
    if prono_etape_user(prono.user_id, prono.etape_id, db):
        # si l'utilisateur a déjà un prono pour cette étape, on le modifie
        existing_prono = db.query(Prono).filter(Prono.user_id == prono.user_id, Prono.etape_id == prono.etape_id).first()
        if existing_prono:
            existing_prono.coureur_id = prono.coureur_id
            db.commit()
            db.refresh(existing_prono)
            print(f"Prono modifié : {existing_prono}")
            return existing_prono

    if not validity_cloture(prono.etape_id, db):
        return {"error": "Les pronostics pour cette étape sont clôturés."}
   
    db_prono = Prono(
        user_id=prono.user_id,
        coureur_id=prono.coureur_id,
        etape_id=prono.etape_id
    )
    db.add(db_prono)
    db.commit()
    db.refresh(db_prono)
    print(f"Prono créé : {db_prono}")
    return db_prono 

#retrouver le prono d'un utilisateur pour une étape donnée
@router.get("/api/pronos/{user_id}/{etape_id}")
def prono_etape_user(user_id: int, etape_id: int, db: Session = Depends(get_db)):
    result = db.query(Prono).filter(Prono.user_id == user_id, Prono.etape_id == etape_id).all()
    print(f"Recherche du prono pour l'utilisateur {user_id} sur l'étape {etape_id}: {result}")
    if not result:
        return False 
    
    coureur_id = result[0].coureur_id
    nom = db.query(Coureur).filter(Coureur.id == coureur_id).first().nom
    return {
        "coureur_id": coureur_id,
        "nom": nom,
        "etape_id": etape_id,
        "user_id": user_id
    }


#supprimer un prono
@router.delete("/api/pronos/{prono_id}")
def supprimer_prono(prono_id: int, db: Session = Depends(get_db)):
    prono = db.query(Prono).filter(Prono.id == prono_id).first()
    if not prono:
        return {"error": "Prono non trouvé"}
    
    db.delete(prono)
    db.commit()
    return {"message": "Prono supprimé avec succès"}

#supprimer tous les pronos 
@router.delete("/api/pronos")
def supprimer_tous_pronos(db: Session = Depends(get_db)):
    db.query(Prono).delete()
    db.commit()
    return {"message": "Tous les pronos ont été supprimés avec succès"}

#modifier un prono 
@router.put("/api/pronos/{prono_id}")
def modifier_prono(prono_id: int, prono: PronoCreate, db: Session = Depends(get_db)):
    existing_prono = db.query(Prono).filter(Prono.id == prono_id).first()
    if not existing_prono:
        return {"error": "Prono non trouvé"}
    
    existing_prono.coureur_id = prono.coureur_id
    existing_prono.etape_id = prono.etape_id
    db.commit()
    db.refresh(existing_prono)
    return existing_prono


#liste des pronos d'un utilisateur
@router.get("/api/pronos/user/{user_id}")
def lister_pronos_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Prono).filter(Prono.user_id == user_id).all()

#liste des pronos d'une étape
@router.get("/api/pronos/etape/{etape_id}")
def lister_pronos_etape(etape_id: int, db: Session = Depends(get_db)):
    return db.query(Prono).filter(Prono.etape_id == etape_id).all()



#Récupérer un prono par son ID
@router.get("/api/pronos/{prono_id}")
def recuperer_prono(prono_id: int, db: Session = Depends(get_db)):
    prono = db.query(Prono).filter(Prono.id == prono_id).first()
    if not prono:
        return {"error": "Prono non trouvé"}
    return prono

#Lister tous les pronos
@router.get("/api/pronos")
def lister_pronos(db: Session = Depends(get_db)):
    return db.query(Prono).all() 




#Fonctions utilitaires 
#Clôture des pronostics avant le début d'une étape
def validity_cloture(etape_id: int, db: Session = Depends(get_db)):
    etape = db.query(Etape).filter(Etape.id == etape_id).first()
    
    # Vérifier si la date de clôture est passée
    if etape.cloture < datetime.now(pytz.UTC):
        return False
    
    return True
