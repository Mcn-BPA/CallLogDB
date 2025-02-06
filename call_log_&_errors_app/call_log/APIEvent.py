from .Event import Event


class APIEvent(Event):
    """
        Класс для информации об API ивентах звонка
    """
    def __init__(self, event_type:str, event_end_time:str, event_talk_time:str, event_wait_time:str, event_start_time:str, event_total_time:str,
                event_answer_time:str, event_rec_filename:str, event_transfered_from:str, event_leg_link_uniqueid_orig:str,
                account_id:str, num_a:str, num_b:str, call_id:str, num_c:str, vpbx_id:str, scenario_id:str, scenario_counter:str, 
                did:str, dtmf:str, ivr_object_id:str, ivr_schema_id:str, linked_id:str, robocall_id:str, 
                robocall_target_number:str, robocall_task_contact_id:str, robocall_task_id:str,
                stt_answer:str, n8n_success:str):
        
        
        super().__init__(event_type, event_end_time, event_talk_time, event_wait_time, event_start_time, event_total_time,
                event_answer_time, event_rec_filename, event_transfered_from, event_leg_link_uniqueid_orig)
        
        self.__account_id = account_id
        self.__num_a = num_a
        self.__num_b = num_b
        self.__call_id = call_id
        self.__num_c = num_c
        self.__vpbx_id = vpbx_id
        self.__scenario_id = scenario_id
        self.__scenario_counter = scenario_counter
        self.__did = did
        self.__dtmf = dtmf
        self.__ivr_object_id = ivr_object_id
        self.__ivr_schema_id = ivr_schema_id
        self.__linked_id = linked_id
        self.__robocall_id = robocall_id
        self.__robocall_target_number = robocall_target_number
        self.__robocall_task_contact_id = robocall_task_contact_id
        self.__robocall_task_id = robocall_task_id
        self.__stt_answer = stt_answer
        self.__n8n_success = n8n_success


    def get_account_id(self):
        """Получение id аккаунта

        Returns:
            str: __account_id звонка
        """
        return self.__account_id

    def get_num_a(self):
        """Получение номера того, кто звонил

        Returns:
            str: __num_a звонка
        """
        return self.__num_a
    
    def get_num_b(self):
        """Получение номера на который звонили

        Returns:
            str: __num_b звонка
        """
        return self.__num_b
    
    def get_call_id(self):
        """Получение call_id звонка

        Returns:
            str: __call_id звонка
        """
        return self.__call_id
    
    def get_num_c(self):
        """Получение номера, на которого перевели вызов

        Returns:
            str: __num_c звонка
        """
        return self.__num_c
    
    def get_vpbx_id(self):
        """Получение айди ВАТСа

        Returns:
            str: __vpbx_id звонка
        """
        return self.__vpbx_id

    def get_scenario_id(self):
        """Получение id сценария

        Returns:
            str: __scenario_id звонка
        """
        return self.__scenario_id
    
    def get_scenario_counter(self):
        """Получение Счетчик сценария

        Returns:
            str: __scenario_counter звонка
        """
        return self.__scenario_counter
    
    def get_did(self):
        """Получение номера того, кто звонил

        Returns:
            str: __did звонка
        """
        return self.__did
    
    def get_dtmf(self):
        """Получение был ли донабор по dtmf от клиента

        Returns:
            str: __dtmf звонка
        """
        return self.__dtmf
    
    def get_ivr_object_id(self):
        """Получение айди объекта на сценарии, техническая информация

        Returns:
            str: __ivr_object_id звонка
        """
        return self.__ivr_object_id
    
    def get_ivr_schema_id(self):
        """Получение id сценарий звонка

        Returns:
            str: __ivr_schema_id звонка
        """
        return self.__ivr_schema_id
    
    def get_linked_id(self):
        """Получение айди цельного звонка

        Returns:
            str: __linked_id звонка
        """
        return self.__linked_id
    
    def get_robocall_id(self):
        """Получение айди робокола

        Returns:
            str: __robocall_id звонка
        """
        return self.__robocall_id
    
    def get_robocall_target_number(self):
        """Получение номера, на который звонит робокол

        Returns:
            str: __robocall_target_number звонка
        """
        return self.__robocall_target_number
    
    def get_robocall_task_contact_id(self):
        """Получение айди этого номера в базе робокола

        Returns:
            str: __robocall_task_contact_id звонка
        """
        return self.__robocall_task_contact_id
    
    def get_robocall_task_id(self):
        """Получение айди задания робокола

        Returns:
            str: __robocall_task_id звонка
        """
        return self.__robocall_task_id
    
    def get_stt_answer(self):
        """Получение ответа звонившего

        Returns:
            str: __stt_answer звонка
        """
        return self.__stt_answer
    
    def get_n8n_success(self):
        """Получение статуса доступности n8n

        Returns:
            str: __n8n_success звонка
        """
        return self.__n8n_success

