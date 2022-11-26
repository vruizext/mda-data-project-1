#!/bin/bash
dropdb -U postgres -f $POSTGRES_DB && createdb -U $POSTGRES_USER $POSTGRES_DB && psql -U postgres -d $POSTGRES_DB -f iip_db.sql