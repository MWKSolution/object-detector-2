FROM python:3.8
RUN mkdir -p /detapp
COPY requirements.txt /detapp/requirements.txt
RUN pip install -r /detapp/requirements.txt
COPY . /detapp
WORKDIR /detapp
RUN chown -R 1000 .
RUN chmod -R 777 .
EXPOSE 8050
USER 1000