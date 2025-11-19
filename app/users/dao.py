from fastapi import HTTPException
import uuid
from app.database import async_session_maker
from app.users.models import User, Role, RoleEnum
from sqlalchemy import insert, select, update

class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
        
    @classmethod
    async def find_by_id(cls, model_id: uuid.UUID):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.unique().scalar_one_or_none()
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.unique().scalars().all()
    
    @classmethod
    async def update_data(cls, model_id: uuid.UUID, **data):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == model_id).values(**data)
            await session.execute(query)
            await session.commit()
        
class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def add_user_with_role(cls, user_data):
        async with async_session_maker() as session:
            user_role = await RoleDAO.find_one_or_none(name=RoleEnum.USER)
            if not user_role:
                raise HTTPException(status_code=500, detail='SOMETHING WRONG WITH DEFOULT USER ROLE')
            user_data['role_id'] = user_role.id
            await cls.add(**user_data)
            user = await UserDAO.find_one_or_none(email=user_data['email'])
            if not user:
                raise HTTPException(status_code=500, detail="USER CREATION FAILED")
            user.role = user_role
            session.add(user)
            await session.commit()
    
    @classmethod
    async def soft_delete_user(cls, user_id: uuid.UUID):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == user_id).values(is_active=False)
            await session.execute(query)
            await session.commit()

                   

class RoleDAO(BaseDAO):
    model = Role