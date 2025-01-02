# scripts/my_loading_script.py
from config.config_loader import URI, USERNAME, PASSWORD
from utils.neo4j_connection_sync import Neo4jConnectionSync
from datetime import datetime

def main():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn_sync = Neo4jConnectionSync(URI, USERNAME, PASSWORD)
    conn_sync.connect()

    # Load Person data
    csv_columns = ['id', 'name', 'age', 'nationality']
    cypher_query = """
        CREATE (n:Person {id: row.id, name: row.name, age: toInteger(row.age), nationality: row.nationality})
    """
    conn_sync.create_nodes_from_csv("/data/persons.csv", cypher_query, csv_columns, {})

    # Load Company data and create relationships
    csv_columns_company = ['companyId', 'companyName', 'employeeId']
    cypher_query_company = """
        MATCH (p:Person {id: row.employeeId})
        CREATE (c:Company {id: row.companyId, name: row.companyName})
        CREATE (p)-[:EMPLOYED_AT]->(c)
    """
    conn_sync.create_nodes_from_csv("/data/companies.csv", cypher_query_company, csv_columns_company, {})

    conn_sync.close()

if __name__ == "__main__":
    main()
