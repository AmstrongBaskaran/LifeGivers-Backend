from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.schemas.users_schema import UserCreate, UserLogin, UserResponse
from app.core.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

# 1. USER REGISTRATION
@router.post("/", response_model=UserResponse)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    # 1. Register a new user
    # Check if phone number already exists to prevent duplicates
    if db.query(User).filter(User.phone_number == data.phone_number).first():
        raise HTTPException(status_code=400, detail="Phone number already registered")
        
    # Security: Hash the password (encrypt it) so it's not stored as plain text
    hashed_pass = get_password_hash(data.password)
    
    new_user = User(
        fullname=data.fullname,
        phone_number=data.phone_number,
        password=hashed_pass,
        role=data.role # "user" or "admin"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# 2. USER LOGIN (JWT Tracking)
@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    # Find user by phone
    user = db.query(User).filter(User.phone_number == data.phone_number).first()
    
    # Verify both user existence and password match
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect phone number or password")
    
    # Create a secure JWT Access Token
    # This token allows the user to stay logged in without sending password again
    token = create_access_token(data={"sub": str(user.phone_number)})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "fullname": user.fullname,
        "role": user.role
    }


# 3. GET USER INFO
@router.get("/me", response_model=UserResponse)
def get_current_profile(current_user: User = Depends(get_current_user)):
    """ Returns profile of whichever user is logged in """
    return current_user

@router.get("/", response_model=list[UserResponse])
def list_all_users(db: Session = Depends(get_db)):
    """ Simple list of all registered users (Admin only ideally) """
    return db.query(User).all()


# 4. ACCOUNT MANAGEMENT
@router.put("/{user_id}")
def update_profile(user_id: int, data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = data.model_dump()
    # Update password only if a new one is provided
    if "password" in user_data:
        user_data["password"] = get_password_hash(user_data["password"])

    for key, value in user_data.items():
        setattr(user, key, value)
    
    db.commit()
    return {"message": "Update successful"}

@router.delete("/{user_id}")
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
