FROM python:3.12

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app" ,"--host","0.0.0.0"]

