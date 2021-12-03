# Backend

Swagger/OpenAPI документация находится в __stinger-hack.ru/docs__

## Технологии

* Python (FastAPI)
* PostgreSQL
* Redis

## Вы можете развернуть всё в приложение в докере (включая базы данных)

__Backend__
```bash
docker-compose up --build -d
```

__Postgres, Redis__
```bash
cd docker
docker-compose up --build -d
```

## Либо развернуть в виртуальном окружении

## Запуск Linux / Mac

```console
foo@bar:~$ cd simple
foo@bar:~$ virtualenv env
foo@bar:~$ source env/bin/activate
foo@bar:~$ pip install -r requirements.txt
```

## Запуск Windows

```console
foo@bar:~$ cd simple
foo@bar:~$ virtualenv env
foo@bar:~$ env/Scripts/activate.ps1
foo@bar:~$ pip install -r requirements.txt
```
