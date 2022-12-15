FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python todolist/manage.py runserver
# также можно указать EXPOSE 8000 прокидывание порта наружу
#                     ENV PYTHONBUFFERED 1 корректно выдавать логи docker'y
#                     COPY todolist/ .
#                     CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]