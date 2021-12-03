# Backend

## Технологии

* Python (FastAPI)
* PostgreSQL
* Redis

## Вы можете развернуть всё в приложение в докере (включая базы данных)

__Backend__
```bash
docker-compose up --build -d
```

__Postgres__
```bash
cd docker/postgres
docker-compose up --build -d
```

__Redis__
```bash
cd docker/redis
docker-compose up --build -d
```