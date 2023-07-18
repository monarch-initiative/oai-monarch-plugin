FROM python:3.10

WORKDIR /app
RUN pip install poetry

COPY . .

RUN make install export-requirements

CMD ["make", "start-prod"]

