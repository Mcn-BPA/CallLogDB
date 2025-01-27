from .Event import Event


class HTTPEvent(Event):
    """
        Класс для информации об API ивентах звонка
    """
    def __init__(self, event_type:str, event_end_time:str, event_talk_time:str, event_wait_time:str, event_start_time:str, event_total_time:str,
                event_answer_time:str, event_rec_filename:str, event_transfered_from:str, event_leg_link_uniqueid_orig:str, status:str):
        
        
        super().__init__(event_type, event_end_time, event_talk_time, event_wait_time, event_start_time, event_total_time,
                event_answer_time, event_rec_filename, event_transfered_from, event_leg_link_uniqueid_orig)
        
        self.__status = status
        
        
        