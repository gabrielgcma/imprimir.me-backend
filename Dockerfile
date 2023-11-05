FROM python:3.11
WORKDIR /imprimirme_backend/
COPY . /imprimirme_backend/
RUN pip install --no-cache-dir --upgrade -r /imprimirme_backend/requirements.txt
