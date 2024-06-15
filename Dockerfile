FROM python:3.10.12

WORKDIR /python/simulator
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
WORKDIR /python/simulator/src/locustfiles
CMD [ "sleep" , "infinity" ]