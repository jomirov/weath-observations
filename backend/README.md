## Инструкция по запуску приложения (PowerShell)
### Запуск локального сервера
```powershell
cd backend
py -m venv .venv
.venv/Scripts/activate
python -m pip install -r requirements.txt
uv run fastapi dev
```
### Запросы серверу по токену
Переименовка .env.example -> .env, установка токенов

POST-запрос на создание записи от имени пользователя
```powershell
curl http://localhost:8000/observations `
-Method POST `
-Headers @{"Content-Type"="application/json";"x-token"="TOKEN FROM ENV"} `
-Body '{"city":"Almaty","temperature_C":20,"note":"Sunny"}'
```
GET-запрос на получение всех записей пользователя:
```powershell
curl http://localhost:8000/observations `
-Method GET `
-Headers @{"x-token"="TOKEN FROM ENV"}
```
GET-запрос на получение записи по ID
```powershell
curl http://localhost:8000/observations/1 `
-Method GET `
-Headers @{"x-token"="TOKEN FROM ENV"}
```
DELETE-запрос на удаление записи по ID
```powershell
curl http://localhost:8000/observations `
-Method DELETE `
-Headers @{"x-token"="TOKEN FROM ENV"}
```

## Запуск тестов
```powershell
cd backend
uv run pytest
```