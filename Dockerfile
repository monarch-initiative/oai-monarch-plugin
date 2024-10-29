FROM python:3.12

WORKDIR /app
RUN pip install poetry

COPY . .

RUN make install export-requirements

CMD ["make", "start-prod"]

