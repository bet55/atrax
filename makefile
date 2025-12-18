.PHONY: up down build logs test celery

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

test:
	docker-compose exec web python manage.py test

celery:
	docker-compose exec celery celery -A phone_lookup worker --loglevel=info

beat:
	docker-compose exec celery celery -A phone_lookup beat --loglevel=info

flower:
	docker-compose exec celery celery -A phone_lookup flower

run-update:
	docker-compose exec web python manage.py update_registry

run-task:
	docker-compose exec web python manage.py run_update_task

# Полный стек для разработки
dev: down up
	@echo "Сервисы запущены:"
	@echo "  • Web: http://localhost:8000"
	@echo "  • API: http://localhost:8000/api/lookup/"
	@echo "  • Admin: http://localhost:8000/admin/"
	@echo "  • Celery worker: запущен в контейнере celery"