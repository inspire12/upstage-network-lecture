from typing import Optional, Dict, Any, List
from app.repository.user_repository import UserRepository
from app.core.exceptions import ValidationException, NotFoundError, ConflictError


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def create_user(self, name: str, email: str) -> Dict[str, Any]:
        # Input validation
        if not name or not name.strip():
            raise ValidationException("Name cannot be empty")
        
        if not email or '@' not in email:
            raise ValidationException("Invalid email format")
        
        # Check for duplicate email
        if self.user_repository.user_exists_by_email(email.lower()):
            raise ConflictError(f"User with email {email} already exists")
        
        user_id = self.user_repository.create_user(name.strip(), email.lower())
        created_user = self.user_repository.get_user_by_id(user_id)
        
        if not created_user:
            raise ValidationException("Failed to create user")
        
        return created_user
    
    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        if not email:
            raise ValidationException("Email cannot be empty")
        
        user = self.user_repository.get_user_by_email(email.lower())
        if not user:
            raise NotFoundError(f"User with email {email} not found")
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        if user_id <= 0:
            raise ValidationException("User ID must be positive")
        
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        return user
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        return self.user_repository.get_all_users()
    
    def update_user(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
        # Check if user exists
        existing_user = self.user_repository.get_user_by_id(user_id)
        if not existing_user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        # Validate inputs
        update_data = {}
        if name is not None:
            if not name.strip():
                raise ValidationException("Name cannot be empty")
            update_data['name'] = name.strip()
        
        if email is not None:
            if not email or '@' not in email:
                raise ValidationException("Invalid email format")
            
            # Check for email conflict
            existing_email_user = self.user_repository.get_user_by_email(email.lower())
            if existing_email_user and existing_email_user['id'] != user_id:
                raise ConflictError(f"Email {email} is already in use")
            
            update_data['email'] = email.lower()
        
        # Update if there's data to update
        if update_data:
            success = self.user_repository.update_user(user_id, **update_data)
            if not success:
                raise ValidationException("Failed to update user")
        
        # Return updated user
        updated_user = self.user_repository.get_user_by_id(user_id)
        if not updated_user:
            raise ValidationException("User not found after update")
        
        return updated_user
    
    def delete_user_by_email(self, email: str) -> None:
        if not email:
            raise ValidationException("Email cannot be empty")
        
        user = self.user_repository.get_user_by_email(email.lower())
        if not user:
            raise NotFoundError(f"User with email {email} not found")
        
        success = self.user_repository.delete_user_by_email(email.lower())
        if not success:
            raise ValidationException("Failed to delete user")

    def delete_user_by_id(self, user_id: int) -> None:
        if user_id <= 0:
            raise ValidationException("User ID must be positive")
        
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")
        
        success = self.user_repository.delete_user_by_id(user_id)
        if not success:
            raise ValidationException("Failed to delete user")
