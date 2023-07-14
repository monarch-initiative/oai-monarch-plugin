FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install poetry
RUN make install export-requirements

CMD ["make", "start"]

