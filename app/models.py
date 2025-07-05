from sqlalchemy import create_engine, Column, Integer, String, Column, BigInteger, TIMESTAMP, func 
from database import Base

class Coureur(Base):
    __tablename__ = "Coureurs"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    equipe = Column(String) 

class Etape(Base):
    __tablename__ = "Etapes"
    id = Column(Integer, primary_key=True, index=True)
    lieux = Column(String, index=True)
    distance = Column(Integer) 
    relief = Column(String)
    date = Column(String, index=True)  
    cloture = Column(TIMESTAMP(timezone=True), server_default=func.now())  
    etapefin = Column(TIMESTAMP(timezone=True), server_default=func.now())
    vainqueur = Column(Integer, nullable=True)  


class Prono(Base):
    __tablename__ = "Prono" 

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id = Column(BigInteger, nullable=False)
    coureur_id = Column(BigInteger, nullable=False)
    etape_id = Column(BigInteger, nullable=False)

class User(Base):
    __tablename__ = "Utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    point = Column(Integer, default=0)
    username = Column(String, unique=True, index=True, nullable=False)

