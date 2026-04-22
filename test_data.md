# API Documentation & Test Data

This document provides a detailed reference for all available API endpoints, including request bodies, sample responses, and test data.

---

## 🔐 Authentication Endpoints

**Base Path**: `/api/v1/auth`

### 1. User Sign-up
- **URL**: `/sign-up/user`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "username": "testuser",
    "password": "Password123!"
  }
  ```
- **Constraints**:
  - `username`: 3-30 chars, alphanumeric/underscore. Reserved names: `admin`, `root`, `superuser`.
  - `password`: Min 8 chars, must include uppercase, lowercase, digit, and special character.

### 2. Admin Sign-up
- **URL**: `/sign-up/admin`
- **Method**: `POST`
- **Body**: Same as User Sign-up.

### 3. Login
- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "Password123!"
  }
  ```

### 4. Logout
- **URL**: `/logout`
- **Method**: `POST`
- **Notes**: Clears the `access_jwt` cookie.

### 5. Refresh Token
- **URL**: `/refresh`
- **Method**: `GET`
- **Notes**: Rotates the `access_jwt` cookie.

---

## ✅ Task Endpoints

**Base Path**: `/api/v1/tasks`

### 1. Get All Tasks (User)
- **URL**: `/`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "data": [
      {
        "id": "uuid",
        "title": "Task Title",
        "status": "pending",
        "priority": "medium",
        "due_date": "2025-12-31T23:59:59Z",
        "tags": ["tag1", "tag2"]
      }
    ]
  }
  ```

### 2. Get Specific Task (User)
- **URL**: `/{task_id}`
- **Method**: `GET`
- **Response**: Same as Task object above.

### 3. Create Task
- **URL**: `/`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "title": "Implement API",
    "description": "Complete the backend documentation",
    "priority": "high",
    "status": "pending",
    "due_date": "2025-12-31T23:59:59Z",
    "tags": ["work", "api"]
  }
  ```

### 4. Update Task
- **URL**: `/{task_id}`
- **Method**: `PATCH`
- **Body**: (Partial updates allowed)
  ```json
  {
    "title": "Updated Title",
    "status": "completed",
    "priority": "low"
  }
  ```

### 5. Delete Task
- **URL**: `/{task_id}`
- **Method**: `DELETE`
- **Response**: `{"data": {"message": "Task deleted successfully."}}`

### 6. Admin: Get All Tasks
- **URL**: `/admin/all`
- **Method**: `GET`
- **Notes**: Returns all tasks in the system. Requires Admin role.

### 7. Admin: Get Any Task
- **URL**: `/admin/{task_id}`
- **Method**: `GET`
- **Notes**: Retrieves a task regardless of which user owns it.

### 8. Admin: Delete Any Task
- **URL**: `/admin/{task_id}`
- **Method**: `DELETE`
- **Response**: `{"data": {"message": "Task deleted by admin."}}`

---

## 👤 User Endpoints

**Base Path**: `/api/v1/users`

### 1. Get Current User Profile
- **URL**: `/me`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "data": {
      "id": "uuid",
      "email": "user@example.com",
      "username": "testuser",
      "role": "user"
    }
  }
  ```

### 2. Update Current User
- **URL**: `/me`
- **Method**: `PATCH`
- **Body**:
  ```json
  {
    "username": "new_username"
  }
  ```

### 3. Delete Current User Account
- **URL**: `/me`
- **Method**: `DELETE`
- **Notes**: Deletes the account and clears session cookies.

### 4. Admin: Get All Users
- **URL**: `/admin/all`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "data": [
      {
        "id": "uuid",
        "username": "testuser",
        "email": "user@example.com",
        "role": "user",
        "is_active": true
      }
    ]
  }
  ```

### 5. Admin: Get Specific User
- **URL**: `/admin/{user_id}`
- **Method**: `GET`

### 6. Admin: Delete Specific User
- **URL**: `/admin/{user_id}`
- **Method**: `DELETE`
- **Response**: `{"data": {"message": "User deleted by admin."}}`

### 7. Admin: Update User Role
- **URL**: `/admin/{user_id}/role`
- **Method**: `PATCH`
- **Query Params**: `role` ("user" or "admin")
- **Response**: Returns the updated user object.

---

## 🧪 Comprehensive Test Scenarios

### Scenario A: New User Flow
1. **Signup**: `POST /auth/sign-up/user` with `user1@test.com` / `User123!`
2. **Login**: `POST /auth/login` with same credentials.
3. **Get Profile**: `GET /users/me` to verify session.
4. **Create Task**: `POST /tasks/` with `title: "First Task"`.
5. **Update Task**: `PATCH /tasks/{id}` with `status: "completed"`.
6. **Delete Account**: `DELETE /users/me` to clean up.

### Scenario B: Admin Flow
1. **Admin Login**: `POST /auth/login` with admin credentials.
2. **View Users**: `GET /users/admin/all` to see all registered users.
3. **Change Role**: `PATCH /users/admin/{id}/role?role=admin` to promote a user.
4. **Moderate Task**: `DELETE /tasks/admin/{task_id}` to remove unauthorized content.
