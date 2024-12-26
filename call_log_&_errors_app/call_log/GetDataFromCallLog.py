import configparser


class Day:
    """
        Класс с информацией о звонках за день
    """
    def __init__(self):
        self.__calls = []
        
    def add_call(self, call):
        """Добавление звонка в список

        Args:
            call (Call): Звонок
        """
        self.__calls.append(call)
    
    def get_calls(self):
        """Возвращает список звонков за день

        Returns:
            list: Список звонков за день
        """
        return self.__calls


class GetDataFromCallLog:
    """
        Класс для получения данных из коллога
    """
    def __init__(self, start_date, end_date, config_path = 'settings/setting.ini'):
        
        __config = configparser.ConfigParser()
        __config.read(config_path)
        
        
        account_id_ls = __config['DATA_CLIENT']['client_ls']
        vpbx_id = __config['DATA_CLIENT']['vpbx_id']
        
        
        API_URL = f'https://api.mcn.ru/v2/rest/account/{account_id_ls}/vpbx/{vpbx_id}/call_log'
        
        self.__get_call_log_data(start_date, end_date, API_URL)
        
        
    def __get_call_log_data(self, start_date, end_date, API_URL):
        """
            Функция для получения данных из коллога

        Args:
            start_date (str): Дата начала выгрузки данных
            end_date (str): Дата конца выгрузки данных
            API_URL (str): Ссылка для получения данных
        """
        pass #! Нужно написать с использованием лимита
