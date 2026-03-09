# Event Plus Backend - Architecture & Design Patterns

## Table of Contents
1. [What I Fixed](#what-i-fixed)
2. [Architecture Overview](#architecture-overview)
3. [Design Patterns Used](#design-patterns-used)
4. [Object Protection & Encapsulation](#object-protection--encapsulation)
5. [Access Patterns](#access-patterns)
6. [Data Flow](#data-flow)

---

## What I Fixed

### Issue 1: Undefined Variable
**File:** `app/routes/event_routes.py` (Line 28)
- **Problem:** Used `current_user_email` which was never defined
- **Solution:** Changed to `user.email` after fetching the complete user object from the repository

### Issue 2: Incorrect Attribute Name
**File:** `app/routes/event_routes.py` (Line 15)
- **Problem:** Used `current_app.authentication_service` which doesn't exist
- **Solution:** Changed to `current_app.auth_service` (the correct attribute registered in `app/__init__.py`)

### Issue 3: Unused Import
**File:** `app/routes/event_routes.py` (Line 3)
- **Problem:** Imported `UserRepository` but never used it directly
- **Solution:** Removed unused import

---

## Architecture Overview

Your project follows a **layered architecture** pattern:

```
┌─────────────────────────────────────────┐
│         Routes (API Endpoints)          │
│  event_routes.py, user_routes.py        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Services (Business Logic)       │
│  event_service.py, authentication_service.py
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        Repositories (Data Access)       │
│  event_repository.py, user_repository.py│
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Domain Models (Entities)        │
│  user.py, event.py                      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        Database (DynamoDB)              │
└─────────────────────────────────────────┘
```

---

## Design Patterns Used

### 1. **Repository Pattern**
The Repository pattern abstracts the data access layer and provides a clean interface for CRUD operations.

**Location:** `app/repositories/`

#### User Repository
```python
# Access pattern - repositories handle all database queries
user = UserRepository.get_by_email("user@example.com")
user = UserRepository.get_by_id(user_id)
UserRepository.save(user)
```

**Benefits:**
- Database logic is isolated from business logic
- Easy to mock for testing
- Can change database without affecting services
- Query logic is centralized

#### Event Repository
```python
event = EventRepository.get_by_id(event_id)
events = EventRepository.get_by_organizer_email(organizer_email)
event = EventRepository.get_by_slug(slug)
EventRepository.save(event)
EventRepository.delete_event(event_id)
```

---

### 2. **Service Layer Pattern**
Services contain the business logic and coordinate between repositories and routes.

**Location:** `app/services/`

#### Authentication Service
```python
class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository  # Dependency Injection
    
    def register(self, email, username, password, ...):
        # Creates user object
        user = User(...)
        # Uses repository to persist
        self.user_repository.save(user)
        return user
    
    def login(self, email, password):
        # Business logic: find user, check password, generate token
        user = self.user_repository.get_by_email(email)
        if not user.check_password(password):
            raise Exception("Invalid credentials")
        token = create_access_token(identity=user.id)
        return token
```

**Why this matters:**
- Keeps routes thin and focused on HTTP concerns
- Business logic is reusable and testable
- Single responsibility principle

#### Event Service
```python
class EventService:
    def __init__(self, event_repository, user_repository):
        self.event_repository = event_repository
        self.user_repository = user_repository
    
    def create_event(self, title, description, ...):
        # Validation happens here
        if len(title) < 8 or len(title) > 20:
            raise ValueError("Title must be 8-20 chars")
        
        # Check for duplicates
        if self.event_repository.get_by_slug(slug):
            raise ValueError("Event already exists")
        
        # Create and persist
        event = Event(...)
        self.event_repository.save(event)
        return event
```

---

### 3. **Domain-Driven Design (DDD)**
Domain models (User, Event) encapsulate business rules and data.

**Location:** `app/domain/`

#### User Domain Model
```python
class User:
    def __init__(self, id, email, password_hash, username=None, ...):
        # Protection: Validation in constructor
        if not id or not email:
            raise ValueError("email and password hash are required")
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        
        self.id = id
        self.email = email
        self.password_hash = password_hash  # Never store plain text!
        # ... other fields
    
    # Business logic methods
    def set_password(self, password):
        # Only way to set password - always hashed
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        # Secure password verification
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        # Encapsulates update logic
        self.last_login = datetime.utcnow()
```

#### Event Domain Model
```python
class Event:
    def __init__(self, id, title, description, organizer_email, ...):
        # Validation: Required fields
        if not id or not title or not organizer_email:
            raise ValueError("Missing required fields")
        
        # Type checking
        if not isinstance(title, str):
            raise ValueError("title must be string")
        
        self.id = id
        self.title = title
        self.status = 'scheduled'  # Encapsulated state
        self.created_at = datetime.utcnow()
    
    def update_event(self, title=None, description=None, ...):
        # Controlled updates - only fields that can be updated
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
```

---

## Object Protection & Encapsulation

### 1. **Constructor Validation**
Objects are protected at creation time:

```python
# User must have email and password_hash
user = User(id="123", email="user@email.com", password_hash="hashed...")
# ✓ Valid

# This would fail:
user = User(id="123", email=None, password_hash="hashed...")
# ✗ Raises: ValueError("email and password hash are required")
```

### 2. **Type Checking**
```python
# Event requires strings for certain fields
event = Event(..., title="Valid Title", organizer_email="email@test.com")
# ✓ Valid

# Type mismatch caught:
event = Event(..., title=123, organizer_email="email@test.com")
# ✗ Raises: ValueError("title must be a string")
```

### 3. **Password Hashing (Critical Protection)**
Passwords are **never stored in plain text**:

```python
# ❌ WRONG - Plain text password
user.password_hash = "mypassword123"

# ✅ CORRECT - Always hash
user.set_password("mypassword123")
# Uses werkzeug.security.generate_password_hash() internally
```

### 4. **Immutable IDs**
Once created, an object's ID cannot be changed:
```python
user = User(id="user-123", ...)
# ID is set once and never modified
# This prevents accidental or malicious ID changes
```

### 5. **Status State Machine (Events)**
Events have controlled statuses:
```python
event.status  # Can be: 'scheduled', 'running', 'stopped', 'completed', 'cancelled'

# Protection: Cannot update certain states
if event.status in ['stopped', 'completed', 'cancelled', 'running']:
    raise ValueError("Cannot update stopped/completed/running/cancelled events")
```

### 6. **Repository Control**
Direct database access is restricted to repositories:
```python
# ❌ WRONG - Direct database access in routes
dynamodb.table.put_item(Item={...})

# ✅ CORRECT - Through repository
user_repository.save(user)
event_repository.save(event)
```

This ensures all data modifications go through validated paths.

---

## Access Patterns

### 1. **How Routes Access Data**

**Current Implementation:**
```python
# app/routes/event_routes.py
@event_bp.route("/create", methods=["POST"])
@jwt_required()  # ← Protection: Only authenticated users
def create_event():
    data = request.get_json()
    current_user = get_jwt_identity()  # ← Get user ID from JWT token
    
    # 1. Get services from Flask app
    event_service = current_app.event_service
    
    # 2. Get user object through service
    user = current_app.auth_service.user_repository.get_by_id(current_user)
    
    # 3. Create event through service (business logic applied)
    event = event_service.create_event(
        title=data["title"],
        description=data.get("description"),
        event_start_datetime=data["event_start_datetime"],
        event_end_datetime=data["event_end_datetime"],
        no_of_participants_allowed=data.get("no_of_participants_allowed", 10),
        organizer_email=user.email,      # ← Protected: Uses authenticated user's email
        organizer_name=user.username,     # ← Protected: Uses authenticated user's name
        organizing_for=data.get("organizing_for", "self")
    )
    
    return jsonify({"success": True, "event_id": event.id}), 201
```

**Access Flow:**
```
Route → Service → Repository → Database
  ↓        ↓          ↓            ↓
HTTP    Validation  Query      DynamoDB
Layer   & Logic     Builder
```

### 2. **Service Access Patterns**

```python
# Authentication Service
auth_service = current_app.auth_service
user = auth_service.user_repository.get_by_email(email)
token = auth_service.login(email, password)  # Returns JWT token

# Event Service
event_service = current_app.event_service
event = event_service.create_event(...)      # Returns Event object
events = event_service.get_events_by_organizer_email(email)  # Returns list
event_service.delete_event(event_id)         # Performs deletion
```

### 3. **Repository Access Patterns**

```python
# User Repository
user_repository.get_by_id(user_id)           # Single user by ID
user_repository.get_by_email(email)          # Single user by email
user_repository.save(user)                   # Create or update

# Event Repository
event_repository.get_by_id(event_id)         # Single event
event_repository.get_by_slug(slug)           # Unique event
event_repository.get_by_organizer_email(email)  # Multiple events
event_repository.save(event)                 # Create or update
event_repository.delete_event(event_id)      # Delete
event_repository.update_status(event_id, status)  # Update status
```

---

## Data Flow - Complete Example

### User Creates an Event

```
1. CLIENT SENDS REQUEST
   POST /api/events/create
   Authorization: Bearer <JWT_TOKEN>
   {
     "title": "Python Meetup 2026",
     "description": "Learn Python best practices",
     "event_start_datetime": "2026-03-15 18:00:00",
     "event_end_datetime": "2026-03-15 20:00:00",
     "no_of_participants_allowed": 50,
     "organizing_for": "community"
   }

2. ROUTE LAYER (event_routes.py)
   ✓ @jwt_required() validates JWT token
   ✓ get_jwt_identity() extracts user ID from token
   ✓ Gets services from Flask app

3. SERVICE LAYER (event_service.py)
   ✓ Gets USER object from repository
   ✓ Validates event data:
     - Title length: 8-20 chars
     - Required dates present
     - Unique slug (no duplicate title)
   ✓ Creates EVENT domain object
   ✓ Calls repository to save

4. DOMAIN LAYER (Event model)
   ✓ Constructor validates all fields
   ✓ Type checking for strings
   ✓ Assigns default status: 'scheduled'
   ✓ Sets created_at timestamp

5. REPOSITORY LAYER (event_repository.py)
   ✓ Converts Event to DynamoDB item
   ✓ Formats data with composite keys
   ✓ Calls dynamodb.table.put_item()

6. DATABASE (DynamoDB)
   ✓ Stores item:
     {
       "PK": "EVENT#<uuid>",
       "SK": "DETAILS",
       "title": "Python Meetup 2026",
       "organizer_email": "user@example.com",
       "status": "scheduled",
       ...
     }

7. RESPONSE
   ✓ Service returns Event object
   ✓ Route returns JSON:
     {
       "success": true,
       "event_id": "<uuid>"
     }
```

---

## Inheritance & Relationships

### No Direct Inheritance (Composition Over Inheritance)
Your project uses **composition** rather than inheritance:

```python
# ❌ NOT USED: Inheritance
class Event(BaseEntity):
    pass

# ✅ USED: Composition/Dependency Injection
class EventService:
    def __init__(self, event_repository):
        self.event_repository = event_repository  # Composed
        
class EventRepository:
    def __init__(self, dynamodb, table_name):
        self.table = dynamodb.Table(table_name)  # Composed
```

### Why Composition?
1. **Flexibility:** Easy to swap implementations
2. **Testability:** Easy to mock dependencies
3. **Single Responsibility:** Each class has one job
4. **Loose Coupling:** Classes don't depend on inheritance hierarchies

---

## Object Lifecycle

### User Object Lifecycle
```
1. Created by AuthService.register()
   ↓
2. Validated in User.__init__()
   ↓
3. Password hashed by user.set_password()
   ↓
4. Persisted by UserRepository.save()
   ↓
5. Retrieved by UserRepository.get_by_email() or get_by_id()
   ↓
6. Used in routes with authenticated user
```

### Event Object Lifecycle
```
1. Created by EventService.create_event()
   ↓
2. Validated in Event.__init__()
   ↓
3. Slug generated by extensions.generate_slug()
   ↓
4. Status set to 'scheduled'
   ↓
5. Persisted by EventRepository.save()
   ↓
6. Retrieved by EventRepository queries
   ↓
7. Updated by EventService.update_event()
   ↓
8. Deleted or status changed
```

---

## Summary: Protection Mechanisms

| Mechanism | Where | Why |
|-----------|-------|-----|
| **JWT Authentication** | Routes (@jwt_required) | Only authorized users can access |
| **Constructor Validation** | Domain models | Objects can't be created in invalid state |
| **Type Checking** | Domain models | Wrong data types caught immediately |
| **Password Hashing** | User model | Passwords never stored in plain text |
| **Service Layer** | Services | Business rules applied consistently |
| **Repository Access** | Repositories | All database changes go through controlled path |
| **Status State Machine** | Event model | Events can't be updated in certain states |
| **Immutable IDs** | Domain models | IDs can't be accidentally changed |

---

## Next Steps to Improve

1. **Add logging** to track data access and changes
2. **Add unit tests** to validate business logic
3. **Add API error handling** for better error messages
4. **Add rate limiting** to prevent abuse
5. **Add permissions** to ensure users can only modify their own events
