from fastapi import Depends, FastAPI,Form, HTTPException
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.db_models import(
                        User,
                        Organization,
                        SystemClaim,
                        System
                    )

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def db_connect():
    with SessionLocal() as db:
        yield db

        
@app.get("/")
def main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})
    


@app.get("/api/activity")
def get_post(request: Request, db: Session=Depends(db_connect)) -> HTMLResponse:

    # see last 10 posts
    claims = db.query(SystemClaim)\
                    .join(User)\
                    .join(System)\
                    .order_by(SystemClaim.claimed_at.desc())\
                    .limit(10)\
                    .all()

    return templates.TemplateResponse("activity.html", {"request": request, "claims": claims})


@app.get("/api/dashboard")
def get_dashboard(request: Request, db: Session=Depends(db_connect)) -> HTMLResponse:

    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/api/systems")
def get_systems(request: Request, db: Session=Depends(db_connect)) -> HTMLResponse:
    systems = db.query(System).all()

    return templates.TemplateResponse("systems.html", {"request": request, "systems": systems})


@app.post("/create-user")
def create_user(
                first_name: str=Form(),
                last_name: str=Form(),
                email: str=Form()
            ) -> HTMLResponse:
    db = SessionLocal()

    organization = db.query(Organization).first()
    if not organization:
        organization = Organization(name="Test organization")
        db.add(organization)
        db.commit()
        db.refresh(organization)

    user = User(
        first_name = first_name,
        last_name = last_name,
        email = email,
        organization_id = organization.id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created!"}