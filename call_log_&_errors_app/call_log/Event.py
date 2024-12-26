

class ApiVars:
    """
        Класс для информации о api_vars звонка
    """
    def __init__(self):
        pass  
    

class Event:
    """
        Класс для информации об ивентах звонка
    """
    def __init__(self, evet_type:str, event_end_time:str, event_talk_time:str, event_wait_time:str, event_start_time:str, event_total_time:str,\
                event_answer_time:str, event_rec_filename:str, event_transfered_from:str, event_leg_link_uniqueid_orig:str, apivars:ApiVars):
        
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
        
        self.__apivars = apivars
        
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

