#!/bin/bash

# Run migrations
python src/migrations.py

# Start Flask application
python src/api.py