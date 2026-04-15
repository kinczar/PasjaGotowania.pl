# PasjaGotowania
Pasja Gotowania is a web application that allows users to discover, share, and save cooking recipes.
The platform combines a recipe search engine with a forum where users can post their own recipes, interact with others, and build a personal collection of favorite dishes.

### Main features
- Search recipes by name or ingredients
- Create and share your own recipes via forum posts
- Comment and like posts
- Save forum posts
- User authentication (register/login/logout)
- Basic health tools (BMI & calorie calculator)

### Technologies

- Python 3.13.5 – backend development
- Django 5.1.6 – web framework
- HTML / CSS / JavaScript – frontend
- PostgreSQL (Aiven) – cloud database
- Cloudinary – image storage and management
- Bootstrap / custom CSS – UI styling

### Dependencies

The project uses the following main dependencies:

- **Django (~5.1.6)** – main web framework used to build the application  
- **Pillow** – image processing library required for handling uploaded images  
- **mysqlclient** – database connector for MySQL  
- **python-dotenv** – loading environment variables from `.env` file  
- **cloudinary** – cloud-based image storage service  
- **django-cloudinary-storage** – integration of Cloudinary with Django  

## How to run local server
Get to the `webapp` directory: `cd webapp` and run `python3 manage.py runserver` from webapp folder

*In some enviroments it could be not `python3` but `python`* 


### How to set up a virtual environment:

`python3 -m venv .venv` and then select new environment in a VSCode (bottom-right corner)

### How to switch to a virtual environment in a terminal

Run `.venv\Scripts\Activate`. Then you will see (.venv) on the left from a CLI prompt

### How to install all dependencies in an env

`pip3 install -r requirements.txt`

### Create .env file in webapp

```
DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=<password>
DB_HOST=<host>
DB_PORT=<db_port>
CLOUD_NAME=<cloud_name>
API_KEY=<api_key>
API_SECRET=<api_secret>

```

### Credentials

All database credentials are private and available only to the project authors.  
They are not included in this repository for security reasons.

### How Quit the server :
Quit the server with CTRL-C in command line

