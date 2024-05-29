import pymongo

class Database:
    def _init_(self, database, collection):
        self.connect(database, collection)

    def connect(self, database, collection):
        try:
            connectionString = "localhost:27017"
            self.clusterConnection = pymongo.MongoClient(
                connectionString,
                tlsAllowInvalidCertificates=True
            )
            self.db = self.clusterConnection[database]
            self.collection = self.db[collection]
            print("Banco de Dados conectado com sucesso")
        except Exception as e:
            print(e)

    def resetDatabase(self):
        try:
            self.db.drop_collection(self.collection)
            print("Banco de dados resetado com sucesso")
        except Exception as e:
            print(e)

    def create(self, lanche, tempo_preparo, unidade, lanche_em_atraso, chapeiro):
        return self.collection.insert_one(
            {"Lanche": lanche, "Tempo de Preparo": tempo_preparo, "Unidade de Medida": unidade, "Lanche em Atraso": lanche_em_atraso, "Chapeiro": chapeiro})