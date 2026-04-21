from app.repository import UserRepo
from app.models import Users,UserRole
from app.schemas import UserCreate
from app.core import AppException
from app.utils import hash_password


class UserService:
        """Service for managing users."""

        def __init__(self, repo: UserRepo):
            self._repo = repo

        async def create_user(self, user_create: UserCreate,role:UserRole) -> Users:
            """Create a new user."""
            existing_user = await self._repo.get_user_by_email(user_create.email)
            if existing_user:
                raise AppException("User with this email already exists.", status_code=401)
            hased_password = hash_password(user_create.password)
            user = Users(
                email=user_create.email,
                role=role.user,
                hashed_password=hased_password,
                username=user_create.username,
                is_active=True,
            )
            await self._repo.save(user)
            return user
        
        async def get_user_by_email(self,email:str):
            """Get user by email."""
            user = await self._repo.get_user_by_email(email)
            if not user or not user.is_active:
                raise AppException("User not found.", status_code=404)
            return user
        
        async def get_user_by_id(self,user_id:str):
            """Get user by id."""
            user = await self._repo.get_user_by_id(user_id)
            if not user or not user.is_active:
                raise AppException("User not found.", status_code=404)
            return user
        
        async def update_user(self,user_id:str,username:str):
            """Update user username."""
            user = await self.get_user_by_id(user_id)
            if not user:
                raise AppException("User not found.", status_code=404)
            user.username = username
            await self._repo.save(user)
            return user
        
        async def delete_user(self,user_id:str):
            """Soft delete user."""
            user = await self.get_user_by_id(user_id)
            if not user:
                raise AppException("User not found.", status_code=404)
            await self._repo.delete(user)   
