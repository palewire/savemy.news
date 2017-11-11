# Save My News

A personal, permanent clipping service.

### Getting started

Requirements:

* Python
* PostgreSQL
* virtualenv or virtualenvwrapper
* Git

Create a virtualenv to store the codebase.

```bash
$ virtualenv savemy.news
```

Activate the virtualenv.

```bash
$ cd savemy.news
$ . bin/activate
```

Clone the git repository from GitHub.

```bash
# If you've made a fork, substitute in your URL
$ git clone git@github.com:pastpages/savemy.news.git repo
```

Enter the project and install its dependencies.

```bash
$ cd repo
$ pip install -r requirements.txt
```

Create a copy of a local settings file for your development environment.

```bash
$ cp project/settings_dev.py.tmpl project/settings_dev.py
```

Create a local database

```bash
$ python manage.py migrate
```

Run the test server for the first time.

```bash
$ python manage.py runserver
```
