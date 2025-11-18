from sqladmin import ModelView
from app.users.models import User, Role, Permission

class AdminUser(ModelView, model=User):
    column_list = [c.name for c in User.__table__.c if c.name != 'id'] + [User.role]
    can_create = True
    can_delete = True
    can_update = True

class AdminRole(ModelView, model=Role):
    column_list = [c.name for c in Role.__table__.c if c.name != 'id'] + [Role.users, Role.permissions]    
    can_create = True
    can_delete = True
    can_update = True


class AdminPermission(ModelView, model=Permission):
    column_list = [c.name for c in Permission.__table__.c if c.name != 'id'] + [Permission.roles]
    can_create = True
    can_delete = True
    can_update = True