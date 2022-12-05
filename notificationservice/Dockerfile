FROM python:3.8.10

WORKDIR /ns

COPY ["*.py", "./"]

# COPY config/ ./config/
COPY templates/ ./templates/

COPY ["requirements.txt", "./"]

RUN pip install -r requirements.txt
RUN pip install .

# CMD ["/bin/bash"]

CMD ["python", "main.py"]