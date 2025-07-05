from pydantic import BaseModel, EmailStr

class PronoCreate(BaseModel):
    user_id: int
    coureur_id: int
    etape_id: int


class UserCreate(BaseModel):
    username: str
    email: str
    password: str 


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    point: int

    class Config:
        from_attributes = True


class ClassementUtilisateur(BaseModel):
    id: int
    username: str
    point: int

    class Config:
        from_attributes = True
        


class TokenData(BaseModel): 
    access_token: str
    token_type: str
    user: UserResponse

    class Config:
        from_attributes = True