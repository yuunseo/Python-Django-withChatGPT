from channels.generic.websocket import JsonWebsocketConsumer
from pprint import pprint
from typing import List
from django.contrib.auth.models import AbstractUser
from chat.models import RolePlayingRoom, GptMessage
import openai


# 상속받은 클래스에 기본 기능 구현되어 있음
class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gpt_messages: List[GptMessage] = []
        self.recommend_message: str = ""

    # 웹소켓 접속 유저가 원하는 채팅방과 연결(connect)
    def connect(self):
        room = self.get_room()
        if room is None:
            self.close()
        else:
            self.accept()

            # user의 초기 설정
            self.gpt_messages = room.get_initial_messages()
            # gpt의 추천 표현
            self.recommend_message = room.get_recommend_message()
            # gpt의 초기 설정
            assistant_message = self.gpt_query()
            # client로 전송
            self.send_json(
                {
                    "type": "assistant-message",
                    "message": assistant_message,
                }
            )

    # client->server: receive_json
    # server->client: send_json
    def receive_json(self, content_dict, **kwargs):
        # user의 메세지를 받아서
        if content_dict["type"] == "user-message":
            assistant_message = self.get_query(user_query=content_dict["message"])
            # 직렬화
            self.send_json(
                {
                    "type": "assistant-message",
                    "message": assistant_message,
                }
            )
        elif content_dict["type"] == "request-recommend-message":
            recommended_message = self.get_query(command_query=self.recommend_message)
            self.send_json(
                {
                    "type": "recommended-message",
                    "message": recommended_message,
                }
            )
        else:
            self.send_json(
                {
                    "type": "error",
                    "message": f"Invalid type: {content_dict['type']}",
                }
            )

    # user의 채팅방 조회
    def get_room(self) -> RolePlayingRoom | None:
        user: AbstractUser = self.scope["user"]
        room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
        room: RolePlayingRoom = None

        if user.is_authenticated:
            try:
                room = RolePlayingRoom.objects.get(pk=room_pk, user=user)
            except RolePlayingRoom.DoesNotExist:
                pass

        return room

    # openai api함수를 호출하는 메소드
    def gpt_query(self, command_query: str = None, user_query: str = None) -> str:
        if command_query is not None and user_query is not None:
            raise ValueError("command_query 인자와 user_query 인자는 동시에 사용할 수 없습니다.")
        elif command_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=command_query))
        elif user_query is not None:
            self.gpt_messages.append(GptMessage(role="user", content=user_query))

        response_dict = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.gpt_messages,
            temperature=1,
        )
        response_role = response_dict["choices"][0]["message"]["role"]
        response_content = response_dict["choices"][0]["message"]["content"]

        # command_query 수행 시에는 대화 내역 저장 안하고, 그 외에만 저장.
        if command_query is None:
            gpt_message = GptMessage(role=response_role, content=response_content)
            self.gpt_messages.append(gpt_message)

        return response_content
