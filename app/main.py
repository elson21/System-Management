from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.db.session import SessionLocal
from app.db.db_models import(
                        User,
                        Organization,
                        SystemClaim,
                        System
                    )
from app.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_active_user,
    get_current_user_from_cookie,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def db_connect():
    with SessionLocal() as db:
        yield db

@app.get("/")
def main_page(request: Request, db: Session = Depends(db_connect)) -> HTMLResponse:
    # Check if user is authenticated via cookie
    current_user = None
    try:
        current_user = get_current_user_from_cookie(request, db)
    except HTTPException:
        pass  # User not authenticated
    
    # Check if this is an HTMX request
    is_htmx = request.headers.get("HX-Request") == "true"
    
    if is_htmx:
        # Return only the main content for HTMX requests
        return templates.TemplateResponse("index_content.html", {
            "request": request, 
            "user": current_user,
            "is_authenticated": current_user is not None
        })
    else:
        # Return full page for regular requests
        return templates.TemplateResponse("login_.html", {
            "request": request, 
            "user": current_user,
            "is_authenticated": current_user is not None
        })

@app.get("/login")
def login_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin/create-user")
def admin_create_user_page(
    request: Request,
    current_user: User = Depends(get_current_active_user)
) -> HTMLResponse:
    # Check if current user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    
    # Check if this is an HTMX request
    is_htmx = request.headers.get("HX-Request") == "true"
    
    if is_htmx:
        # Return only the admin create user content for HTMX requests
        return templates.TemplateResponse("admin_create_user_content.html", {
            "request": request, 
            "user": current_user
        })
    else:
        # Return full page for regular requests
        return templates.TemplateResponse("admin_create_user.html", {
            "request": request, 
            "user": current_user
        })

@app.post("/api/login")
async def login(
    request: Request,
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(db_connect)
):
    print(f"Login attempt for user: {username}")
    
    user = authenticate_user(db, username, password)
    if not user:
        print(f"Authentication failed for user: {username}")
        # Return login page with error message
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Incorrect email or password"
        })
    
    print(f"Authentication successful for user: {username}")
    
    # Update last login
    user.last_login = datetime.now()
    db.commit()
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    print(f"Generated token for user {username}: {access_token[:20]}...")
    
    # Create response with token in cookie and redirect to dashboard
    response = RedirectResponse(url="/api/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=False  # Set to True in production with HTTPS
    )
    
    return response

@app.get("/logout")
def logout():
    """Logout user by clearing the cookie and redirecting to home."""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    return response

@app.post("/api/admin/create-user")
async def admin_create_user(
    request: Request,
    first_name: str = Form(),
    last_name: str = Form(),
    email: str = Form(),
    password: str = Form(),
    is_admin: bool = Form(False),
    is_active: bool = Form(True),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(db_connect)
):
    # Check if current user is admin (you can modify this logic based on your admin criteria)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create new users"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Get or create organization
    organization = db.query(Organization).first()
    if not organization:
        organization = Organization(name="Default Organization")
        db.add(organization)
        db.commit()
        db.refresh(organization)
    
    # Create new user with hashed password
    hashed_password = get_password_hash(password)
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=hashed_password,
        organization_id=organization.id,
        is_admin=is_admin,
        is_active=is_active
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "User created successfully"}

@app.get("/api/activity")
def get_post(
    request: Request, 
    db: Session = Depends(db_connect),
    current_user: User = Depends(get_current_active_user)
) -> HTMLResponse:
    # see last 10 posts
    claims = db.query(SystemClaim)\
                    .join(User)\
                    .join(System)\
                    .order_by(SystemClaim.claimed_at.desc())\
                    .limit(10)\
                    .all()

    # Check if this is an HTMX request
    is_htmx = request.headers.get("HX-Request") == "true"
    
    if is_htmx:
        # Return only the activity content for HTMX requests
        return templates.TemplateResponse("activity_content.html", {
            "request": request, 
            "claims": claims, 
            "user": current_user
        })
    else:
        # Return full page for regular requests
        return templates.TemplateResponse("activity.html", {
            "request": request, 
            "claims": claims, 
            "user": current_user
        })

@app.get("/api/dashboard")
def get_dashboard(
    request: Request, 
    db: Session = Depends(db_connect),
    current_user: User = Depends(get_current_active_user)
) -> HTMLResponse:
    # Check if this is an HTMX request
    is_htmx = request.headers.get("HX-Request") == "true"
    
    if is_htmx:
        # Return only the dashboard content for HTMX requests
        return templates.TemplateResponse("dashboard_content.html", {
            "request": request, 
            "user": current_user
        })
    else:
        # Return full page for regular requests
        return templates.TemplateResponse("dashboard.html", {
            "request": request, 
            "user": current_user
        })

@app.get("/api/systems")
def get_systems(
    request: Request, 
    db: Session = Depends(db_connect),
    current_user: User = Depends(get_current_active_user)
) -> HTMLResponse:
    systems = db.query(System).all()
    
    # Check if this is an HTMX request
    is_htmx = request.headers.get("HX-Request") == "true"
    
    if is_htmx:
        # Return only the systems content for HTMX requests
        return templates.TemplateResponse("systems_content.html", {
            "request": request, 
            "systems": systems, 
            "user": current_user
        })
    else:
        # Return full page for regular requests
        return templates.TemplateResponse("systems.html", {
            "request": request, 
            "systems": systems, 
            "user": current_user
        })

@app.post("/create-user")
def create_user(
                first_name: str=Form(),
                last_name: str=Form(),
                email: str=Form(),
                password: str=Form()
            ) -> HTMLResponse:
    db = SessionLocal()

    organization = db.query(Organization).first()
    if not organization:
        organization = Organization(name="Test organization")
        db.add(organization)
        db.commit()
        db.refresh(organization)

    # Hash the password before storing
    hashed_password = get_password_hash(password)

    user = User(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password_hash = hashed_password,
        organization_id = organization.id
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created!"}

