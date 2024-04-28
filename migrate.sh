#!/usr/bin/env bash

# Create the hackspace DB if it doesn't already exist
psql -h localhost -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'hackspace'" | \
    grep -q 1 || psql -h localhost -U postgres -c "CREATE DATABASE hackspace"

# Create the schema_version file if it doesn't exist
if ! [ -e last_migrated.txt ] ; then
    echo -n "-1" > last_migrated.txt
fi

last_migrated_file=$( cat last_migrated.txt )
needs_migrating=false

for file in migration/*
do
    if [ "$last_migrated_file" = file ] || [ "$last_migrated_file" = "-1" ] ; then
        needs_migrating=true
    fi

    if [ "$needs_migrating" = true ] ; then
        echo "Migrating $file"
        psql -h localhost -U postgres -d hackspace -f "$file"
        echo "$file" > last_migrated.txt
    fi
done
