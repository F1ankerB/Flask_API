# User API с Docker, MySQL и Nginx

Проект представляет собой API для управления пользователями с использованием Flask, MySQL и Nginx в Docker-контейнерах.
# Технологии

- **Flask**
- **MySQL**
- **Flask-SQLAlchemy**
- **Flask-Migrate**
- **Nginx**
- **Docker**

## Требования

- Docker и Docker Compose
- Доступные порты:
  - 80 (для Nginx)
  - 3306 (для MySQL, внутренний)
  - 5000 (для API, внутренний)

## Установка и запуск
- Клонировать репозиторий.
- Запустить Docker Compose: docker-compose up -d
- Проверить статус: docker-compose ps

## Описание API

### Основные эндпоинты

| Эндпоинт | Метод | Описание | Параметры |
|----------|-------|----------|-----------|
| `/health` | GET | Проверка состояния API | Нет |
| `/api/db_test` | GET | Тест подключения к БД | Нет |
| `/api/register_user` | POST | Регистрация пользователя | JSON с данными пользователя |
| `/api/login` | POST | Авторизация пользователя | JSON с `username` и `password` |
| `/api/logout` | POST | Выход из системы | Нет |
| `/api/get_users` | GET | Получение списка пользователей | Нет |

### CSRF-защита

API использует CSRF-токены для защиты от cross-site request forgery атак. Для любых POST/PUT/DELETE запросов необходимо:

1. Получить CSRF-токен из заголовка ответа `X-CSRF-Token` любого GET запроса
2. Передать полученный токен в заголовке `X-CSRF-Token` при последующих запросах

# Примеры запросов для Postman
## 2. Register User

**Метод**: POST  
**URL**: `http://localhost/api/register_user`  
**Заголовки**:
```
Content-Type: application/json
X-CSRF-Token: csrf_token
```
**Тело запроса**:
```json
{
    "username": "john.doe",
    "password": "secure123",
    "full_name": "John Doe",
    "gender": "male"
}
```

## 3. Login

**Метод**: POST  
**URL**: `http://localhost/api/login`  
**Заголовки**:
```
Content-Type: application/json
X-CSRF-Token: csrf_token
```
**Тело запроса**:
```json
{
    "username": "john.doe",
    "password": "secure123"
}
```

## 5. Logout

**Метод**: POST  
**URL**: `http://localhost/api/logout`  
**Заголовки**:
```
X-CSRF-Token: csrf_token
```
**Тело запроса**: Не требуется

