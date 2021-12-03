from starlette.websockets import WebSocket
from starlette.responses import FileResponse
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.endpoints import WebSocketEndpoint
from pydantic import BaseModel
from fastapi import Body, HTTPException
from typing import Any, List, Optional
from enum import Enum
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from services.chat import Distance, Room, ThunderDistance, UserInfo, UserListResponse

from utils.chat import ConnectionManager


manager = ConnectionManager()

chat_router = APIRouter(prefix='/chat')


@chat_router.get("/")
def home():
    """Serve static index page.
    """
    return FileResponse("static/index.html")




@chat_router.get("/users", response_model=UserListResponse)
async def list_users(request: Request):
    """List all users connected to the room.
    """
    room: Optional[Room] = request.get("room")
    if room is None:
        raise HTTPException(500, detail="Global `Room` instance unavailable!")
    return {"users": room.user_list}


class UserInfoResponse(UserInfo):
    """Response model for /users/:user_id endpoint.
    """


@chat_router.get("/users/{user_id}", response_model=UserInfoResponse)
async def get_user_info(request: Request, user_id: str):
    room: Optional[Room] = request.get("room")
    if room is None:
        raise HTTPException(500, detail="Global `Room` instance unavailable!")
    user = room.get_user(user_id)
    if user is None:
        raise HTTPException(404, detail=f"No such user: {user_id}")
    return user


@chat_router.post("/users/{user_id}/kick", response_model=UserListResponse)
async def kick_user(request: Request, user_id: str):
    """List all users connected to the room.
    """
    room: Optional[Room] = request.get("room")
    if room is None:
        raise HTTPException(500, detail="Global `Room` instance unavailable!")
    try:
        await room.kick_user(user_id)
    except ValueError:
        raise HTTPException(404, detail=f"No such user: {user_id}")




@chat_router.post("/thunder")
async def thunder(request: Request, distance: ThunderDistance = Body(...)):
    """Broadcast an ambient message to all chat room users.
    """
    room: Optional[Room] = request.get("room")
    if room is None:
        raise HTTPException(500, detail="Global `Room` instance unavailable!")
    if distance.category == Distance.Near:
        await room.broadcast_message("server", "Thunder booms overhead")
    elif distance.category == Distance.Far:
        await room.broadcast_message("server", "Thunder rumbles in the distance")
    else:
        await room.broadcast_message("server", "You feel a faint tremor")


@chat_router.websocket_route("/ws", name="ws")
class RoomLive(WebSocketEndpoint):
    """Live connection to the global :class:`~.Room` instance, via WebSocket.
    """

    encoding: str = "text"
    session_name: str = ""
    count: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room: Optional[Room] = None
        self.user_id: Optional[str] = None

    @classmethod
    def get_next_user_id(cls):
        """Returns monotonically increasing numbered usernames in the form
            'user_[number]'
        """
        user_id: str = f"user_{cls.count}"
        cls.count += 1
        return user_id

    async def on_connect(self, websocket):
        """Handle a new connection.
        New users are assigned a user ID and notified of the room's connected
        users. The other connected users are notified of the new user's arrival,
        and finally the new user is added to the global :class:`~.Room` instance.
        """
        print("Connecting new user...")
        room: Optional[Room] = self.scope.get("room")
        if room is None:
            raise RuntimeError(f"Global `Room` instance unavailable!")
        self.room = room
        self.user_id = self.get_next_user_id()
        await websocket.accept()
        await websocket.send_json(
            {"type": "ROOM_JOIN", "data": {"user_id": self.user_id}}
        )
        await self.room.broadcast_user_joined(self.user_id)
        self.room.add_user(self.user_id, websocket)

    async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
        """Disconnect the user, removing them from the :class:`~.Room`, and
        notifying the other users of their departure.
        """
        if self.user_id is None:
            raise RuntimeError(
                "RoomLive.on_disconnect() called without a valid user_id"
            )
        self.room.remove_user(self.user_id)
        await self.room.broadcast_user_left(self.user_id)

    async def on_receive(self, _websocket: WebSocket, msg: Any):
        """Handle incoming message: `msg` is forwarded straight to `broadcast_message`.
        """
        if self.user_id is None:
            raise RuntimeError("RoomLive.on_receive() called without a valid user_id")
        if not isinstance(msg, str):
            raise ValueError(f"RoomLive.on_receive() passed unhandleable data: {msg}")
        await self.room.broadcast_message(self.user_id, msg)
