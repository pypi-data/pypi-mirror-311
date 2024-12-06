"""本模块定义了bot模块中共享的一些类型。

下面的文档中，「类型」部分使用 Python 的 Type Hint 语法，
参考 [`PEP 484`](https://www.python.org/dev/peps/pep-0484/),
[`PEP 526`](https://www.python.org/dev/peps/pep-0526/) 和
[`typing`](https://docs.python.org/3/library/typing.html)。

"""
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    TypeVar,
    Callable,
    Optional,
    Awaitable,
    TypedDict, Union
)
if TYPE_CHECKING:
    from .base import FriendType, FriendshipType


T_event_processor = TypeVar("T_event_processor", bound=Awaitable[Callable])
"""
事件处理函数类型
"""
class TServerErrorDict(TypedDict):
    name: str
    message: str
    stack: Optional[str]

class TContactDict(TypedDict):
    id: str
    name: str
    alias: str
    friend: 'FriendType'
    type: int
    gender: int
    province: str
    city: str
    self: bool


class TGroupDict(TypedDict):
    id: str
    topic: str
    owner: Optional[TContactDict]

class TEventDict(TypedDict):
    serviceFlag: str
    eventName: str
    timestamp: int


class TScanDict(TypedDict):
    qrcode: str
    status: str


class TLoginDict(TypedDict):
    contact: TContactDict


class TLogoutDict(TypedDict):
    contact: TContactDict


class TFileBoxDict(TypedDict):
    id: str
    type: int
    name: str
    size: str
    md5: Optional[str]
    mediaType: str
    metadata: dict[str, Any]


class TUrlLinkDict(TypedDict):
    description: str
    thumbnailUrl: str
    title: str
    url:str


class TMessageDict(TypedDict):
    talker: TContactDict
    text: str
    type: int
    date: str
    age: int
    self: bool
    fileBox: Optional[TFileBoxDict]
    urlLink: Optional[TUrlLinkDict]


class TContactMessageItem(TMessageDict):
    listener: TContactDict


class TGroupMessageDict(TMessageDict):
    room: TGroupDict
    mentionList: List[TContactDict]
    mentionSelf: bool


class TFriendshipItemDict(TypedDict):
    id: str
    hello: str
    contact: TContactDict
    type: 'FriendshipType'


class TGroupInvitationItemDict(TypedDict):
    id: str
    inviter: TContactDict
    topic: str
    date: str
    age: int


class TGroupNameChangeItemDict(TypedDict):
    room: TGroupDict
    newTopic: str
    oldTopic: str
    changer: TContactDict


class TGroupMemberJoinItemDict(TypedDict):
    room: TGroupDict
    inviteeList: List[TContactDict]
    inviter: TContactDict


class TGroupMemberLeaveItemDict(TypedDict):
    room: TGroupDict
    leaverList: List[TContactDict]
    remover: TContactDict


class TTaskResultDict(TypedDict):
    code: int
    message: str
    data: Optional[Union[Dict, List]]