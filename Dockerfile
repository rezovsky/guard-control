FROM postgres:latest

ENV POSTGRES_USER=guard
ENV POSTGRES_PASSWORD=12345
ENV POSTGRES_DB=guard

EXPOSE 5432

COPY init.sql /docker-entrypoint-initdb.d/

