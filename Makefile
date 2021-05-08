.PHONY: run
run:
	docker-compose up

.PHONY: install
install:
	docker-compose build
	docker-compose run web python manage.py migrate

.PHONY: test
test:
	docker-compose run web python manage.py behave --simple --failfast

.PHONY: superuser
superuser:
	docker-compose run web python manage.py createsuperuser

.PHONY: clean
clean:
	docker-compose down -v
