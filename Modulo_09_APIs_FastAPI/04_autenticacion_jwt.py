"""
Módulo 9.4 - Autenticación JWT

Implementación completa de autenticación con JSON Web Tokens (JWT),
hash de passwords, OAuth2 con Password Bearer, y protección de endpoints.

Para ejecutar:
    uvicorn 04_autenticacion_jwt:app --reload
    
Instalar dependencias:
    pip install python-jose[cryptography] passlib[bcrypt]
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List, Annotated

# =============================================================================
# Configuración
# =============================================================================

# Clave secreta para firmar JWT (en producción: variable de entorno)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Context para hash de passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(title="Autenticación JWT", version="1.0.0")


# =============================================================================
# Schemas
# =============================================================================

class Token(BaseModel):
    """Schema de respuesta de token."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos dentro del token JWT."""
    username: Optional[str] = None
    user_id: Optional[int] = None


class UserRegister(BaseModel):
    """Schema para registro de usuario."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str
    password: str = Field(..., min_length=8)


class UserInDB(BaseModel):
    """Usuario en la base de datos (con password hasheado)."""
    id: int
    username: str
    email: EmailStr
    full_name: str
    hashed_password: str
    disabled: bool = False
    is_admin: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


class UserResponse(BaseModel):
    """Schema de respuesta (sin password)."""
    id: int
    username: str
    email: EmailStr
    full_name: str
    disabled: bool
    is_admin: bool
    created_at: datetime


# =============================================================================
# Base de Datos Simulada
# =============================================================================

# En producción: usar base de datos real
fake_users_db = []
user_id_counter = 1


# =============================================================================
# Utilidades de Password
# =============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar password contra hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashear password."""
    return pwd_context.hash(password)


print("=== Ejemplo 1: Password Hashing ===")
print(f"Password original: 'secretpassword'")
print(f"Password hasheado: {get_password_hash('secretpassword')[:50]}...")
print(f"Verificación: {verify_password('secretpassword', get_password_hash('secretpassword'))}\n")


# =============================================================================
# Utilidades de JWT
# =============================================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crear JWT access token.
    
    Args:
        data: Dict con datos a incluir en token (ej: {"sub": "username"})
        expires_delta: Tiempo de expiración (default: 30 min)
    
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Firmar token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """
    Decodificar y verificar JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        TokenData con información del usuario
    
    Raises:
        HTTPException: Si token es inválido o expirado
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username, user_id=user_id)
        
    except JWTError:
        raise credentials_exception
    
    return token_data


print("=== Ejemplo 2: JWT Token ===")
sample_token = create_access_token(data={"sub": "testuser", "user_id": 1})
print(f"Token generado: {sample_token[:50]}...")
print(f"Token decodificado: {decode_access_token(sample_token)}\n")


# =============================================================================
# Funciones de Base de Datos
# =============================================================================

def get_user_by_username(username: str) -> Optional[UserInDB]:
    """Obtener usuario por username."""
    for user in fake_users_db:
        if user.username == username:
            return user
    return None


def get_user_by_id(user_id: int) -> Optional[UserInDB]:
    """Obtener usuario por ID."""
    for user in fake_users_db:
        if user.id == user_id:
            return user
    return None


def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Obtener usuario por email."""
    for user in fake_users_db:
        if user.email == email:
            return user
    return None


# =============================================================================
# Dependencias de Autenticación
# =============================================================================

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """
    Dependencia: Obtener usuario actual del JWT token.
    
    Esta dependencia:
    1. Extrae token del header Authorization: Bearer <token>
    2. Decodifica y valida el token
    3. Obtiene usuario de la DB
    4. Devuelve el usuario
    
    Si algo falla, lanza 401 Unauthorized.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decodificar token
    token_data = decode_access_token(token)
    
    # Obtener usuario de DB
    user = get_user_by_username(token_data.username)
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    """
    Dependencia: Verificar que usuario esté activo.
    
    Dependencia anidada: requiere get_current_user primero.
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
) -> UserInDB:
    """
    Dependencia: Verificar que usuario sea admin.
    
    Cadena de dependencias:
    get_current_admin_user → get_current_active_user → get_current_user
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


# Type hints para dependencias (más clean)
CurrentUser = Annotated[UserInDB, Depends(get_current_active_user)]
AdminUser = Annotated[UserInDB, Depends(get_current_admin_user)]


# =============================================================================
# Endpoints de Autenticación
# =============================================================================

@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Registrar nuevo usuario.
    
    Password se hashea antes de guardar.
    """
    global user_id_counter
    
    # Validar que username no exista
    if get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Validar que email no exista
    if get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Crear usuario
    user = UserInDB(
        id=user_id_counter,
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        disabled=False,
        is_admin=False
    )
    
    fake_users_db.append(user)
    user_id_counter += 1
    
    return user


@app.post("/auth/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login con username y password.
    
    Devuelve JWT access token.
    
    OAuth2PasswordRequestForm proporciona:
    - username
    - password
    - scope (opcional)
    """
    # Obtener usuario
    user = get_user_by_username(form_data.username)
    
    # Validar credenciales
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que usuario esté activo
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Crear access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# =============================================================================
# Endpoints Protegidos
# =============================================================================

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: CurrentUser):
    """
    Obtener información del usuario actual.
    
    Requiere autenticación (token JWT en header).
    """
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: CurrentUser):
    """
    Obtener items del usuario actual.
    
    Endpoint protegido: requiere autenticación.
    """
    return {
        "items": [
            {"id": 1, "owner": current_user.username},
            {"id": 2, "owner": current_user.username}
        ]
    }


@app.put("/users/me", response_model=UserResponse)
async def update_user_me(
    full_name: str,
    current_user: CurrentUser
):
    """
    Actualizar información del usuario actual.
    
    Solo el usuario puede actualizar su propia información.
    """
    current_user.full_name = full_name
    return current_user


# =============================================================================
# Endpoints de Admin
# =============================================================================

@app.get("/admin/users", response_model=List[UserResponse])
async def list_all_users(admin: AdminUser):
    """
    Listar todos los usuarios.
    
    Solo accesible por usuarios admin.
    """
    return fake_users_db


@app.delete("/admin/users/{user_id}")
async def delete_user(user_id: int, admin: AdminUser):
    """
    Eliminar usuario.
    
    Solo admin puede eliminar usuarios.
    """
    user = get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    fake_users_db.remove(user)
    
    return {"message": f"User {user.username} deleted"}


@app.patch("/admin/users/{user_id}/toggle-admin")
async def toggle_admin_status(user_id: int, admin: AdminUser):
    """
    Cambiar status de admin de un usuario.
    
    Solo admin puede hacer esto.
    """
    user = get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_admin = not user.is_admin
    
    return {
        "message": f"User {user.username} admin status: {user.is_admin}",
        "user": user
    }


# =============================================================================
# Ejemplo: Roles y Permisos Avanzados
# =============================================================================

from enum import Enum


class Role(str, Enum):
    """Roles de usuario."""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class UserWithRole(UserInDB):
    """Usuario con rol."""
    role: Role = Role.USER


def require_role(required_role: Role):
    """
    Dependencia factory: requiere rol específico.
    
    Uso:
        @app.get("/endpoint")
        async def endpoint(user: UserInDB = Depends(require_role(Role.ADMIN))):
            ...
    """
    async def role_checker(current_user: CurrentUser) -> UserInDB:
        # En producción: user.role vendría de DB
        user_role = Role.ADMIN if current_user.is_admin else Role.USER
        
        # Jerarquía de roles
        role_hierarchy = {
            Role.USER: 0,
            Role.MODERATOR: 1,
            Role.ADMIN: 2
        }
        
        if role_hierarchy[user_role] < role_hierarchy[required_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires role: {required_role}"
            )
        
        return current_user
    
    return role_checker


@app.get("/moderator/dashboard")
async def moderator_dashboard(
    user: UserInDB = Depends(require_role(Role.MODERATOR))
):
    """Dashboard de moderador (requiere rol MODERATOR o superior)."""
    return {"message": "Moderator dashboard", "user": user.username}


# =============================================================================
# Endpoint Público (sin autenticación)
# =============================================================================

@app.get("/")
async def root():
    """
    Endpoint público (no requiere autenticación).
    """
    return {
        "message": "API con Autenticación JWT",
        "docs": "/docs",
        "instructions": "1. Registrarse en /auth/register, 2. Login en /auth/login, 3. Usar token en /users/me"
    }


@app.get("/public/info")
async def public_info():
    """Endpoint público."""
    return {
        "message": "This is a public endpoint",
        "users_count": len(fake_users_db)
    }


# =============================================================================
# Seed Data (Usuario de prueba)
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """Crear usuario de prueba al iniciar."""
    global user_id_counter
    
    # Usuario regular
    user1 = UserInDB(
        id=user_id_counter,
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword"),
        disabled=False,
        is_admin=False
    )
    fake_users_db.append(user1)
    user_id_counter += 1
    
    # Usuario admin
    admin = UserInDB(
        id=user_id_counter,
        username="admin",
        email="admin@example.com",
        full_name="Admin User",
        hashed_password=get_password_hash("adminpassword"),
        disabled=False,
        is_admin=True
    )
    fake_users_db.append(admin)
    user_id_counter += 1
    
    print("\n✓ Usuarios de prueba creados:")
    print("  testuser / testpassword (regular)")
    print("  admin / adminpassword (admin)\n")


# =============================================================================
# Instrucciones de Uso
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("AUTENTICACIÓN JWT - MÓDULO 9.4")
    print("=" * 70)
    print("\nPara ejecutar:")
    print("  uvicorn 04_autenticacion_jwt:app --reload")
    print("\nDocumentación:")
    print("  http://localhost:8000/docs")
    print("\nFlujo de Autenticación:")
    print("  1. Registrarse:")
    print("     POST /auth/register")
    print("     Body: {username, email, full_name, password}")
    print("\n  2. Login:")
    print("     POST /auth/login")
    print("     Body: {username, password}")
    print("     → Devuelve access_token")
    print("\n  3. Usar token en endpoints protegidos:")
    print("     GET /users/me")
    print("     Header: Authorization: Bearer <access_token>")
    print("\nUsuarios de prueba:")
    print("  testuser / testpassword (usuario regular)")
    print("  admin / adminpassword (usuario admin)")
    print("\n" + "=" * 70)
    print("💡 En Swagger UI: Click en 'Authorize' y usa username/password")
    print("=" * 70 + "\n")
