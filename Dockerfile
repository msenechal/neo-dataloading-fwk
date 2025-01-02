# Use the official Airflow image
FROM apache/airflow:2.3.0

# Set the working directory in the container
WORKDIR /usr/local/airflow

# Set the AIRFLOW_HOME environment variable
ENV AIRFLOW_HOME=/usr/local/airflow

# Install any necessary libraries or tools
RUN pip install --no-cache-dir --upgrade pip
# If you need to install additional Python packages, uncomment the next line and list them
RUN pip install --no-cache-dir python-dotenv neo4j-rust-ext

# Copy the airflow configuration file
COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

# Copy your DAGs and scripts into the container
COPY data/ /data/
COPY dags/ ${AIRFLOW_HOME}/dags/
COPY scripts/ ${AIRFLOW_HOME}/scripts/
COPY start_airflow.sh ${AIRFLOW_HOME}/

# Expose the port Airflow web server is reachable on
EXPOSE 8080

ENV PYTHONPATH=${AIRFLOW_HOME}/scripts:$PYTHONPATH
ENV NEO4J_URI=bolt://host.docker.internal:7687
ENV NEO4J_USERNAME=neo4j
ENV NEO4J_PASSWORD=password

# Override the default entrypoint, and use the shell to interpret the script
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["./start_airflow.sh"]
