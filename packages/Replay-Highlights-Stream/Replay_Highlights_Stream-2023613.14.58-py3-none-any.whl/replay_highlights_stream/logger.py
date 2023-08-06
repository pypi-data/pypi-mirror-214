# ############################################################################################################
#  @author Oliver Consterla Araya                                                                            #
#  @version 2023613.14.58                                                                                    #
#  @since 2023                                                                                               #
# ############################################################################################################

import os
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
log_folder = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_folder, exist_ok=True)
log_file = time.strftime('OutPlayed Replay Stream %d%m%Y %H%M%S.log')
log_path = os.path.join(log_folder, log_file)

def log(message):
    with open(log_path, 'a') as file:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{timestamp}] {message}\n')
        file.write(f'[{timestamp}] {message}\n')

def initialize_log():
    with open(log_path, 'a') as file:
        timestamp = time.strftime('%A %d de %B del %Y %H:%M:%S')
        file.write(f'############## {timestamp} ##############\n')

initialize_log()

try:
    days_threshold = int(config.get('LogSettings', 'DaysThreshold', fallback='3'))
except Exception as e:
    log("La clave 'DaysThreshold' no está definida en el archivo config.ini.")
    log(e)
    days_threshold = 3

def delete_old_logs_name():
    files = os.listdir(log_folder)
    for file in files:
        if file.endswith('.log'):
            file_path = os.path.join(log_folder, file)
            file_date_str = file.split(' ')[3].split('.')[0]  # Extraer la fecha del nombre del archivo
            file_date = time.strptime(file_date_str, '%d%m%Y')  # Convertir la fecha a estructura de tiempo
            current_date = time.localtime()  # Obtener la fecha actual
            file_timestamp = time.mktime(file_date)  # Convertir la fecha del archivo a timestamp
            current_timestamp = time.mktime(current_date)  # Convertir la fecha actual a timestamp
            time_diff = (current_timestamp - file_timestamp) / (24 * 3600)  # Calcular la diferencia en días
            if time_diff > 3:
                os.remove(file_path)

def delete_old_logs_creation_date():
    files = os.listdir(log_folder)
    current_timestamp = time.time()  # Obtener el timestamp actual
    for file in files:
        if file.endswith('.log'):
            file_path = os.path.join(log_folder, file)
            creation_timestamp = os.path.getctime(file_path)  # Obtener el timestamp de creación del archivo
            time_diff = (current_timestamp - creation_timestamp) / (24 * 3600)  # Calcular la diferencia en días
            if time_diff > 3:
                os.remove(file_path)

delete_old_logs_name()
delete_old_logs_creation_date()