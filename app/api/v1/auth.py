"""
Authentication Router
REST-compliant endpoints for authentication
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import SecurityManager
from app.core.dependencies import AuthDependency
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister, TokenResponse, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    return AuthService.register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login and get access token"""
    user = AuthService.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = SecurityManager.create_access_token(
        data={"sub": user.username, "user_id": str(user.id), "roles": []}
    )
    refresh_token = SecurityManager.create_refresh_token(
        data={"sub": user.username, "user_id": str(user.id), "roles": []}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=900  # 15 minutes
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(AuthDependency.get_current_user)
):
    """Get current authenticated user"""
    return current_user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    payload = SecurityManager.decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    new_access_token = SecurityManager.create_access_token(
        data={"sub": user.username, "user_id": str(user.id), "roles": []}
    )
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=refresh_token,  # Refresh token remains the same
        expires_in=900
    )

