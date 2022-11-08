FROM python:3.8.10

COPY ["*.py", "./"]

COPY config/ ./

COPY ["requirements.txt", "./"]

RUN pip install -r requirements.txt
RUN pip install .

CMD ["python", "main.py"]