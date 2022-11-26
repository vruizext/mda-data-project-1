#!/bin/bash
psql -U postgres -c "DROP DATABASE IF EXISTS $POSTGRES_DB;"
createdb -U $POSTGRES_USER $POSTGRES_DB
psql -U postgres -d $POSTGRES_DB -f iip_db.sql