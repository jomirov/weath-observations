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
POST-запрос на создание записи от имени пользователя-А
```powershell
curl http://localhost:8000/observations `
-Method POST `
-Headers @{"Content-Type"="application/json";"x-token"="TEST-TOKEN-A"} `
-Body '{"city":"Almaty","temperature_C":20,"note":"Sunny"}'
```
GET-запрос на получение всех записей пользователя-А:
```powershell
curl http://localhost:8000/observations `
-Method GET `
-Headers @{"x-token"="TEST-TOKEN-A"}
```
GET-запрос на получение записи по ID
```powershell
curl http://localhost:8000/obseravations/1 `
-Method GET `
-Headers @{"x-token"="TEST-TOKEN-A"}
```
DELETE-запрос на удаление записи по ID
```powershell
curl http://localhost:8000/observations `
-Method DELETE `
-Headers @{"x-token"="TEST-TOKEN-A"}
```

## Запуск тестов
```powershell
cd backend
uv run pytest
```