import configparser
from Error import Error
import psycopg2

class AddError:
    
    def __init__(self, file_name:str, error_code:str, error_text:str, error_date:str, config_path = 'settings/setting.ini'):
        self.__error = Error(file_name, error_code, error_text, error_date)
        self.__config_path = config_path
        
    def __set_connection(self):
        """Создание подключения

        Returns:
            psycopg2: Подключение к БД
        """        
        try:
            # Загрузка настроек подключения
            __config = configparser.ConfigParser()
            __config.read(self.__config_path)

            db_params = {
            'dbname': __config['DATA_DB_ERROR']['database'],
            'user': __config['DATA_DB_ERROR']['user'],
            'password': __config['DATA_DB_ERROR']['password'],
            'host': __config['DATA_DB_ERROR']['host'],
            'port': int(__config['DATA_DB_ERROR']['port'])
            }
            source_conn = psycopg2.connect(**db_params)
            
            return source_conn
        except Exception as e:
            self.__log.error(f"❌Ошибка подключения к базе данных: {e}")   
        
        
    def add_error_to_db(self):
        """
            Добавление ошибки в БД
        """
        
        try:
            client_ls = self.__error.get_client_ls()
            client_name = self.__error.get_client_name()
            script_path = self.__error.get_script_path()
            error_code = self.__error.get_error_code()
            error_text = self.__error.get_error_text()
            error_date = self.__error.get_error_date()
            server_name = self.__error.get_server_name()
            
            __config = configparser.ConfigParser()
            __config.read(self.__config_path)
            
            conn = self.__set_connection()
            cursor = conn.cursor()
            
            # Начало транзакции
            cursor.execute("BEGIN;")
            
            cursor.execute(f'''
                INSERT INTO {__config['DATA_DB_ERROR']['table_name']} (client_ls, client_name, script_path, error_code, error_text, error_date, server_name)
                VALUES ({client_ls}, {client_name}, {script_path}, {error_code}, {error_text}, {error_date}, {server_name});
                ''')
                
            # Фиксация транзакции
            cursor.execute("COMMIT;")
            self.__log.info("✅ Данные записаны в БД")
        
        except Exception as e:
            # Откат транзакции в случае ошибки
            cursor.execute("ROLLBACK;")
            self.__log.error(f"❌Ошибка выполнения запроса записы в БД: {e}")
            
        finally:
            # Закрытие курсора и соединения
            cursor.close()
            conn.close()     
