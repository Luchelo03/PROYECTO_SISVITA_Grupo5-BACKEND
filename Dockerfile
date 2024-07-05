FROM python:3.8.0

COPY ./ /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5432

CMD ["python3","-m","flask","run","--host=0.0.0.0"]