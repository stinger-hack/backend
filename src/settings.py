import os

PREFIX = "/v1/api"

AUDIENCE: str = "Hack"
APP_ID: str = "app"
VERSION: str = "0.1"

APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", 8000))

MINUTE: int = 60
DAY: int = 86400

REFRESH_TOKEN_TTL_SECONDS: int = 30 * DAY
ACCESS_TOKEN_TTL_SECONDS: int = 30 * DAY

DATABASE_URL: str = os.getenv("DATABASE_URL", "postgres://imvbedyroolvuf:5caa670e9db2f7e6205db2ea73c1c3724e24b053a05d69cfc480e2a56fd1ca3b@ec2-54-163-97-228.compute-1.amazonaws.com:5432/dbu2v7tor73q55")
REDIS_CONNECTION_STRING: str = os.getenv('REDIS_CONNECTION_STRING', 'redis://localhost:6379')

SECRET_KEY: str = os.getenv("SECRET_KEY", "1234")
ALGORITHMS_JWT: str = os.getenv("ALGORITHMS_JWT", "HS256")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", 'AC381aea21ea160310da420a70d674458f')
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", '3cafc867be1f9238b050cde709f4e6c4')
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER", '+17634017209')


origins = ["*"]
