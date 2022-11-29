FROM postgres:14-alpine
COPY entrypoint docker-entrypoint-initdb.d
COPY scripts usr/local/bin
RUN chmod +x usr/local/bin/reset_db.sh