FROM python:alpine3.17

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]

CMD ["run.py"]