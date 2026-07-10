[Claude link](https://claude.ai/share/4d87cc70-63d9-4ff4-8627-a3618f3180a2)
# Django RBAC Project

A Django-based **Role-Based Access Control (RBAC)** system built using Django's built-in **Groups** and **Permissions** framework. Includes custom user authentication (Login/Register), a Super Admin panel, and fully dynamic role & permission management — no hardcoded roles.

## Features

- Custom User Model (extends `AbstractUser`)
- User Registration & Login (raw `request.POST` handling, no Django Forms)
- Super Admin (`is_superuser`) with full bypass access
- Dynamic Role (Group) creation — add as many roles as needed at runtime
- Permission assignment per role via a simple checkbox UI
- Module-wise custom permissions (via model `Meta.permissions`)
- Bootstrap 5 UI
- Seed command for default roles (Admin, Manager, Accountant, Sales, Purchase, Inventory, HR, Payroll, CRM, Auditor, Branch Manager, Cashier, Store Keeper)

## Tech Stack

- Python 3.x
- Django 6.0.6
- SQLite (default, swappable)
- Bootstrap 5

## Project Structure

```
rbac_project/
├── config/            # Project settings, root urls
├── accounts/           # Custom user model, login/register views
├── core/                # Dashboard, role & permission management
├── templates/
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   └── core/
│       ├── dashboard.html
│       ├── role_list.html
│       └── role_form.html
└── manage.py
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd rbac_project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django
```

*(Optional)* freeze dependencies:

```bash
pip freeze > requirements.txt
```

### 4. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Super Admin)

```bash
python manage.py createsuperuser
```

### 6. (Optional) Seed default roles

```bash
python manage.py seed_roles
```

This creates empty Groups for: Admin, Manager, Accountant, Sales, Purchase, Inventory, HR, Payroll, CRM, Auditor, Branch Manager, Cashier, Store Keeper. Permissions must then be assigned via the Role Management UI.

### 7. Run the development server

```bash
python manage.py runserver
```

## Usage

| URL | Description |
|---|---|
| `/accounts/register/` | New user registration |
| `/accounts/login/` | User login |
| `/accounts/logout/` | Logout |
| `/` | Dashboard |
| `/roles/` | Role list (Super Admin only) |
| `/roles/create/` | Create a new role with selected permissions |
| `/roles/<id>/edit/` | Edit role name / permissions |
| `/roles/<id>/delete/` | Delete a role |

### How RBAC works

1. **Super Admin** (`is_superuser=True`) has unrestricted access and bypasses all permission checks.
2. Super Admin logs in and creates **Roles** (Django `Group`s) with any name, assigning any combination of **Permissions**.
3. Permissions include Django's auto-generated CRUD permissions (`add_`, `change_`, `delete_`, `view_` per model) plus any custom permissions defined in each app's `Meta.permissions`.
4. Users are assigned one or more roles via `user.groups`.
5. Access is checked in views/templates using:
   ```python
   request.user.has_perm("app_label.codename")
   ```
   ```html
   {% if perms.app_label.codename %}
   ```

### Adding new modules/permissions

When adding a new app/model, define custom permissions in its `Meta` class:

```python
class Invoice(models.Model):
    class Meta:
        permissions = [
            ("approve_invoice", "Can approve invoice"),
        ]
```

Run migrations, and the new permission automatically appears in the Role Management UI — no additional code changes required.

## Roadmap

- [ ] Email-based password reset
- [ ] User management UI (assign roles to existing users)
- [ ] Audit logging for role/permission changes
- [ ] API-based permission checks (DRF)

## License

This project is open for personal/commercial use. Update this section based on your preferred license (MIT, Apache 2.0, etc.).
