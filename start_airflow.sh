#!/bin/bash

# Initialize the database
airflow db init

# Create a user
airflow users create --username admin --password admin --firstname Anonymous --lastname Admin --role Admin --email admin@example.com

# Start the webserver and scheduler in the background
airflow webserver -D &  # -D option to daemonize it
airflow scheduler -D &  # -D option to daemonize it

# Wait forever
wait
