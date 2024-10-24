# CRM A/S

This is a CRM (Customer Relational Management)
it's made to be more streamlined for Insurance agents.


## Github Contributors:
alexpr42
AngelHCS


### Project Layout:

crm_project/                # Root directory
│
├── app/                    # App directory
│   ├── __init__.py         # Initiates flask and extensions.
│   ├── models.py           # Defines Database Model.
│   ├── routes.py           # Routes for app layout.
│   ├── auth.py             # Authentication logic
│   ├── templates/          # Diretory containing HTML templates.
│   │   ├── base.html       # Base HTML template.
│   │   ├── dashboard.html  # Dashboard (Contains control panel.)
│   │   ├── login.html      # Page containing the login
│   │   └── client_list.html # Page with client list.
│   └── static/             # Static files, These contain CSS and Javascript
│       ├── styles.css      # personalized styles for the application
│       └── scripts.js      # Javascript scrips (Optional.)
│
├── config.py               # Saves application configuration (Database, Password and such)
├── requirements.txt        # Contains the dependencies the project currently has.
├── run.py                  # Runs the flask application, It's how to actually initiate the app.
