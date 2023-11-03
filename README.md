Перед початком роботи переконайтеся, що встановлені наступні компоненти та залежності з pyproject.toml

## Встановлення та налаштування

1. Склонуйте репозиторій проекту на свій локальний комп'ютер.
2. Встановіть необхідні залежності
3. В каталозі проекту створіть файл .env та додайте туди свої дані за таким шаблоном:
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_PORT=
SQLALCHEMY_DATABASE_URL=
SECRET_KEY=
ALGORITHM=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_PORT=
MAIL_SERVER=
REDIS_HOST=
REDIS_PORT=
CLOUDINARY_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
4. Створіть підключення до бази даних Postgres та Redis за допомогою команди  docker-compose up
5. Запустіть сервер командою uvicorn main:app --reload
6. Відкрийте документацію Swagger за посиланням http://localhost:8000/docs. Також для авторизації та виконання запитів можна використовувати Postman.


