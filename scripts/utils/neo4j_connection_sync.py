import csv
from neo4j import GraphDatabase, basic_auth
import datetime

class Neo4jConnectionSync:
    def __init__(self, uri, user, password):
        self.__uri = uri
        self.__user = user
        self.__password = password
        self.__driver = None

    def connect(self):
        if not self.__driver:
            self.__driver = GraphDatabase.driver(
                self.__uri,
                auth=basic_auth(self.__user, self.__password)
            )
            print("Connected to the database (Sync).")

    def close(self):
        if self.__driver:
            self.__driver.close()
            print("Connection closed (Sync).")
    
    def create_nodes_from_csv(self, file_path, query_template, csv_columns, cypher_params, batch_size=500):
        start_time = datetime.datetime.now()
        print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        with self.__driver.session() as session:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                data = [row for row in reader if all(col in row for col in csv_columns)]

            iterate_query = f"""
            CALL apoc.periodic.iterate(
                'UNWIND $rows AS row RETURN row',
                '{query_template}',
                {{params:{{rows: $rows}}, batchSize: $batchSize, iterateList: true, parallel: false}}
            )
            YIELD batches, total, errorMessages, failedBatches, retries, committedOperations, timeTaken
            RETURN batches, total, errorMessages, failedBatches, retries, committedOperations, timeTaken
            """
            result = session.run(iterate_query, {'rows': data, 'batchSize': batch_size})
            summary = result.single()

        end_time = datetime.datetime.now()
        print(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        execution_time = end_time - start_time
        print(f"Execution Time: {execution_time}")

        # Print the results from the Neo4j operation
        print(f"Batches processed: {summary['batches']}")
        print(f"Total operations processed: {summary['total']}")
        print(f"Committed operations: {summary['committedOperations']}")
        print(f"Failed batches: {summary['failedBatches']}")
        print(f"Retries: {summary['retries']}")
        print(f"Time taken: {summary['timeTaken']}")
        if summary['errorMessages']:
            print(f"Error Messages: {summary['errorMessages']}")
