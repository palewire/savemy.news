test:
	pipenv run flake8 archive --exclude=archive/migrations/*
	pipenv run python manage.py test

loadbackup:
	heroku pg:backups:download
	sudo -u postgres dropdb savemynews
	sudo -u postgres createdb savemynews
	pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d savemynews latest.dump
	rm latest.dump
