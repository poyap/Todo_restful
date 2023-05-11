FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /code/

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000
CMD [ "python3", "manage.py", "runserver" ]