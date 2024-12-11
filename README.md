[![⚙️ CI](https://github.com/usrofgh/traffic_devils/actions/workflows/ci.yml/badge.svg)](https://github.com/usrofgh/traffic_devils/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/usrofgh/traffic_devils.svg)](https://GitHub.com/usrofgh/traffic_devils/releases/)
 
## STACK
![](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![](https://img.shields.io/badge/Pydantic-e92063?style=for-the-badge&logo=Pydantic)
![](https://img.shields.io/badge/SQLAlchemy-798577?style=for-the-badge&logo=sqlalchemy)
![](https://img.shields.io/badge/alembic-ffffff?style=for-the-badge&logo=alembic)
![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![](https://img.shields.io/badge/poetry-0088dd?style=for-the-badge&logo=poetry)
![](https://img.shields.io/badge/asyncio-blue?style=for-the-badge&logo=asyncio)
![](https://img.shields.io/badge/asyncio-blue?style=for-the-badge&logo=asyncio)
![](https://img.shields.io/badge/Sentry-black?style=for-the-badge&logo=Sentry&logoColor=#362D59)
![](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)

<hr>


# <a name="docker">🐳 Docker</a>
It uses a multi-stage build to optimize the image size

Put .env to root of the project
```bash
git clone https://github.com/usrofgh/traffic_devils.git
cd traffic_devils
docker compose up
```

Visit http://127.0.0.1:8001/docs

You can register a new user or login with help the next creds:

1. admin / stringst (admin rules)
2. manager / stringst (manager rules)
3. user / stringst (user rules)


Example of creating a message and sending to TG(https://t.me/traffic_devills_bot)

In 'chat_id' you can specify ID of your chat
```json
{
  "bot_token": "7617819637:AAG2qbjjMgpe4UhEXWKYYpUHJStZbTSZ6rs",
  "chat_id": "1946569085",
  "message": "What's up"
}
```


## Swagger docs http://127.0.0.1:8081/v1/docs

![Scenarios](https://img001.prntscr.com/file/img001/wSSnEFSKSSqOUCJzlP8i_g.png)
