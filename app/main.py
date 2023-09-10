import sys
sys.path.append('.')
from src.db.users_actions import create_user
from src.db.models import UsersBase
from src.db.database import sessionLocal

db = sessionLocal()
new_user = UsersBase(name="oscar",
                     last_name="rodriguez",
                     email="orodriguez@mail.com",
                     password="880106abcde",
                     rol_id=1)

create_user(db=db,user=new_user)

