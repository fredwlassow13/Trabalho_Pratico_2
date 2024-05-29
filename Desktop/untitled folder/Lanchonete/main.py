import random
import threading
import time
from database import Database

# Inicialização do banco de dados
db = Database('bancoiot', 'lanches')
db.resetDatabase()

# Inicialização do semáforo para 3 espátulas
semaforo_espatulas = threading.Semaphore(3)


# Função para simular o preparo de lanches por chapeiros
def prepare_lanche(chapeiro_name, lanche_name, interval):
    while True:
        tempo_preparo = random.uniform(2, 5)  # Tempo de preparo aleatório entre 2 e 5 minutos
        print(chapeiro_name, "está esperando uma espátula para preparar", lanche_name, " ")

        # Aguardar até que uma espátula esteja disponível
        semaforo_espatulas.acquire()
        try:
            print(chapeiro_name, "conseguiu uma espátula e está preparando", lanche_name, " ")

            if tempo_preparo >= 4:  # Limite máximo de tempo de preparo
                db.create(lanche_name, tempo_preparo, 'minutos', True, chapeiro_name)
                print("Atenção! Tempo de preparo muito longo! Verificar", lanche_name, "!")
                break
            else:
                db.create(lanche_name, tempo_preparo, 'minutos', False, chapeiro_name)
        finally:
            # Liberar a espátula após o uso
            semaforo_espatulas.release()

        time.sleep(interval)


# Lista de lanches e seus intervalos de monitoramento
lanches_list = [
    ('Big Mac', 1),
    ('McChicken', 1),
    ('McFish', 1)
]

# Inicialização das threads para os chapeiros
threads = []

# Definindo chapeiros e associando-os aos lanches
chapeiros = ['Chapeiro Pedro', 'Chapeiro Lucas', 'Chapeiro Guima', 'Chapeiro Fred']

for chapeiro_name in chapeiros:
    for lanche_info in lanches_list:
        lanche_name, interval = lanche_info
        # Criar uma nova thread para o chapeiro preparar um lanche específico
        thread = threading.Thread(target=prepare_lanche, args=(chapeiro_name, lanche_name, interval))
        threads.append(thread)

        # Iniciar a execução da thread
        thread.start()

# Aguardar a conclusão de todas as threads
for thread in threads:
    thread.join()