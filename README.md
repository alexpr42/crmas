# CRM A/S


This is a CRM (Customer Relational Management) system designed to streamline workflows for insurance agents.

## GitHub Contributors:
- [alexpr42](https://github.com/alexpr42)
- [AngelHCS](https://github.com/AngelHCS)

### Project Layout:

```
crm_project/                # Root directory
│
├── app/                    # App directory
│   ├── __init__.py         # Initializes Flask and extensions.
│   ├── models.py           # Defines database model.
│   ├── routes.py           # Routes for app layout.
│   ├── auth.py             # Authentication logic.
│   ├── templates/          # Directory containing HTML templates.
│   │   ├── base.html       # Base HTML template.
│   │   ├── dashboard.html  # Dashboard (contains control panel).
│   │   ├── login.html      # Login page.
│   │   └── client_list.html# Page with client list.
│   └── static/             # Static files (CSS, JS).
│       ├── styles.css      # Custom styles for the application.
│       └── scripts.js      # JavaScript scripts (optional).
│
├── config.py               # Application configuration (database, passwords, etc.).
├── requirements.txt        # Project dependencies.
├── run.py                  # Runs the Flask application.
```



#### Getting Started
1. Get the repository from github, you can find it easier by searching our profiles
2. Install the dependencies listed in the requirements.txt file
3. Use the run.py file to run the app.



#### License
(TBD)
