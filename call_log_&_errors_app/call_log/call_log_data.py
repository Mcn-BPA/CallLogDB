from logger import setup_logger
import configparser

class Call:
    """
        Класс c информацией о звонке
    """
    def __init__(self, callid:str, type:str, status:str, hangup_reason:str, date:str, answer_date:str, end_date:str, billsec:str,
                talktime:str, waittime:str, dst_num:str, dst_name:str, dst_type:str, src_num:str, src_name:str, src_type:str,
                did:str, did_num:str, events_count:str, has_record:str):
                                
                                #* Пример:
        self.__callid = callid  # '116-1734905090.27079126'
        self.__type = type      # 'inb'
        self.__status = status  # 'ANSWERED'
        self.__hangup_reason = hangup_reason # 'ANSWER'
        self.__date = date               # '2024-12-23 01:04:50'
        self.__answer_date = answer_date # '2024-12-23 01:04:50'
        self.__end_date = end_date       # '2024-12-23 01:06:39'
        self.__billsec = billsec   # 109
        self.__talktime = talktime # 94
        self.__waittime = waittime # 15
        self.__dst_num = dst_num   # '18'
        self.__dst_name = dst_name # 'Оператор 4'
        self.__dst_type = dst_type # 'sipdevice'
        self.__src_num = src_num   # '79140270777'
        self.__src_name = src_name # '79140270777'
        self.__src_type = src_type # 'pstn'
        self.__did = did           # 78006003897
        self.__did_num = did_num   # 78006003897
        self.__events_count = events_count # 6
        self.__has_record = has_record # 1

        self.__last_event = None
        self.__events = []  
        self.__apivars = [] 
        
    def get_callid(self):
        """Возвращает call_id звонка

        Returns:
            str: call_id звонка
        """
        return self.__callid
    
    def get_type(self):
        """Возвращает тип звонка

        Returns:
            str: Тип звонка
        """
        return self.__type
    
    def get_status(self):
        """Возвращает статус звонка

        Returns:
            str: Статус звонка
        """
        return self.__status
    
    def get_hangup_reason(self):
        """Возвращает статус поднятия трубки

        Returns:
            str: Статус поднятия трубки
        """
        return self.__hangup_reason
    
    def get_date(self):
        """Возвращает дата звонка

        Returns:
            str: Дата звонка
        """
        return self.__date
    
    def get_answer_date(self):
        """Возвращает дату поднятия трубки

        Returns:
            str: Дата поднятия трубки
        """
        return self.__answer_date
    
    def get_end_date(self):
        """Возвращает дату окончания звонка

        Returns:
            str: Дата окончания звонка
        """
        return self.__end_date
    
    def get_billsec(self):
        """Возвращает время звонка в секундах

        Returns:
            str: Время звонка в секундах

        """
        return self.__billsec
    
    def get_talktime(self):
        """Возвращает время разговора в секундах

        Returns:
            str: call_id Время разговора в секундах
        """
        return self.__talktime
    
    def get_waittime(self):
        """Возвращает время ожидания в секундах

        Returns:
            str: Время ожидания в секундах
        """
        return self.__waittime
    
    def get_dst_num(self):
        """Возвращает номер ответа

        Returns:
            str: Номер ответа
        """
        return self.__dst_num
    
    def get_dst_name(self):
        """Возвращает название ответившего

        Returns:
            str: Название ответившего
        """
        return self.__dst_name
    
    def get_dst_type(self):
        """Возвращает тип отвеченного аппарата

        Returns:
            str: Тип отвеченного аппарата
        """
        return self.__dst_type
    
    def get_src_num(self):
        """Возвращает номер, с которого звонили

        Returns:
            str: Номер, с которого звонили
        """
        return self.__src_num
    
    def get_src_name(self):
        """Возвращает название номера, с которого звонили

        Returns:
            str: Название номера, с которого звонили
        """
        return self.__src_name
    
    def get_src_type(self):
        """Возвращает тип звонившего

        Returns:
            str: Тип звонившего
        """
        return self.__src_type
    
    def get_did(self):
        """Возвращает номер, на который звонят

        Returns:
            str: Номер, на который звонят
        """
        return self.__did
    
    def get_did_num(self):
        """Возвращает название номера, на который звонят

        Returns:
            str: Название номера, на который звонят
        """
        return self.__did_num
    
    def get_events_count(self):
        """Возвращает количество ивентов

        Returns:
            str: Количество ивентов
        """
        return self.__events_count
    
    def get_has_record(self):
        """Возвращает флаг записи звонка

        Returns:
            str: Флаг записи звонка
        """
        return self.__has_record
    
    def get_events(self):
        """Возвращает список ивентов звонка

        Returns:
            str: Ивенты звонка
        """
        return self.__events
    
    def get_apivars(self):
        """Возвращает данные элемента apivars звонка

        Returns:
            str: Данные элемента apivars звонка
        """
        return self.__apivars
    
    def get_last_event(self):
        """Возвращает данные о последнем ивенте
        Returns:
            str: Данные о последнем ивенте
        """
        return self.__last_event
        
    def add_event(self, event):
        """Добавление ивента

        Args:
            event (Event): Ивент
        """
        self.__events.append(event)
    
    def add_apivars(self, apivars):
        """Добавление данных из элемента apivars

        Args:
            apivars (ApiVars): Элемент apivars
        """
        self.__apivars.append(apivars)
    
    def add_last_event(self, event):
        """Добавление последнего ивента

        Args:
            event (Event): Ивент
        """
        self.__last_event = event


class Event:
    """
        Класс для информации об ивентах звонка
    """
    def __init__(self, evet_type:str, event_end_time:str, event_talk_time:str, event_wait_time:str, event_start_time:str, event_total_time:str,\
                event_answer_time:str, event_rec_filename:str, event_transfered_from:str, event_leg_link_uniqueid_orig:str):
        
        self.__evet_type = evet_type
        self.__event_end_time = event_end_time
        self.__event_talk_time = event_talk_time
        self.__event_wait_time = event_wait_time
        self.__event_start_time = event_start_time
        self.__event_total_time = event_total_time
        self.__event_answer_time = event_answer_time
        self.__event_rec_filename = event_rec_filename
        self.__event_transfered_from = event_transfered_from
        self.__event_leg_link_uniqueid_orig = event_leg_link_uniqueid_orig
        
    def get_evet_type(self):
        """Возвращает тип ивента

        Returns:
            str: Тип ивента
        """
        return self.__evet_type
    
    def get_event_end_time(self):
        """Возвращает дату и время конца ивента

        Returns:
            str: Дата и время конца ивента
        """
        return self.__event_end_time
    
    def get_event_talk_time(self):
        """Возвращает время разговора

        Returns:
            str: Время разговора
        """
        return self.__event_talk_time
    
    def get_event_wait_time(self):
        """Возвращает время ожидания

        Returns:
            str: Время ожидания
        """
        return self.__event_wait_time
    
    def get_event_start_time(self):
        """Возвращает дату и время начала ивента

        Returns:
            str: Дата и время начала ивента
        """
        return self.__event_start_time
    
    def get_event_total_time(self):
        """Возвращает итоговое время ивента

        Returns:
            str: Итоговое время ивента
        """
        return self.__event_total_time
    
    def get_event_answer_time(self):
        """Возвращает время ответа

        Returns:
            str: Время ответа
        """
        return self.__event_answer_time
    
    def get_event_rec_filename(self):
        """Возвращает название файла записи

        Returns:
            str: Название файла записи
        """
        return self.__event_rec_filename
    
    def get_event_transfered_from(self):
        """Возвращает номер, с которого был перевод

        Returns:
            str: Номер, с которого был перевод
        """
        return self.__event_transfered_from
    
    def get_event_leg_link_uniqueid_orig(self):
        """Возвращает данные типа '116-1734911399.27080188'

        Returns:
            str: Данные типа '116-1734911399.27080188'
        """
        return self.__event_leg_link_uniqueid_orig

    
class ApiVars:
    """
        Класс для информации о api_vars звонка
    """
    def __init__(self):
        pass    


class Day:
    """
        Класс с информацией о звонках за день
    """
    def __init__(self):
        self.__calls = []
        
    def add(self, call):
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
    def __init__(self, start_date, end_date):
        # * инициализация логера
        self.__log = setup_logger()
        __CONFIG_PATH = 'settings/setting.ini'
        
        __config = configparser.ConfigParser()
        __config.read(__CONFIG_PATH)
        
        
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
