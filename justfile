# Stack demineur — jeu démineur Python

status:
    docker compose ps

deploy: pull build down up

pull:

build:
    docker compose build

down:
    docker compose down

up:
    docker compose up -d

restart:
    docker compose restart

logs *ARGS:
    docker compose logs {{ARGS}}
