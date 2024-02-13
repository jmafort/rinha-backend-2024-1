FROM python:3.11

COPY requirements.txt /
RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt
COPY . /app
WORKDIR /app

EXPOSE 9000
EXPOSE 9001

CMD ["python3.11", "app.py"]
