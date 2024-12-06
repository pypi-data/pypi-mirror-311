from .types import (TScanDict, TLoginDict, TLogoutDict, TMessageDict,
                    TContactMessageItem, TGroupMessageDict, TFriendshipItemDict, TGroupInvitationItemDict,
                    TGroupNameChangeItemDict, TGroupMemberJoinItemDict, TGroupMemberLeaveItemDict, TServerErrorDict)
import datetime
from .base import (Contact, Group, MessageType, ScanStatus, ReceiverType, File, FriendshipType, UrlLink)
from .logging_config import logging
from typing import TYPE_CHECKING, List, NoReturn
if TYPE_CHECKING:
    from .bot import WechatBot
logger = logging.getLogger('default')


class EventMeta:
    def __init__(self, service_flag: str,
                 name: str,
                 timestamp: int):

        self.service_flag = service_flag
        self.name = name
        self.timestamp = timestamp


class ServerError:
    def __init__(self, items: TServerErrorDict):
        self.name = items['name']
        self.message = items['message']
        if items.get('stack'):
            self.stack = items['stack']

    def __str__(self):
        return f"ServerError [{self.name}][{self.message}]"


class Scan:
    def __init__(self, items: TScanDict):
        self.qrcode = items['qrcode']
        self.status = ScanStatus(items['status'])

    def __str__(self):
        return f"Scan [{self.status.name}]: {self.qrcode}"


class Login:
    def __init__(self, items: TLoginDict):
        self.contact = Contact(items['contact'])


class Logout:
    def __init__(self, items: TLogoutDict):
        self.contact = Contact(items['contact'])


class Message:
    def __init__(self, items: TMessageDict):
        self.sender = Contact(items['talker'])
        self.text = items['text']
        self.type = MessageType(items['type'])
        self.date = datetime.datetime.fromisoformat(items['date'].replace("Z", "+00:00"))
        self.age = items['age']
        self.is_owner = items['self']
        if items.get('fileBox'):
            self.file = File(items['fileBox'])
        if items.get('urlLink'):
            self.url_link = UrlLink(items['urlLink'])


class ContactGroupMessage(Message):
    def __init__(self, wechat_bot: 'WechatBot', items: TMessageDict):
        super().__init__(items)
        self._wechat_bot = wechat_bot

    async def _forward(self, receiver_type: ReceiverType, receiver_id_list: List[str], interval: int = 1000):

        if self.type == MessageType.Text:
            if receiver_type == ReceiverType.Group:
                await self._wechat_bot.send_group_text_message(self.text,
                                                          receiver_id_list,
                                                          interval)

            elif receiver_type == ReceiverType.Contact:
                await self._wechat_bot.send_contact_text_message(self.text,
                                                          receiver_id_list,
                                                          interval)

        elif self.type in [MessageType.Image,
                           MessageType.Audio,
                           MessageType.Video,
                           MessageType.Attachment]:
            if self.file:
                await self._wechat_bot.forward_file(receiver_type,
                                                    receiver_id_list,
                                                    self.file.id,
                                                    interval)
            else:
                logger.error('This message does not contain a file.')

        # wechaty 暂不支持发送Url类型的消息
        # elif self.type == MessageType.Url:
        #     await self._wechat_bot.send_url_link(receiver_type,
        #                                          receiver_id_list,
        #                                          self.url_link,
        #                                          interval)
        else:
            logger.error(f'消息类型[{self.type.name}]不支持转发。')

    async def forward_to_contacts(self, contact_id_list: List[str], interval: int = 1000) -> NoReturn:
        await self._forward(ReceiverType.Contact, contact_id_list, interval)

    async def forward_to_groups(self, groups_id_list: List[str], interval: int = 1000) -> NoReturn:
        await self._forward(ReceiverType.Group, groups_id_list, interval)

    async def forward_to_group_with_at(
            self,
            group_id: str,
            member_id_list: List[str],
    ) -> NoReturn:
        if self.type == MessageType.Text:
            await self._wechat_bot.send_group_message_with_at(group_id,
                                                              self.text,
                                                              member_id_list
                                                              )
        else:
            logger.error(f"消息类型[{self.type.name}]不支持转发到群并@成员。")


class ContactMessage(ContactGroupMessage):
    def __init__(self, wechat_bot: 'WechatBot', items: TContactMessageItem):
        super().__init__(wechat_bot, items)
        self.receiver = Contact(items['listener'])

    def __str__(self):
        return f"{'🙋‍♂️' if self.is_owner else ''}ContactMessage [{self.type.name}][{self.sender.name}]: {self.file.name if hasattr(self, 'file') else self.text}"

    async def reply_text(self, text: str) -> NoReturn:
        await self._wechat_bot.send_contact_text_message(text,
                                                    [self.sender.id],
                                                    )



class GroupMessage(ContactGroupMessage):
    def __init__(self, wechat_bot: 'WechatBot', items: TGroupMessageDict):
        super().__init__(wechat_bot, items)
        self.group = Group(items['room'])
        self.mention_list = [Contact(mention_items) for mention_items in items['mentionList']]
        self.mention_self = items['mentionSelf']

    def __str__(self):
        if self.mention_list:
            new_mention_list = [f"@{mention.name}" for mention in self.mention_list]
            mention_str = ", ".join(new_mention_list)
            mention_str = f"[{mention_str}]"
        else:
            mention_str =  ''
        return f"{'🙋‍♂️' if self.is_owner else ''}GroupMessage [{self.type.name}][{self.group.name}][{self.sender.name}]{mention_str}: {self.file.name if hasattr(self, 'file') else self.text}"


    async def remove_sender(self):
        await self._wechat_bot.group_remove_member(self.group.id, [self.sender.id])


    async def reply_text(self, text: str) -> NoReturn:
        await self._wechat_bot.send_group_text_message(text,
                                                    [self.group.id]
                                                  )

    async def reply_text_with_at(self, text: str) -> NoReturn:
        await self._wechat_bot.send_group_message_with_at(self.group.id,
                                                          text,
                                                          [self.sender.id],
                                                          )


class Friendship:
    def __init__(self, wechat_bot: 'WechatBot', items: TFriendshipItemDict):
        self._wechat_bot = wechat_bot
        self.id = items['id']
        self.hello = items['hello']
        self.contact = Contact(items['contact'])
        self.type = FriendshipType(items['type'])

    def __str__(self):
        return f"Friendship [{self.type.name}][{self.contact.name}]: {self.hello}"

    async def accept(self):
        if self.type == FriendshipType.Receive:
            await self._wechat_bot.accept_friend_verify(self.id)


class GroupInvitation:
    def __init__(self, wechat_bot: 'WechatBot', items: TGroupInvitationItemDict):
        self._wechat_bot = wechat_bot
        self.id = items['id']
        self.group_name = items['topic']
        self.inviter = Contact(items['inviter'])
        self.date = datetime.datetime.fromisoformat(items['date'].replace("Z", "+00:00"))
        self.age = items['age']

    async def accept(self):
        await self._wechat_bot.accept_group_invitation(self.id)

class GroupNameChange:
    def __init__(self, items: TGroupNameChangeItemDict):
        self.group = Group(items['room'])
        self.new_name = items['newTopic']
        self.old_name = items['oldTopic']
        self.changer = Contact(items['changer'])


class GroupMemberJoin:
    def __init__(self, items: TGroupMemberJoinItemDict):
        self.group = Group(items['room'])
        self.invitee_list = [Contact(contact_dict) for contact_dict in items['inviteeList']]
        self.inviter = Contact(items['inviter'])


class GroupMemberLeave:
    def __init__(self, items: TGroupMemberLeaveItemDict):
        self.group = Group(items['room'])
        self.leaver_list = [Contact(contact_dict) for contact_dict in items['leaverList']]
        self.remover = Contact(items['remover'])


# class FriendVerify(Message):
#     def __init__(self, instance: 'WechatBot', event: T_event):
#         """
#         EventFriendVerify,  好友请求事件
#         :param instance:  Bot类的实例对象
#         :param event: 事件dict
#         """
#         super().__init__(event)
#         self._wechat_bot = instance
#         self.to_id: str = event['items']['to_id']
#         self.json_msg: T_json_msg = event['items']['json_msg']
#
#         self.to_name: str = event['items']['json_msg']['to_name']
#         # self.sender.id: str = event['items']['json_msg']['from_id']
#         self.from_nickname: str = event['items']['json_msg']['from_nickname']
#         self.sex: int = event['items']['json_msg']['sex']
#         self.from_content: str = event['items']['json_msg']['from_content']
#         self.headimgurl: str = event['items']['json_msg']['headimgurl']
#         self.mode: int = event['items']['json_msg']['type']
#         if 'from_group_id' in event['items']['json_msg']:
#             self.from_group_id = event['items']['json_msg']['from_group_id']
#
#         """
#         to_id, 消息接收者微信ID
#         json_msg,  好友验证信息字典（1 / 群内添加时，包含群id
#         to_name，消息接收者微信昵称
#         from_id， 对方微信ID
#         from_nickname， 对方微信昵称
#         sex， 对方性别代号
#         from_content， 验证内容
#         headimgurl， 对方头像url
#         mode， 添加方式，15：搜索添加，14：通过群聊添加
#         from_group_id： 群聊添加的 群聊ID
#
#         """
#
#     async def agree(self) -> NoReturn:
#         """
#         同意好友请求
#         :return:
#         """
#         if self.sender.id != self.robot_id:
#             await self._wechat_bot.agree_friend_verify(self.json_msg)
#
#
# class GroupInvite(Message):
#     def __init__(self, instance: 'WechatBot', event: T_event):
#         """
#         EventGroupInvite, 邀请入群事件
#         :param instance:  Bot类的实例对象
#         :param event: 事件dict
#         """
#         super().__init__(event)
#         self._wechat_bot: 'WechatBot' = instance
#         self.event_name: str = 'EventGroupInvite'
#         self.to_id: str = event['items']['to_id']
#         self.json_msg: T_json_msg = event['items']['msg']
#
#         self.inviter_id: str = event['items']['msg']['inviter_id']
#         self.inviter_nickname: str = event['items']['msg']['inviter_nickname']
#         self.group_headimgurl: str = event['items']['msg']['group_headimgurl']
#         self.group_name: str = event['items']['msg']['group_name']
#         """
#         event_name 事件名称
#         msg_type, 消息类型
#         to_id, 消息接收者
#         json_msg, 消息原json，仅用来同意邀请回传使用
#         inviter_id: 邀请者微信ID
#         inviter_nickname：邀请者昵称
#         group_headimgurl：群头像url
#         group_name：群名
#         """
#
#     async def agree(self) -> NoReturn:
#         """
#         同意入群请求
#         :return:
#         """
#         # 判断是否是自己微信号邀请别人
#         if self.inviter_id != self.robot_id:
#             await self._wechat_bot.agree_group_invite(self.json_msg)
#
#
# class Group_member_add(Message):
#     def __init__(self, instance: 'WechatBot', event: T_event):
#         """
#         EventGroupMemberAdd,  群成员增加事件
#         :param instance: Bot类的实例对象
#         :param event: 事件dict
#         """
#         super(Group_member_add, self).__init__(event)
#         self._wechat_bot: 'WechatBot' = instance
#         self.guest: List[Dict[str, Any]] = event['items']['json_msg']['guest']
#         self.inviter_id: str = event['items']['json_msg']['inviter']['id']
#         self.inviter_nickname: str = event['items']['json_msg']['inviter']['nickname']
#         """
#
#             guest 进群人列表
#             inviter_id 邀请人微信ID
#             inviter_nickname 邀请人微信昵称
#         """
#
#     async def reply(self, content: str):
#         await self._wechat_bot.send_text_msg(self.sender.id, content)
#
#
# class Group_member_decrease(Message):
#     def __init__(self, instance: 'WechatBot', event: T_event):
#         """
#         EventGroupMemberDecrease,  群成员减少事件
#         :param instance: Bot类的实例对象
#         :param event: 事件dict
#         """
#         super(Group_member_decrease, self).__init__(event)
#         self._wechat_bot: 'WechatBot' = instance
#         self.member_id: str = event['items']['json_msg']['member_id']
#         self.member_nickname: str = event['items']['json_msg']['member_nickname']
#         """
#         "member_id" 减少的成员微信ID
#         "member_nickname" 减少的成员微信昵称
#         """
#     async def reply(self, content: str):
#         await self._wechat_bot.send_text_msg(self.sender.id, content)
#
#
# class Received_transfer(Message):
#     def __init__(self, instance: 'WechatBot', event: T_event):
#         """
#         EventReceivedTransfer,  收到转账事件
#         :param instance:  Bot类的实例对象
#         :param event: 事件dict
#         """
#         super(Received_transfer, self).__init__(event)
#         self._wechat_bot: 'WechatBot' = instance
#         self.json_msg: T_json_msg = event['items']['json_msg']
#
#         self.paysubtype: str = event['items']['json_msg']['paysubtype']
#         self.is_arrived: int = event['items']['json_msg']['is_arrived']
#         self.is_received: int = event['items']['json_msg']['is_received']
#         self.receiver_pay_id: str = event['items']['json_msg']['receiver_pay_id']
#         self.payer_pay_id: str = event['items']['json_msg']['payer_pay_id']
#         self.money: str = event['items']['json_msg']['money']
#         self.remark: str = event['items']['json_msg']['remark']
#         """
#         "paysubtype" 支付子类型
#         "is_arrived" 是否即时到账,  这个变量用来判断这一笔转账是否是正常的，因为有可能是延迟转账类型
#         "is_received" 是否已经收款, 这个变量用来判断是否收款成功，因为本事件有（收到转账消息、同意收款后的消息、转账过期的消息）这几种类型，这里代表已经收到了
#         "receiver_pay_id" 接收方订单号
#         "payer_pay_id" 发送方订单号
#         "money", 金额
#         "remark" 转账备注
#         """
#     async def accept(self):
#         await self._wechat_bot.accept_transfer(self.sender.id, self.json_msg)
#
#
# class Scan_cashMoney:
#     def __init__(self, event: T_event):
#         """
#         EventScanCashMoney,  二维码收款事件
#         :param event: 事件dict
#         """
#         self.event_name: str = event['event_name']
#         self.timestamp: int = event['timestamp']
#
#         self.robot_id: str = event['items']['robot_id']
#
#         self.payer_id: str = ''
#         self.payer_nickname: str = ''
#         self.money: str = ''
#         if 'payer_id' in event['items']['json_msg']:
#             self.payer_id = event['items']['json_msg']['payer_id']
#         if 'payer_nickname' in event['items']['json_msg']:
#             self.payer_nickname = event['items']['json_msg']['payer_nickname']
#         if 'money' in event['items']['json_msg']:
#             self.money = event['items']['json_msg']['money']
#         self.msgid: str = event['items']['json_msg']['msgid']
#         self.to_id: str = event['items']['json_msg']['to_id']
#         self.scene_desc: str = event['items']['json_msg']['scene_desc']
#         self.scene: str = event['items']['json_msg']['scene']
#         self.pay_timestamp: int = event['items']['json_msg']['timestamp']
#         """
#         robot_id, , 收到事件的机器人微信ID
#         payer_id, , 扫码付款者的微信ID
#         payer_nickname, , 扫码付款者的微信昵称
#         money, , 金额
#
#         msgid 消息ID
#         to_id 收款人的微信ID
#         scene_desc 场景详情
#         scene 场景代号
#         pay_timestamp 场景发生时间戳
#
#         """
#
#
# class Plug:
#     def __init__(self, event: T_event):
#         """
#         EventPlug 插件被启用/停用/插件重载/插件卸载/软件退出事件
#         :param event: 事件dict
#         """
#         self.event_name: str = 'EventPlug'
#         self.timestamp: int = event['timestamp']
#         if event['event_name'] == 'EventStop':
#             self.type: int = event['items']['type']
#         elif event['event_name'] == 'EventEnable':
#             self.type: int = 4
#     """
#     type, 0 插件被停用 / 1 插件重载  / 2 插件卸载 / 3 可爱猫退出 /4 插件激活
#
#     """
#
#
# class Sys_message:
#     def __init__(self, event: T_event):
#         self.event_name: str = event['event_name']
#         self.timestamp: int = event['timestamp']
#         self.robot_id: str = event['items']['robot_id']
#         self.type: int = event['items']['type']
#         self.json_msg: T_json_msg = event['items']['json_msg']
#     """
#     robot_id, 机器人账号id（就是这条消息是哪个机器人的，因为可能登录多个机器人）
#     type, 消息类型
#     json_msg, 消息内容
#     """