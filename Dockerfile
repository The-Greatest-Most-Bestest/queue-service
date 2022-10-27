FROM python:3.8.10


COPY src /src

WORKDIR /src

RUN pip install -r requirements.txt

RUN pip install .

WORKDIR /src/queueservice

CMD ["python", "webapp.py"]