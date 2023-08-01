from channels.generic.websocket import JsonWebsocketConsumer


# 상속받은 클래스에 기본 기능 구현되어 있음
class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 대화내역 저장을 위한 count 변수 생성
        self.count = 0

    # client->server: receive_json
    # server->client: send_json
    def receive_json(self, content, **kwargs):
        self.count += 1
        # 대화 하나씩 추가 시, 내용과 함께 추가
        content["count"] = self.count
        # Echo
        self.send_json(content)
