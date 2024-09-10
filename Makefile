start :
	python manage.py runserver 0.0.0.0:8000

uvicorn-start :
	uvicorn coffee_shop.asgi:application --host 0.0.0.0 --port 8000

gunicorn-start:
	gunicorn coffee_shop.wsgi:application --host 0.0.0.0 --port 8000

waitress-start:
	waitress-serve --listen=127.0.0.1:5000 coffee_shop.wsgi:application

migrate :
	python manage.py migrate --run-syncdb
	python manage.py makemigrations

shell :
	python manage.py shell

tests:
	python manage.py test --pattern="test_*.py" --parallel auto --force-color --debug-mode --verbosity 0

