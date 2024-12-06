from enum import IntEnum
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .types import TContactDict, TGroupDict, TFileBoxDict, TUrlLinkDict, TTaskResultDict


class FileBoxType(IntEnum):
    Unknown = 0
    Base64  = 1
    Url     = 2
    QRCode  = 3
    Buffer  = 4
    File    = 5
    Stream  = 6
    Uuid    = 7


class ReceiverType(IntEnum):
    Contact = 0
    Group = 1

class FriendshipType(IntEnum):
    Unknown = 0
    Confirm = 1
    Receive = 2
    Verify = 3


class Gender(IntEnum):
    Unknown = 0
    Male    = 1
    Female  = 2


class UserType(IntEnum):
    Unknown = 0
    Individual = 1
    Official = 2
    Corporation = 3


class MessageType(IntEnum):
    # 未知
    Unknown = 0
    # 文件
    Attachment = 1
    # 语音
    Audio = 2
    # 联系人分享
    Contact = 3
    # 表情图片
    Emoticon = 5
    # 图片
    Image = 6
    # 文本
    Text = 7
    # 小程序分享
    MiniProgram = 9
    # 撤回
    Recalled = 13
    # url分享
    Url = 14
    # 视频
    Video = 15


class FriendType(IntEnum):
    Unknown = 0
    Yes = 1
    No = 2


class ScanStatus(IntEnum):
    Unknown   = 0
    Cancel    = 1
    Waiting   = 2
    Scanned   = 3
    Confirmed = 4
    Timeout   = 5


class UrlLink:
    def __init__(self, items: 'TUrlLinkDict'):
        self.description = items['description']
        self.thumbnail_url = items['thumbnailUrl']
        self.title = items['title']
        self.url = items['url']

    def __str__(self):
        return (f"description: {self.description}\n"
                f"thumbnail_url: {self.thumbnail_url}\n"
                f"title: {self.title}\n"
                f"url: {self.url}")

    def to_dict(self):
        return {
            'description': self.description,
            'thumbnail_url': self.thumbnail_url,
            'title': self.title,
            'url': self.url
        }

class File:
    def __init__(self, items: 'TFileBoxDict'):
        self.id = items['id']
        self.type = FileBoxType(items["type"])
        self.name = items["name"]
        self.size = items["size"]
        self.md5 = items.get('md5', '')
        self.media_type = items["mediaType"]
        self.metadata = items['metadata']

    def __str__(self):
        return (f"id: {self.id}\n"
                f"type: {self.type}\n"
                f"name: {self.name}\n"
                f"size: {self.size}\n"
                f"md5: {self.md5}\n"
                f"media_type: {self.media_type}\n"
                f"metadata: {self.metadata}")

class Contact:
    def __init__(self, items: 'TContactDict'):
        if 'friend' not in items:
            self.friend = FriendType.Unknown
        else:
            if items['friend']:
                self.friend = FriendType.Yes
            else:
                self.friend = FriendType.No
        self.id: str = items['id']
        self.name: str = items['name']
        self.alias: str = items['alias']
        self.type: UserType = UserType(items['type'])
        self.gender: Gender = Gender(items['gender'])
        self.province: str = items['province']
        self.city: str = items['city']
        self.self: bool = items['self']

    def __str__(self):
        if self.alias:
            alias_str = f"({self.alias})"
        else:
            alias_str = ""

        return f"{'🙋‍♂️' if self.self else ''}Contact [{self.type.name}][{self.id}][{self.name}{alias_str}]"

class Group:
    def __init__(self, items: 'TGroupDict'):
        self.id: str = items['id']
        self.name: str = items['topic']
        if items.get('owner'):
            self.owner = Contact(items['owner'])

    def __str__(self):
        me = ''
        if hasattr(self, 'owner'):
            me = '🙋‍♂️' if self.owner.self else ''
        return f"{me}Group [{self.id}][{self.name}]"


class TaskResult:
    def __init__(self, items: 'TTaskResultDict'):
        self.code = items['code']
        self.message = items['message']
        if items.get('data'):
            self.data = items['data']