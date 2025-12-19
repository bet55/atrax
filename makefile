up:
	docker-compose up -d

down:
	docker-compose down

force-update:
	docker-compose exec web uv run phone_lookup/manage.py force_update
