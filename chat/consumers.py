from channels.generic.websocket import JsonWebsocketConsumer


# 상속받은 클래스에 기본 기능 구현되어 있음
class RolePlayingRoomConsumer(JsonWebsocketConsumer):
    # client->server: receive_json
    # server->client: send_json
    def receive_json(self, content, **kwargs):
        print("received:", content)
        # Echo
        self.send_json(content)
