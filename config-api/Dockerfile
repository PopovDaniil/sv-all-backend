FROM python:3.7-alpine

EXPOSE 80

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY config-api/ config-api/
COPY common/ common/

WORKDIR /usr/src/app/config-api
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]