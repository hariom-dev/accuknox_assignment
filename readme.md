
# Accuknox Assignment for social application API

##Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/hariom-dev/accuknox_assignment.git
$ cd accuknox_assignment
```

Run Migration

```sh
$ docker-compose exec web python manage.py migrate 
```

Start Server

```sh
$ docker-compose up --build
```