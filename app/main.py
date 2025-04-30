from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models import User, Project
from app.schemas import UserCreate, UserRead, Token, ProjectCreate, ProjectRead
from app.auth import get_current_user, get_password_hash, create_access_token, check_admin_role
from app.database import get_session, init_db
from datetime import timedelta
from app.config import settings
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    # Check if username already exists
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Validate role
    if user.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Role must be either 'admin' or 'user'")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password, role=user.role)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/projects", response_model=list[ProjectRead])
def read_projects(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    projects = session.exec(select(Project)).all()
    return projects

@app.post("/projects", response_model=ProjectRead)
def create_project(
    project: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(check_admin_role)
):
    db_project = Project(**project.dict(), owner_id=current_user.id)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@app.get("/projects/{project_id}", response_model=ProjectRead)
def read_project(project_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.put("/projects/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    project: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(check_admin_role)
):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    project_data = project.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(check_admin_role)
):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"ok": True}