from fastapi import Depends, APIRouter
from schemas import PronoCreate, ClassementUtilisateur
from sqlalchemy import desc
from sqlalchemy.orm import Session 
from database import get_db
from models import Prono, Etape, User 
from sqlalchemy.orm import Session  

router = APIRouter()


#nombre de pronos par étape
@router.get("/api/statistiques/pronos/etape/{etape_id}")
def statistiques_pronos_etape(etape_id: int, db: Session = Depends(get_db)):
    count = db.query(Prono).filter(Prono.etape_id == etape_id).count()
    return {"etape_id": etape_id, "nombre_pronos": count}

#classement des utilisateurs par nombre de points 
@router.get("/api/statistiques/classement")
def classement_utilisateurs(db: Session = Depends(get_db)):
    #classement des utilisateurs par nombre de points, on retourne le nom, l'id et le nombre de points
    #on prend les 100 premiers utilisateurs 
    print("Récupération du classement des utilisateurs")
    classement = db.query(User).order_by(desc(User.point)).limit(100).all()
    classement = [
        ClassementUtilisateur(
            id=user.id,
            username=user.username,
            email=user.email,
            point=user.point
        ) for user in classement
    ]
    print(f"Classement récupéré : {len(classement)} utilisateurs", classement)
    return classement 



#mettre à jour les points des utilisateurs
@router.post("/api/attribuer_points/{etape_id}")
def attribuer_points(etape_id: int, db: Session = Depends(get_db)):
    etape = db.query(Etape).filter(Etape.id == etape_id).first()
    if not etape or not etape.vainqueur:
        return {"message": "Étape non trouvée ou vainqueur non défini"}

    # Récupère tous les pronostics pour cette étape
    pronostics = db.query(Prono).filter(Prono.etape_id == etape_id).all()

    for prono in pronostics:
        if prono.coureur_id == etape.vainqueur:
            user = db.query(User).filter(User.id == prono.user_id).first()
            if user:
                user.point += 15  # ou le nombre de points que tu veux
    db.commit()

    return {"message": "Points mis à jour"}