# CRUD + Sync Practice App

A small backend practice project built with **Python**, **FastAPI**, **SQLAlchemy**, and **MySQL**.

This project started as a basic CRUD app and was later extended into a small **data sync / data comparison app**.

It compares external user data with database data and applies business rules to update the database.

---

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Pydantic

---

## Project Features

### User Functions
- Create user
- Get user
- Get all users
- Patch user
- Delete user

### Group Member Functions
- Create group member
- Delete group member
- Get group member list

### Sync Functions
- Read external test data
- Read current DB data
- Convert DB data into dict maps
- Compare external data with DB data
- Create or update users
- Create or delete group members
- Return sync summary counts

---

## Database Tables

### `users`
Stores user master data.

Main fields:
- `id`
- `userid`
- `user_name`
- `is_active`
- `updated_at`

### `group_members`
Stores group membership data.

Main fields:
- `id`
- `userid`
- `user_name`
- `group_name`
- `updated_at`

---

## Sync Logic

### Users
- If `userid` already exists in the `users` table, compare `updated_at`
- If the external data is newer, update the user
- If `userid` does not exist, create a new user

### Group Members
- If external `is_active = True`, the user should exist in `group_members`
- If external `is_active = False`, the user should not exist in `group_members`

This logic is handled by comparing:
- external data
- `users` table data
- `group_members` table data

---

## Why `dict map` is used

To make sync logic simpler, DB data is converted into dictionaries like:

- `db_user_map[userid]`
- `db_member_map[userid]`

This helps:
- avoid unnecessary double loops
- make existence checks easier
- simplify create / patch / delete decisions

---

## Example Sync Result

The sync function returns summary counts such as:

- `hit`
- `user_patch`
- `user_create`
- `member_create`
- `member_delete`

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Make sure MySQL is running

Please make sure your MySQL server is running before starting the app.

### 3. Start the FastAPI server

```bash
uvicorn main:app --reload
```

### 4. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Users
- `POST /users` - create a new user
- `GET /users/{userid}` - get a user by userid
- `GET /users` - get all users
- `PATCH /users/{userid}` - update user status
- `DELETE /users/{userid}` - delete a user

### Group Members
- `POST /group-members` - create a group member
- `DELETE /group-members/{userid}` - delete a group member
- `GET /group-members` - get all group members

### Sync
- `POST /sync` - run the sync process

---

## What I Practiced in This Project

- FastAPI API development
- SQLAlchemy CRUD operations
- MySQL table design
- Sync logic implementation
- Business logic with `if`, `for`, and `dict`
- Comparing external data with DB data
- Updating in-memory maps after DB changes

---

## Future Improvements

- Refactor sync logic into smaller functions
- Replace debug `print()` with proper logging
- Improve project documentation
- Add a cleaner README with API examples

---

## Notes

This project is a practice app for learning backend development and sync logic.

It is not just a basic CRUD project.  
It was extended to simulate a small real-world data sync workflow.
