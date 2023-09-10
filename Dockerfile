FROM python:3.10.9-buster

RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN rm requirements.txt
COPY app /app
WORKDIR /app



#EXPOSE 80

#CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]