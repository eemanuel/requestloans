## Run Locally

### Clone repository

```sh
$  git clone https://github.com/eemanuel/requestloans.git
```

### Create virtualenv

Above the cloned directory

```sh
$  virtualenv venv
$  source venv/bin/activate
```

### Install requirements

At the same level than manage.py

```sh
$  pip install -r requirements/local.txt
```

### To run development server inside virtualenv

```sh
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## To run in docker container

At the same level than manage.py

```sh
$ docker-compose up
```

## Endpoints

**Create:**
/

**List:**
/list/

**Detail:**
/id/detail/

**Update:**
/id/update/

**Delete:**
/id/delete/
