# nlp-table-questioning
NLP table questioning using Python


### Features
- User signup and login
- Session for user
- User signup and login blocked when signed in


### Setup instructions

#### Clone this repository
```
git clone https://github.com/orangatun/nlp-table-questioning.git
```

Change the current working directory to the parent of `nlp-table-questioning`.

For example if the absolute path of the project is `/home/user/Projects/flask-tutorial/nlp-table-questioning/`, the current working directory should be `/home/user/Projects/flask-tutorial/`. 

#### Create Virtual Environment
```
python3 -m venv .venv
```

#### Activate the Virtual Environment
```
. .venv/bin/activate
```

#### Installing flask

```
pip3 install Flask
```


### Running the application


#### Initialize Database 

We're currently using SQLite for the database, and here's the command to initialize it

```
flask --app nlp-table-questioning init-db
```
#### Running the app

```
flask --app nlp-table-questioning run
```

To run in debug mode, add the debug option
```
flask --app nlp-table-questioning --debug run
```

Open the url `http://127.0.0.1:5000` in the browser to view the website
