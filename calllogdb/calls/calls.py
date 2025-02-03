import json
from calllogdb.types import Call, Events
from typing import List


class Calls:
    def __init__(self):
        self.calls: List[Call] = []  # Список для хранения звонков

    @staticmethod
    def parse_json(json_data: str) -> Call:
        """Парсит JSON-объект в Call."""
        data = json.loads(json_data)
        id_ = data["id"]
        did = data.get("did", "")
        dst_num = data.get("dst_num", "")
        events = [Events.from_dict(event_data)
                  for event_data in data.get("events", [])]
        return Call(id_=id_, did=did, dst_num=dst_num, events=events, **data)

    def add_call(self, json_data: str):
        """Добавляет один звонок в массив calls."""
        call = self.parse_json(json_data)
        self.calls.append(call)

    def add_calls(self, json_array: str):
        """Добавляет массив звонков."""
        data_list = json.loads(json_array)
        for item in data_list:
            self.add_call(json.dumps(item))
