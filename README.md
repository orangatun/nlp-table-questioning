# nlp-table-questioning
NLP table questioning using Python

Please visit [Wiki](https://github.com/orangatun/nlp-table-questioning/wiki) for more details about this project.

Details in Wiki include:
- UI Mockups
- Screenshots of views
- Detailed setup instructions
- Known Issues

## Homepage

<img width="719" alt="image" src="https://github.com/orangatun/nlp-table-questioning/assets/34887793/c246139d-9ad0-4960-a03f-b4281203abbe">


## Project structure

```
..                                      # Parent directory aka repository root
├── instance/                           # Created by flask
│   ├── uploads/                        # Created during init to save `.csv` files
│   │   └── ...                         # `.csv` files
│   └── nlp-table-questioning.sqlite    # sqlite database file
│
├── nlp-table-questioning/              # Project directory
│   ├── ai_model/                       # Contains AI models
│   │   └── tapas_model.py              # Functions to access pre-trained table questioning model using transformers
│   │
│   ├── sqlite/                         # Contains sqlite related code
│   │   ├── sqlite_db.py                # Contains functions for db init, and handling db connection
│   │   ├── sqlite_db_func.py           # Contains sql interface layer for functions that execute on sqlite db
│   │   └── sqlite_schema.sql           # Schema for sqlite db
│   │
│   ├── static/                         # Contains static css or image files
│   │   ├── home/                       # Contains individual css for each of the pages
│   │   │   ├── general-home.css        # Styling for home page when user is not signed in
│   │   │   ├── history.css             # Styling for user history page
│   │   │   └── user-home.css           # Styling for user home page for when user is signed in
│   │   │
│   │   ├── auth.css                    # Styling for all the pages under `auth` template (signup, login, signedin)
│   │   └── base-style.css              # Styling for the template `base.html` which includes navbar
│   │
│   ├── templates/                      # Contains html template files
│   │   ├── auth/                       # Contains individual css for each of the pages
│   │   │   ├── login.html              # Login page html
│   │   │   ├── signedin.html           # For when the user tries to login or signup when already logged in
│   │   │   └── signup.html             # Signup page html
│   │   │
│   │   ├── home/                       # Contains individual css for each of the pages
│   │   │   ├── general-home.html       # Home page when user is not signed in
│   │   │   ├── history.html            # User history page displays all user file and question activity
│   │   │   └── user-home.html          # User home page for when user is signed in
│   │   │
│   │   └── base.html                   # Base html template which includes navbar commonly used
│   │
│   ├── __init__.py                     # inits db, instance dir, registers blueprints for home and auth paths
│   ├── auth.py                         # Contains routes for signup, login, logout and auth functions
│   ├── home.py                         # Contains routes for user home, general home, user history, file and questions handlers.
│   └── README.md                       # Contains setup and running info for the project.
│
├── .flaskenv                           # Contains environment variables of project
└── ...
```

**NOTE**: `.flaskenv` file needs to be moved from the `nlp-table-questioning/` directory to its parent directory (aka repository root) before running the application.


## Features
- User signup and login
- Session for user
- .csv File upload for user
- Querying files with pre-trained table querying AI model
- View history of all file, questions and answers history of a user


## About the AI model
The AI model used is [google/tapas-base-finetuned-wtq](https://huggingface.co/google/tapas-base-finetuned-wtq) from [HuggingFace](https://huggingface.co).

From the description:
> TAPAS is a BERT-like transformers model pretrained on a large corpus of English data from Wikipedia in a self-supervised fashion. This means it was pretrained on the raw tables and associated texts only, with no humans labelling them in any way (which is why it can use lots of publicly available data) with an automatic process to generate inputs and labels from those texts. 

## Setup instructions

### Clone this repository
```
git clone https://github.com/orangatun/nlp-table-questioning.git
```

Change the current working directory to the parent of `nlp-table-questioning`.

For example if the absolute path of the project is `/home/user/Projects/flask-tutorial/nlp-table-questioning/`, the current working directory should be `/home/user/Projects/flask-tutorial/`. 

### Move the `.flaskenv` file

The `.flaskenv` file contains environment variables which need to be in current working directory. Going off the previous example, the final path of the `.flashenv` file should be `/home/user/Projects/flask/.flaskenv` and **NOT** `/home/user/Projects/flask/nlp-table-questioning/.flaskenv`.

### Create Virtual Environment
```
python3 -m venv .venv
```

### Activate the Virtual Environment
```
. .venv/bin/activate
```

### Installing dependencies

```
pip3 install Flask transformers pandas torch torchvision python-dotenv pymysql
pip3 install -r ./nlp-table-questioning/requirements.txt

```

## Running the application


### Initialize Database 

#### Using SQLite

We're currently using SQLite for the database, and here's the command to initialize it

```
flask --app nlp-table-questioning init-db
```

**NOTE**: If the database is ever deleted before being removed from the app context,
to re-initialize it, just run the command again. It will create a new one, and replace the connection in the context.

#### Using MySQL

To use MySQL, set the details in `.flaskenv` with localhost for local installation, and `db4free.net` for the online service.
Replace the username, password, and database_name with their respective values.

```
DEV_DATABASE_HOST=localhost #db4free.net
DEV_DATABASE_USER=username
DEV_DATABASE_PASS=password
DEV_DATABASE_DB=database_name
```

##### Online MySQL service

In order to save setup time for MySQL, I was able to find a free hosted MySQL service [db4free.net](https://www.db4free.net).
The service is unreliable and has a limit of 200MB, and is only meant for testing purposes. 
However, it offers a quick way to test out the project.

Please delete your account after use, to save resources.

##### Local MySQL installation

Follow the installation instructions for your operating system in the [official documentation here](https://dev.mysql.com/doc/mysql-getting-started/en/)

After the installation, set your username and password in the mysql monitor

```mysql
mysql>  ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
```

Once your new password is set, create a database

```mysql
mysql> CREATE DATABASE pets;
```

To verify that the database is created, run the command

```mysql
mysql> SHOW DATABASES;
```

Replace the username, password, and database_name values in `.flaskenv` with your values now. 


### Running the app

```
flask --app nlp-table-questioning run
```

To run in debug mode, add the debug option
```
flask --app nlp-table-questioning --debug run
```

Open the url `http://127.0.0.1:5000` in the browser to view the website
