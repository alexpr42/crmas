# CRM A/S

The goal of this project is to make a CRM, Focusing on streamlining it for insurance agents.


## Github contributors:
alexpr42
AngelHCS



Project is run using run.py


### Project structure:
crm_project/                # Root folder of project
│
├── app/                    # App folder
│   ├── __init__.py         # Starts flask app and it's extensions.
│   ├── models.py           # Defines database models
│   ├── routes.py           # visual routes for app.
│   ├── auth.py             # Routes and logic for authenthication(Login/out)
│   ├── templates/          # Folder with the HTML templates
│   │   ├── base.html       # Base template (Other templates burrow from this)
│   │   ├── dashboard.html  # Dashboard page (Otherwise known as control panel)
│   │   ├── login.html      # Login page
│   │   └── client_list.html # Page with client list template.
│   └── static/             # Contains static files made in CSS and Javascript.
│       ├── styles.css      # Personalized styles for the application.
│       └── scripts.js      # Javascript scripts (Optional)
│
├── config.py               # App config (Contains the database, passwords, etc.)
├── requirements.txt        # Text file with a list of dependencies
├── run.py                  # File that runs the flask file.
└── README.md               # This file, contains basic information about the application.

