FROM python:3.11-bullseye
RUN apt-get -y update

RUN mkdir app

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENV LISTEN_PORT 80
EXPOSE 80

CMD ["streamlit", "run", "app.py", "--server.port", "80", "--server.maxUploadSize", "3"]