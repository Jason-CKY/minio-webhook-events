FROM python:3.10 as dev

WORKDIR /code

COPY ./deploy/api/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

COPY ./src/api /code/app

CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]


FROM dev as production

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
