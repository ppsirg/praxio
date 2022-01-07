#https://fastapi.tiangolo.com/pt/deployment/docker/
FROM python:alpine3.7 


EXPOSE 8000

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r  app/requirements.txt

COPY . /app/src


WORKDIR /app/src

ENV PYTHONUNBUFFERED=1



CMD ["uvicorn", "search_engine:app", "--reload","--host", "0.0.0.0", "--port", "8000"]