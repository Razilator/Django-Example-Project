FROM python:3.10.6-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Обновление системы
RUN apt-get update
RUN apt-get -y install postgresql-client gcc

# Обновление pip python
RUN pip install --upgrade pip

# Установка требований

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

# Рабочий каталог

WORKDIR /app

# Копирование проекта

COPY . .
