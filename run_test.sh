#!/usr/bin/env bash

source venv/bin/activate
export DATABASE_URL_TEST=postgresql://mmg-user:mmg-pwd@localhost:5433/mmg-db
pytest tests/