postgres:
	docker run --name fasttodo-postgres -e POSTGRES_USER=root -e POSTGRES_PASSWORD=secret -p 127.0.0.1:5432:5432 -d postgres:15-alpine

createdb:
	docker exec -it fasttodo-postgres createdb --username=root --owner=root fasttodo

dropdb:
	docker exec -it fasttodo-postgres dropdb fasttodo

migration:
	migrate create -ext sql -dir app/db/migrations -seq init_schema

migrateup:
	migrate -path ./database/migrations/ -database "postgresql://root:secret@localhost:5432/fasttodo?sslmode=disable" -verbose up

migratedown:
	migrate -path ./database/migrations/ -database "postgresql://root:secret@localhost:5432/fasttodo?sslmode=disable" -verbose down

tests:
	poetry run pytest

.PHONY: postgres createdb dropdb tests