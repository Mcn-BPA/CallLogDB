import configparser

class  Error:
    """
        Класс для информации об ошибках
    """
    def __init__(self, script_path:str, error_code:str, error_text:str, error_date:str):
        config = configparser.ConfigParser()
        config.read('settings/setting.ini')
        
        self.__error_code = error_code
        self.__error_text = error_text
        self.__error_date = error_date
        self.__script_path = script_path
        self.__client_ls = config['DATA_CLIENT']['client_ls']
        self.__client_name = config['DATA_CLIENT']['client_name']
        self.__server_name = config['DATA_CLIENT']['server_name']
    
    def get_error_code(self):
        """Возвращает код ошибки

        Returns:
            str: Код ошибки
        """
        return self.__error_code
    
    def get_error_text(self):
        """Возвращает описание ошибки

        Returns:
            str: Описание ошибки
        """
        return self.__error_text
        
    def get_error_date(self):
        """Возвращает дату и время ошибки

        Returns:
            str: Дата и время ошибки
        """
        return self.__error_date
    
    def get_client_ls(self):
        """Возвращает лицевой счет клиента

        Returns:
            str: Лицевой счет клиента
        """
        return self.__client_ls
    
    def get_client_name(self):
        """Возвращает название клиента

        Returns:
            str: Название клиента
        """
        return self.__client_name
    
    def get_script_path(self):
        """Возвращает путь к файлу с ошибкой

        Returns:
            str: Путь к файлу с ошибкой
        """
        return self.__script_path
    
    def get_server_name(self):
        """Возвращает название хоста со скриптом

        Returns:
            str: Название хоста со скриптом
        """
        return self.__server_name
