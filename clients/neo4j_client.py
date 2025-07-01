from neo4j import GraphDatabase


class Neo4jClient:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def get_driver(self):
        return self.driver

    def close(self):
        self.driver.close()