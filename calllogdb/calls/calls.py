import json

from calllogdb.types import Call


class Calls:
    def __init__(self) -> None:
        self.calls: list[Call] = []

    @staticmethod
    def parse_json(json_data: str) -> Call:
        """Парсит JSON-строку в объект Call, используя Call.from_dict."""
        data = json.loads(json_data)
        return Call.from_dict(data)

    def add_call(self, json_data: str) -> None:
        """Добавляет один звонок в список calls."""
        call = self.parse_json(json_data)
        self.calls.append(call)

    def add_calls(self, json_array: str) -> None:
        """Добавляет несколько звонков из JSON-массива."""
        data_list = json.loads(json_array)
        for data in data_list:
            self.calls.append(Call.from_dict(data))
