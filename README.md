# DB Links:

### First DB link:
https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?select=credits.csv \
This DB will be our main db and includes a lot of metadata about movies

### Second DB link:
https://www.kaggle.com/datasets/aptlin/posterlens-25m \
This dataset will be used for showing posters of the images in the client

Download those datasets, then create a data folder in the root of the project, and put those files in the data folder.
The movies db should be under the the-movies-dataset folder.
The posterlens db should be under posterlens folder.

# Prerequisites:

1. Make sure you have UV installed on your system, if not, download it here: \
https://docs.astral.sh/uv/getting-started/installation/

2. Make sure you have mysql installed on your system, if not, download it here: \
https://dev.mysql.com/downloads/mysql/8.4.6.html \
We will be using version 8.4.6 of mysql as its the LTS veresion.

3. Make sure you have Node.js installed on your system, if not, download it here: \
https://nodejs.org/en/download/

# Installing Depencences:

### Installing python dependences:
```uv sync```
Then, make sure your python is using the created environment: \
```source .venv/bin/activate```

### Installing node dependences: 
First, cd into the client folder: \
```cd client``` \
Then, install the dependences: \
```npm install```

# To run the project:

First, make sure mysql is running, and update the .env file with your mysql credentials.

### Creating the database (Run this only once):
#### For the dev - Itay and Eyal use this: 
```python -m db.load_data```
#### For the testers that want to look at the project use this:
```python -m db.init_db_from_dump dump_file.sql```

### To run the backnd: 
```uvicorn app.main:app --reload``` 

### To run the client: 
Do this in a different terminal from the terminal running the backend. 
```cd client``` \
```npm run start```