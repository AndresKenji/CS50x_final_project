from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# Local imports
from . helpers import get_current_user
from .. db import users_actions
from .. db.database import get_db
from .. db.models import UsersBase
from .. db.db_models import Users, Roles

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post('/users')
async def create_user(request: Request,response:Response,db: Session = Depends(get_db)):
    print("Trying user creation")
    user, body = get_current_user(request=request, db=db)
    try:
        if user is None:
            return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        if user.rol_id != 1:
            body["msg"] = "Unauthorized user getting back to home page"
            return templates.TemplateResponse("users.html", body)

        formdata = await request.form()
        user = UsersBase(
            name=formdata['name'],
            last_name= formdata['last_name'],
            email=formdata['email'],
            rol_id=formdata['rol'],
            password=formdata['password']
        )
        userdb = users_actions.create_user(db=db,user=user)
        if isinstance(userdb, Users):
            return RedirectResponse(url="/users/users",status_code=status.HTTP_302_FOUND)
        if isinstance(userdb, str):
            body["msg"] = userdb
            return templates.TemplateResponse("users.html", body)
    except Exception as e:
        body["msg"] = str(e)
        return templates.TemplateResponse("users.html", body)

@router.get('/update_user/{id}')
def update_user_page(request: Request, response:Response, id:int, db: Session = Depends(get_db)):
    print("Loading edit user page")
    user, body = get_current_user(request=request, db=db)
    if user is None:
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    if user.rol_id != 1:
        body["msg"] = "Unauthorized user getting back to home page"
        return templates.TemplateResponse("users.html", body)
    edit_user = db.query(Users).filter(Users.id == id).first()
    body["user"] = edit_user

    return templates.TemplateResponse("edit-user.html", body)

@router.post('/update_user/{id}')
async def update_user(request: Request, response:Response, id:int, db: Session = Depends(get_db)):
    print("Editing user page")
    user, body = get_current_user(request=request, db=db)
    if user is None:
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    if user.rol_id != 1:
        body["msg"] = "Unauthorized user getting back to home page"
        return templates.TemplateResponse("home.html", body)
    edit_user = db.query(Users).filter(Users.id == id).first()
    formdata = await request.form()
    edit_user.name = formdata['name']
    edit_user.last_name = formdata['last_name']
    edit_user.email = formdata['email']
    edit_user.password = edit_user.password if formdata['password'] =="" or formdata['password'] is None else  users_actions.Hash.bcrypt(formdata['password'])
    edit_user.rol_id = formdata['rol']
    updated_user = users_actions.update_user(db=db, user=user)
    
    return RedirectResponse(url="/users/users", status_code=status.HTTP_302_FOUND)


@router.get('/delete_user/{id}')
def delete_user(request: Request, response:Response, id:int,db: Session = Depends(get_db)):
    print("Deleting user")
    user, body = get_current_user(request=request, db=db)
    if user is None:
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    if user.rol_id != 1:
        body["msg"] = "Unauthorized user getting back to home page"
        return templates.TemplateResponse("home.html", body)
    dleted_user = users_actions.delete_user(db=db, id=id)
    return RedirectResponse(url="/users/users", status_code=status.HTTP_302_FOUND)


@router.get('/users',response_class=HTMLResponse)
def get_users_page(request: Request,response:Response, db: Session = Depends(get_db)):
    print("loading users page")
    user, body = get_current_user(request=request, db=db)
    if user is None:
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    if user.rol_id != 1:
        print("Unauthorized user getting back to home page")
        return RedirectResponse(url="/home",status_code=status.HTTP_307_TEMPORARY_REDIRECT)
    
    users = db.query(Users.id,Users.name, Users.last_name, Users.email, Roles.name.label('rol'))\
                .join(Roles, Roles.id == Users.rol_id)
    
    body["users"] = users
    
    return templates.TemplateResponse("users.html", body)