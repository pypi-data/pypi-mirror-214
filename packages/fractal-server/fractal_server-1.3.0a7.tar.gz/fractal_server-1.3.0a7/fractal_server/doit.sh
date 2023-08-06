#!/bin/bash

export SQLITE_PATH=/tmp/test.db

rm -f /tmp/test.db
poetry run fractalctl set-db

poetry run alembic revision --autogenerate

rm -f /tmp/test.db
poetry run fractalctl set-db
