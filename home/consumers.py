import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    players = {}

    async def connect(self):
        self.room_group_name = "game"
        self.username = None

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.username and self.username in GameConsumer.players:
            del GameConsumer.players[self.username]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "players_list_update",
                    "players": GameConsumer.players
                }
            )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get("type")

        if msg_type == "set_username":
            username = data["username"]
            self.username = username

            GameConsumer.players[username] = {
                "id": username,
                "position": {"x": 250, "y": 150},
                "esquerda": False,
                "direita": False,
                "cima": False,
                "baixo": False
            }

            await self.send(text_data=json.dumps({
                "type": "username_set",
                "user_id": username
            }))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "players_list_update",
                    "players": GameConsumer.players
                }
            )

        elif msg_type == "update_movement":
            if not self.username or self.username not in GameConsumer.players:
                return  # ignora se jogador não está registrado

            player = GameConsumer.players[self.username]

            movimento = data.get("movimento", {})
            player["esquerda"] = movimento.get("esquerda", False)
            player["direita"] = movimento.get("direita", False)
            player["cima"] = movimento.get("cima", False)
            player["baixo"] = movimento.get("baixo", False)

            if "position" in data:
                player["position"]["x"] = data["position"].get("x", player["position"]["x"])
                player["position"]["y"] = data["position"].get("y", player["position"]["y"])

            # Envia só o jogador que atualizou (mais eficiente)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "players_list_update",
                    "players": {self.username: player}
                }
            )

    async def players_list_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "players_list_update",
            "players": event["players"]
        }))