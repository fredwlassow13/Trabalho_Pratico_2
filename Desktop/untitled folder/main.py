import threading
import time
import random
from statistics import mean

# Função para simular a execução de um processo
def execute_process(process_id, burst_time, start_times, end_times, burst_times, wait_times, lock):
    # Inicia o cronômetro quando o processo começa a ser executado
    start_time = time.time()

    # Simula a execução do processo por um determinado tempo (burst_time)
    time.sleep(burst_time)

    # Finaliza o cronômetro quando o processo termina de ser executado
    end_time = time.time()

    # Adquire o lock para garantir exclusão mútua na atualização das estruturas de dados compartilhadas
    with lock:
        # Armazena os tempos de início, fim e burst do processo atual
        start_times[process_id] = start_time
        end_times[process_id] = end_time
        burst_times[process_id] = burst_time

        # Calcula o tempo de espera do processo
        wait_time = start_time - start_times['simulation_start']
        wait_times[process_id] = wait_time

    # Imprime informações sobre a conclusão do processo
    print(f"Processo {process_id} terminou em {burst_time:.2f} segundos. Tempo de espera: {wait_time:.2f} segundos.")

# Função para escalonamento FCFS (First-Come, First-Served)
def fcfs_scheduling(processes):
    # Inicializa as estruturas de dados para armazenar os tempos de início, fim, burst e espera dos processos
    start_times = {'simulation_start': time.time()}
    end_times = {}
    burst_times = {}
    wait_times = {}

    # Utiliza um lock para garantir a exclusão mútua ao acessar as estruturas de dados compartilhadas
    lock = threading.Lock()

    # Itera sobre os processos na ordem em que são fornecidos
    previous_end_time = start_times['simulation_start']
    for process_id, burst_time in processes:
        # Cria uma nova thread para executar o processo
        thread = threading.Thread(target=execute_process, args=(
            process_id, burst_time, start_times, end_times, burst_times, wait_times, lock))
        thread.start()
        thread.join()  # Espera pelo término da thread antes de continuar
        previous_end_time = end_times.get(process_id)

    # Calcula o tempo médio de espera e de execução dos processos
    avg_wait_time = mean(wait_times.values()) if wait_times else 0
    avg_execution_time_fcfs = mean(burst_times.values()) if burst_times else 0

    return avg_wait_time, avg_execution_time_fcfs

# Função para escalonamento SJF (Shortest Job First)
def sjf_scheduling(processes):
    # Inicializa as estruturas de dados para armazenar os tempos de início, fim, burst e espera dos processos
    start_times = {'simulation_start': time.time()}
    end_times = {}
    burst_times = {}
    wait_times = {}

    # Utiliza um lock para garantir a exclusão mútua ao acessar as estruturas de dados compartilhadas
    lock = threading.Lock()

    # Ordena os processos com base no tempo de burst
    processes = sorted(processes, key=lambda x: x[1])

    # Itera sobre os processos ordenados
    previous_end_time = start_times['simulation_start']
    for process_id, burst_time in processes:
        # Cria uma nova thread para executar o processo
        thread = threading.Thread(target=execute_process, args=(
            process_id, burst_time, start_times, end_times, burst_times, wait_times, lock))
        thread.start()
        thread.join()  # Espera pelo término da thread antes de continuar
        previous_end_time = end_times.get(process_id)

    # Calcula o tempo médio de espera e de execução dos processos
    avg_wait_time = mean(wait_times.values()) if wait_times else 0
    avg_execution_time_sjf = mean(burst_times.values()) if burst_times else 0

    return avg_wait_time, avg_execution_time_sjf

# Simulação de processos com tempos de burst aleatórios
processes = [(i, random.uniform(1, 5)) for i in range(10)]

# Imprime o tamanho da lista de processos
print(f"Tamanho da lista de processos: {len(processes)}\n")

# Execução do escalonamento FCFS (First-Come, First-Served)
print("Executando FCFS...")
avg_wait_time_fcfs, avg_execution_time_fcfs = fcfs_scheduling(processes)
print(f"Tempo médio de espera (FCFS): {avg_wait_time_fcfs:.2f} segundos.")
print(f"Tempo médio de execução (FCFS): {avg_execution_time_fcfs:.2f} segundos.\n")

# Execução do escalonamento SJF (Shortest Job First)
print("Executando SJF...")
avg_wait_time_sjf, avg_execution_time_sjf = sjf_scheduling(processes)
print(f"Tempo médio de espera (SJF): {avg_wait_time_sjf:.2f} segundos.")
print(f"Tempo médio de execução (SJF): {avg_execution_time_sjf:.2f} segundos.\n")

# Comparação dos resultados
if avg_wait_time_fcfs < avg_wait_time_sjf:
    print("FCFS teve um tempo de espera médio menor.")
else:
    print("SJF teve um tempo de espera médio menor.")