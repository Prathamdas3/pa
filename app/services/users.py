from app.repository import UserRepo
from app.models import Users,UserRole
from app.schemas import UserCreate
from app.core import AppException, get_logger
from app.utils import hash_password
from uuid import UUID

logger = get_logger(__name__)

class UserService:
        """Service for managing users."""

        def __init__(self, repo: UserRepo):
            self._repo = repo

        async def create_user(self, user_create: UserCreate,role:UserRole) -> Users:
            """Create a new user."""
            existing_user = await self._repo.get_user_by_email(user_create.email)
            if existing_user:
                raise AppException("User with this email already exists.", status_code=401)
            existing_username = await self._repo.get_user_by_username(user_create.username)
            if existing_username:
                raise AppException("Username already taken.", status_code=401)
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

        async def get_user_by_email_no_exception(self, email: str):
            """Get user by email without raising exception (for auth)."""
            user = await self._repo.get_user_by_email(email)
            return user
        
        async def get_user_by_id(self,user_id:UUID):
            """Get user by id."""
            user = await self._repo.get_user_by_id(user_id)
            if not user or not user.is_active:
                raise AppException("User not found.", status_code=404)
            return user
        
        async def update_user(self,user_id:UUID,username:str):
            """Update user username."""
            user = await self.get_user_by_id(user_id)
            if not user:
                raise AppException("User not found.", status_code=404)
            existing = await self._repo.get_user_by_username(username)
            if existing and existing.id != user_id:
                raise AppException("Username already taken.", status_code=401)
            user.username = username
            await self._repo.save(user)
            return user
        
        async def delete_user(self,user_id:UUID):
            """Soft delete user."""
            user = await self.get_user_by_id(user_id)
            if not user:
                raise AppException("User not found.", status_code=404)
            await self._repo.delete(user)

        async def get_all_users(self):
            """Get all users (admin)."""
            logger.debug("Getting all users (admin)")
            users = await self._repo.get_all_users()
            logger.debug(f"Retrieved {len(users)} users")
            return users

        async def get_user_by_id_admin(self, user_id: UUID):
            """Get any user by id (admin)."""
            logger.debug(f"Getting user (admin): user_id={user_id}")
            user = await self._repo.get_user_by_id_no_filter(user_id)
            if not user:
                logger.warning(f"User not found: user_id={user_id}")
                raise AppException("User not found.", status_code=404)
            return user

        async def delete_user_admin(self, user_id: UUID):
            """Delete any user (admin)."""
            logger.debug(f"Deleting user (admin): user_id={user_id}")
            user = await self._repo.get_user_by_id_no_filter(user_id)
            if not user:
                logger.warning(f"User deletion failed: user not found, user_id={user_id}")
                raise AppException("User not found.", status_code=404)
            await self._repo.delete(user)
            logger.info(f"User deleted by admin: id={user_id}")

        async def update_user_role(self, user_id: UUID, role: str):
            """Update user role (admin)."""
            logger.debug(f"Updating user role: user_id={user_id}, role={role}")
            user = await self._repo.get_user_by_id_no_filter(user_id)
            if not user:
                logger.warning(f"Role update failed: user not found, user_id={user_id}")
                raise AppException("User not found.", status_code=404)
            user.role = role
            result = await self._repo.save(user)
            logger.info(f"User role updated: user_id={user_id}, role={role}")
            return result

