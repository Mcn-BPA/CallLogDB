# from datetime import datetime

# import pytest

# from calllogdb.types.event import (
#     AnnounceEvent,
#     BlackListEvent,
#     GptEvent,
#     HangupEvent,
#     HTTPEvent,
#     IvrEvent,
#     QueueEvent,
#     SpeechRecogEvent,
#     UnknownEvent,
# )


# @pytest.fixture
# def mock_data():
#     return {
#         "event_additional_info": {
#             "message": "Test message",
#             "target_number": "1234567890",
#             "exten": "1234",
#             "api_vars": '{"key": "value"}',
#         },
#         "event_answer_time": "2025-04-15T12:00:00Z",
#         "speechkit_dialog": [{"dialog_value": "How are you?"}, {"dialog_value": "I'm fine"}],
#     }


# def test_announce_event_from_dict(mock_data):
#     data = {"event_additional_info": {}}
#     event = AnnounceEvent.from_dict(data)
#     assert isinstance(event, AnnounceEvent)
#     assert event.__class__.__name__ == "AnnounceEvent"


# def test_hangup_event_from_dict(mock_data):
#     data = {"event_additional_info": {}}
#     event = HangupEvent.from_dict(data)
#     assert isinstance(event, HangupEvent)
#     assert event.__class__.__name__ == "HangupEvent"


# def test_ivr_event_from_dict(mock_data):
#     data = {"event_additional_info": {}}
#     event = IvrEvent.from_dict(data)
#     assert isinstance(event, IvrEvent)
#     assert event.__class__.__name__ == "IvrEvent"


# def test_gpt_event_from_dict(mock_data):
#     data = {
#         "event_additional_info": {
#             "api_vars": """{account_id:133429,num_a:12396,num_b:88002344499,call_id:116-1741694432.6016962,num_c:null,
#             short_num_found:false,vpbx_id:16884,scenario_id:34056,scenario_counter:1,
#             scenario_client_variables_1:{short_num_found:false,vpbx_id:16884},
#             scenario_id_1:34056,dest_link_name:,did:12396,dtmf:,ivr_object_id:318,
#             ivr_schema_id:34056,linked_id:116-1741694432.6016962,robocall_id:0,
#             robocall_target_number:,robocall_task_contact_id:0,robocall_task_id:0,stt_answer:,n8n_success:true}"""
#         }
#     }
#     event = GptEvent.from_dict(data)
#     assert isinstance(event, GptEvent)
#     assert event.api_vars == {
#         "account_id": "133429",
#         "num_a": "12396",
#         "num_b": "88002344499",
#         "call_id": "116-1741694432.6016962",
#         "num_c": "null",
#         "short_num_found": "false",
#         "vpbx_id": "16884",
#         "scenario_id": "34056",
#         "scenario_counter": "1",
#         "scenario_client_variables_1": "short_num_found:false",
#         "scenario_id_1": "34056",
#         "dest_link_name": "",
#         "did": "12396",
#         "dtmf": "",
#         "ivr_object_id": "318",
#         "ivr_schema_id": "34056",
#         "linked_id": "116-1741694432.6016962",
#         "robocall_id": "0",
#         "robocall_target_number": "",
#         "robocall_task_contact_id": "0",
#         "robocall_task_id": "0",
#         "stt_answer": "",
#         "n8n_success": "true",
#     }


# def test_queue_event_from_dict(mock_data):
#     data = {
#         "event_additional_info": {
#             "name": "QueueName",
#             "number": "12345",
#         },
#         "event_answer_time": "2025-04-15 12:00:00",
#     }
#     event = QueueEvent.from_dict(data)
#     assert isinstance(event, QueueEvent)
#     assert event.name == "QueueName"
#     assert event.number == "12345"
#     assert event.event_answer_time == datetime(2025, 4, 15, 12, 0, 0)


# def test_blacklist_event_from_dict(mock_data):
#     data = {"event_additional_info": {"exten": "1234"}}
#     event = BlackListEvent.from_dict(data)
#     assert isinstance(event, BlackListEvent)
#     assert event.exten == "1234"


# def test_speech_recog_event_from_dict(mock_data):
#     data = {"speechkit_dialog": [{"dialog_value": "What is the weather like?"}, {"dialog_value": "It's sunny."}]}
#     event = SpeechRecogEvent.from_dict(data)
#     assert isinstance(event, SpeechRecogEvent)
#     assert event.question == "What is the weather like?"
#     assert event.answer == "It's sunny."


# @pytest.mark.parametrize(
#     "event_class, data, expected_api_vars",
#     [
#         (
#             GptEvent,
#             {
#                 "event_additional_info": {
#                     "api_vars": """{account_id:133429,num_a:12396,num_b:88002344499,call_id:116-1741694432.6016962,
#                     num_c:null,short_num_found:false,vpbx_id:16884,scenario_id:34056,scenario_counter:1,
#                     scenario_client_variables_1:{short_num_found:false,vpbx_id:16884},
#                     scenario_id_1:34056,dest_link_name:,did:12396,dtmf:,
#                     ivr_object_id:318,ivr_schema_id:34056,linked_id:116-1741694432.6016962,
#                     robocall_id:0,robocall_target_number:,
#                     robocall_task_contact_id:0,robocall_task_id:0,stt_answer:,n8n_success:true}"""
#                 }
#             },
#             {
#                 "account_id": "133429",
#                 "num_a": "12396",
#                 "num_b": "88002344499",
#                 "call_id": "116-1741694432.6016962",
#                 "num_c": "null",
#                 "short_num_found": "false",
#                 "vpbx_id": "16884",
#                 "scenario_id": "34056",
#                 "scenario_counter": "1",
#                 "scenario_client_variables_1": "short_num_found:false",
#                 "scenario_id_1": "34056",
#                 "dest_link_name": "",
#                 "did": "12396",
#                 "dtmf": "",
#                 "ivr_object_id": "318",
#                 "ivr_schema_id": "34056",
#                 "linked_id": "116-1741694432.6016962",
#                 "robocall_id": "0",
#                 "robocall_target_number": "",
#                 "robocall_task_contact_id": "0",
#                 "robocall_task_id": "0",
#                 "stt_answer": "",
#                 "n8n_success": "true",
#             },
#         ),
#         (
#             HTTPEvent,
#             {
#                 "event_additional_info": {
#                     "api_vars": """{account_id:133429,num_a:12396,num_b:88002344499,call_id:116-1741694432.6016962,
#                     num_c:null,short_num_found:false,vpbx_id:16884,scenario_id:34056,scenario_counter:1,
#                     scenario_client_variables_1:{short_num_found:false,vpbx_id:16884},
#                     scenario_id_1:34056,dest_link_name:,did:12396,
#                     dtmf:,ivr_object_id:318,ivr_schema_id:34056,
#                     linked_id:116-1741694432.6016962,robocall_id:0,robocall_target_number:,
#                     robocall_task_contact_id:0,robocall_task_id:0,stt_answer:,n8n_success:true}"""
#                 }
#             },
#             {
#                 "account_id": "133429",
#                 "num_a": "12396",
#                 "num_b": "88002344499",
#                 "call_id": "116-1741694432.6016962",
#                 "num_c": "null",
#                 "short_num_found": "false",
#                 "vpbx_id": "16884",
#                 "scenario_id": "34056",
#                 "scenario_counter": "1",
#                 "scenario_client_variables_1": "short_num_found:false",
#                 "scenario_id_1": "34056",
#                 "dest_link_name": "",
#                 "did": "12396",
#                 "dtmf": "",
#                 "ivr_object_id": "318",
#                 "ivr_schema_id": "34056",
#                 "linked_id": "116-1741694432.6016962",
#                 "robocall_id": "0",
#                 "robocall_target_number": "",
#                 "robocall_task_contact_id": "0",
#                 "robocall_task_id": "0",
#                 "stt_answer": "",
#                 "n8n_success": "true",
#             },
#         ),
#     ],
# )
# def test_event_with_api_vars(event_class, data, expected_api_vars):
#     event = event_class.from_dict(data)
#     assert isinstance(event, event_class)
#     assert event.api_vars == expected_api_vars


# # Пример теста для обработки некорректных данных
# def test_unknown_event_from_dict_invalid_data():
#     data = {"invalid_field": "some_value"}
#     event = UnknownEvent.from_dict(data)
#     assert isinstance(event, UnknownEvent)
#     assert event.data == {"invalid_field": "some_value"}
