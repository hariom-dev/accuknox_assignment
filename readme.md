
# Accuknox Assignment for social application API

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/hariom-dev/accuknox_assignment.git
$ cd accuknox_assignment
```

create local_settings.py

```sh
$ echo > local_settings.py
```
Paste this to settings
from .settings import *

DEBUG = os.environ.get('DEBUG', True)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'accuknowx_assignment'), 
        'USER': os.environ.get('DATABASE_USER', 'user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'password'),
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'), 
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}


Create .env file

```sh
$ echo > .env
```

Paste to env 

DEBUG=0
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_USER=root
DATABASE_PASSWORD=root
DATABASE_NAME=accuknox_assignment
DATABASE_PORT=5434
DATABASE_HOST=db




Run Migration

```sh
$ docker-compose exec web python manage.py migrate 
```

Start Server

```sh
$ docker-compose up --build
```