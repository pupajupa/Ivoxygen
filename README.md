# Ivoxygen

[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Welcome+to+my+project+)](https://git.io/typing-svg)

**Ivoxygen** — это веб-приложение, разработанное на Django с использованием API-интеграций и административной панели, предназначенное для автоматизации определённых бизнес-процессов. Проект демонстрирует уверенное владение backend-разработкой, интеграцией внешних сервисов и современным подходом к архитектуре приложений.

## 🚀 Основной функционал

-   Авторизация пользователей
-   Управление сущностями в административной панели
-   Интеграция с внешними API (в зависимости от назначения проекта)
-   Асинхронная обработка задач через Celery и Redis
-   Email-уведомления (SMTP)
-   Логирование и обработка ошибок

## 🛠️ Технологический стек

-   **Язык программирования**: Python 3.10+
-   **Фреймворк**: Django 4.x
-   **База данных**: PostgreSQL
-   **Фоновая обработка задач**: Celery + Redis
-   **Очередь сообщений**: Redis
-   **Фронтенд**: HTML, CSS (Bootstrap)
-   **Интеграции**:
    -   SMTP для отправки email-сообщений
    -   PayPal API для обработки платежей
-   **Docker**: для контейнеризации приложения

## ⚙️ Установка и запуск проекта

1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/pupajupa/Ivoxygen.git
    cd Ivoxygen
    ```
2.  Создайте и активируйте виртуальное окружение
    python3 -m venv venv
    source venv/bin/activate

3.  Установите зависимости

        pip install -r requirements.txt

4.  Выполните миграции и создайте суперпользователя

        python manage.py migrate
        python manage.py createsuperuser

5.  Запустите Redis сервер

        redis-server

6.  Запустите Celery воркер

        celery -A ivo celery worker --loglevel=info

7.  Запустите Django сервер

        python manage.py runserver

8.  Перейдите в браузере по адресу

        http://127.0.0.1:8000/

## 🧪 Тестирование

-   Для запуска тестов используйте:

          python manage.py test

## 📌 Особенности проекта

-   Использование асинхронных задач через Celery (например, отправка email)
-   Интеграция с внешними API
-   Хорошо структурированный и расширяемый backend
-   Возможность масштабирования (благодаря Docker и Celery)
-   Продуманная структура для администрирования и управления

## 💼 Применение в резюме

Проект отлично подходит для демонстрации следующих навыков:

-   Разработка REST API на Django
-   Интеграция внешних API
-   Работа с фоновыми задачами (Celery)
-   Подключение и настройка SMTP и Redis
-   Опыт построения архитектуры Django-проектов
-   Уверенное владение системами контроля версий (Git, GitHub)

## 🧑‍💻 Автор

[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Maksim+Antikhovitch+)](https://git.io/typing-svg)

[👤 GitHub](https://github.com/pupajupa) [💌 Telegram](https://t.me/vyshelpoparit)
