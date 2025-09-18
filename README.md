# Cafe Manager

A Django-based management system for tracking cafe inventory and equipment maintenance.

## Overview

Cafe Manager is a web application designed to help cafe owners and managers efficiently track:
- Product inventory and expiration dates
- Equipment status and maintenance needs
- Overall cafe operational status

## Features

- **Product Management**
  - Track product quantities
  - Monitor expiration dates
  - Maintain product descriptions and details

- **Equipment Tracking**
  - Monitor equipment status
  - Track maintenance history
  - Record equipment conditions

- **State Management**
  - Define and track different states for equipment
  - Maintain detailed descriptions of conditions

## Project Structure

```
CafeManager/
├── Cafe/
│   ├── models.py         # Data models
│   ├── views.py          # View logic
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin interface
│   └── serializers.py    # API serializers
└── CafeManager/
    ├── settings.py       # Project settings
    ├── urls.py          # Main URL configuration
    └── wsgi.py          # WSGI configuration
```

## Data Models

### Product
- `name`: Product name
- `description`: Product details
- `quantity`: Current stock quantity
- `expiration_date`: Product expiration date

### Equipment
- `name`: Equipment name
- `description`: Equipment details
- `state`: Current state (foreign key to State)
- `date`: Date of last status update

### State
- `name`: State name
- `description`: Detailed description of the state

## Requirements

See `requirements.txt` for a full list of dependencies.

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

Access the admin interface at `/admin` to:
- Add/Edit products and track inventory
- Manage equipment status
- Define and update equipment states
