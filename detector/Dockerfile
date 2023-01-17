FROM python:3.8
RUN mkdir -p /detapi
COPY requirements.txt /detapi/requirements.txt
RUN pip install -r /detapi/requirements.txt
COPY . /detapi
WORKDIR /detapi
RUN chown -R 1000 .
RUN chmod -R 777 .
EXPOSE 8066
USER 1000
CMD uvicorn detapi:app --host 0.0.0.0 --port 8066
