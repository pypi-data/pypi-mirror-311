import json
from multiprocessing.reduction import sendfds
from uuid import uuid4
from redis import asyncio as aioredis
import time
from .error import TaskReturnTimeout, TaskProcessingException, MessageTypeError
from pprint import pprint
from .types import T_event_processor
from typing import NoReturn, Dict, Callable, Any, List, Union, Type
import asyncio
from .base import ReceiverType, Contact, Group, TaskResult, MessageType
from .event import (Scan, Login, Logout, GroupMessage, ContactMessage, Friendship, GroupInvitation, GroupNameChange,
                    GroupMemberJoin, GroupMemberLeave, ServerError)
from .logging_config import logging
logger = logging.getLogger('default')


def underline_to_hump(text: str) -> str:
    arr = text.lower().split('_')
    res = []
    for i in arr:
        res.append(i[0].upper() + i[1:])
    return ''.join(res)


class Base_bot:
    def __init__(self, host: str, port: int, service_flag: str, password=None):
        self._redis = aioredis.Redis(host=host,
                                     port=port,
                                     password=password,
                                     encoding="utf-8",
                                     decode_responses=True )
        self._service_flag: str = service_flag
        self._matcher: Dict[str, Callable[..., Any]] = {}
        self._task_return_timeout = 60

    @property
    def service_flag(self):
        return self._service_flag

    def register(self, processor: str) -> Callable[[T_event_processor], NoReturn]:
        def wrapper(func: T_event_processor) -> NoReturn:
            self._matcher[processor] = func
        return wrapper

    async def _send_task(self, task_name: str, items: Dict[str, Any] = None, return_key:str = None) -> NoReturn:

        task_json = dict()
        task_json['service_flag'] = self._service_flag
        task_json['task_name'] = task_name
        task_json['timestamp'] = int(time.time() * 1000)
        task_json[task_name] = items

        if return_key:
            task_json['return_key'] = return_key
        try:
            await self._redis.lpush(f"{self.service_flag}_task", json.dumps(task_json))
        except Exception as e:
            logger.error(f"_send_task 任务推送异常：{repr(e)}")

    async def _get_task_return(self, return_key: str):
        start_time = time.time()
        while time.time() - start_time < self._task_return_timeout:
            ret_value = await self._redis.get(return_key)
            if ret_value is not None:
                await self._redis.delete(return_key)
                task_result = TaskResult(json.loads(ret_value))
                if task_result.code == 200:
                    return task_result.data
                else:
                    raise TaskProcessingException(task_result.message, task_result.code)
            await asyncio.sleep(0.1)
        raise TaskReturnTimeout(f'等待任务结果返回超时: {return_key}')


class WechatBot(Base_bot):
    def __init__(self, service_flag: str, host: str = '127.0.0.1', port: int = 6379, password=None, time_range=None):
        """
        初始化机器人
        :param service_flag: 服务标志需要和wechaty服务端设置的一样
        :param host: redis主机地址
        :param port: redis端口
        :param password: redis服务的连接密码
        :param time_range: 忽略超时的事件的时间范围，单位：秒
        """
        super().__init__(host, port, service_flag, password)
        self._time_range = time_range


    async def close(self):
        await self._redis.close()


    async def listen(self) -> NoReturn:
        logger.info(f'wechaty客户端[{self.service_flag}]开始监听事件。')
        while True:
            try:
                list_name, pop = await self._redis.brpop([f"{self.service_flag}_event"])
            except Exception as e:
                logger.error(e)
                return
            asyncio.create_task(self.__process_event(pop))

    async def __process_event(self, event: str) -> NoReturn:
        event_items = (json.loads(event))
        # pprint(event_items)
        event_name = event_items['eventName']
        if self._time_range and (time.time()  - event_items['timestamp'] / 1000 > self._time_range):
            logger.info(f"忽略超出设置的时间范围的事件：{event_name}")
            return

        if event_name == 'message':
            if event_items[event_name].get('room'):
                event_name = 'group_message'
            else:
                event_name = 'contact_message'

        if event_name not in self._matcher:
            logger.info(f'未注册事件：{event_name}')
            return

        if event_name == 'server_error':
            event_object = ServerError(event_items[event_name])

        elif event_name == 'scan':
            event_object = Scan(event_items[event_name])

        elif event_name == 'login':
            event_object = Login(event_items[event_name])

        elif event_name == 'logout':
            event_object = Logout(event_items[event_name])

        elif event_name == 'group_message':
            event_object = GroupMessage(self, event_items['message'])

        elif event_name == 'contact_message':
            event_object = ContactMessage(self, event_items['message'])

        elif event_name == 'friendship':
            event_object = Friendship(self, event_items[event_name])

        elif event_name == 'group_invitation':
            event_object = GroupInvitation(self, event_items[event_name])

        elif event_name == 'group_name_change':
            event_object = GroupNameChange(event_items[event_name])

        elif event_name == 'group_member_join':
            event_object = GroupMemberJoin(event_items[event_name])

        elif event_name == 'group_member_leave':
            event_object = GroupMemberLeave(event_items[event_name])

        else:
            raise TypeError(f'不支持的事件类型：{event_name}')

        await self._matcher[event_name](event_object)

    async def _send_text_message(self,
                                receiver_type: ReceiverType,
                                receiver_id_list: List[str],
                                text: str,
                                interval,
                                mention_id_list: List[str] = None,
                               ) -> NoReturn:
        assert receiver_id_list, f"send_text_message: 接收者id列表不能为空。"
        await self._send_task('text_message',
                              {
                                  'receivers': receiver_id_list,
                                  'text': text,
                                  'interval': interval,
                                  'receiver_type': receiver_type.value,
                                  'mention_id_list': mention_id_list or []
                               })

    # wechaty-puppet-wechat4u 不支持
    # async def send_url_link(self,
    #                         receiver_type: ReceiverType,
    #                         receiver_id_list: List[str],
    #                         url_link: UrlLink,
    #                         interval: int=1000):
    #     await self._send_task('url_link',
    #                           {
    #                               'receivers': receiver_id_list,
    #                               'interval': interval,
    #                               'receiver_type': receiver_type.value,
    #                               'url_link': url_link.to_dict()
    #                           })

    async def forward_file(self,
                           receiver_type: ReceiverType,
                           receiver_id_list: List[str],
                           file_id: str,
                           interval: int=1000):
        assert receiver_id_list, f"forward_file: 接收者id列表不能为空。"
        assert file_id, f"forward_file: 文件id不能为空"
        await self._send_task('forward_file',
                              {
                                  'receivers': receiver_id_list,
                                  'file_id': file_id,
                                  'interval': interval,
                                  'receiver_type': receiver_type.value
                              })

    async def send_contact_text_message(self,
                                        text: str,
                                        contact_id_list: List[str],
                                        interval: int=1000):

        await self._send_text_message(ReceiverType.Contact, contact_id_list, text, interval)


    async def send_contact_file_message(self,
                                        file_name: str,
                                        contact_id_list: List[str],
                                        interval: int=1000):

        await self._send_task('file_message',
                          {
                              'receivers': contact_id_list,
                              'file_name': file_name,
                              'interval': interval,
                              'receiver_type': ReceiverType.Contact,
                           })


    async def send_group_text_message(self,
                                      text,
                                      group_id_list: List[str],
                                      interval: int=1000):

        await self._send_text_message(ReceiverType.Group, group_id_list, text, interval)


    async def send_group_file_message(self,
                                        file_name: str,
                                        group_id_list: List[str],
                                        interval: int=1000):

        await self._send_task('file_message',
                          {
                              'receivers': group_id_list,
                              'file_name': file_name,
                              'interval': interval,
                              'receiver_type': ReceiverType.Group,
                           })

    async def send_group_message_with_at(self, group_id:str, text:str, mention_id_list: List[str]):
        assert group_id, f'send_group_message_with_at：微信群id不能为空。'
        assert mention_id_list, f'send_group_message_with_at：提及联系人id列表不能为空。'
        await self._send_text_message(ReceiverType.Group,
                                      [group_id],
                                      text,
                                      1000,
                                      mention_id_list)

    async def accept_friend_verify(self, friendship_id: str) -> NoReturn:
        assert friendship_id, f"accept_friend_verify: 友谊事件id不能为空。"
        await self._send_task('accept_friend_verify',
                              {'friendship_id': friendship_id})

    async def accept_group_invitation(self, invitation_id: str) -> NoReturn:
        assert invitation_id, f'accept_group_invitation：邀请事件id不能为空。'
        await self._send_task('accept_group_invitation',
                              {'invitation_id': invitation_id})


    async def group_add_member(self, group_id:str, contact_id_list: List[str]):
        assert group_id, f'group_add_member：微信群id不能为空。'
        assert contact_id_list, f'group_add_member：联系人id列表不能为空。'

        await self._send_task('group_member_add',
                              {'group_id': group_id, 'contact_id_list': contact_id_list})


    async def group_remove_member(self, group_id:str, member_id_list: List[str]):
        assert group_id, f'group_remove_member：微信群id不能为空。'
        assert member_id_list, f'group_remove_member：联系人id列表不能为空。'
        await self._send_task('group_remove_member',
                              {'group_id': group_id, 'member_id_list': member_id_list})

    # wechaty-puppet-wechat4u 不支持
    # async def group_quit(self, group_id:str):
    #     assert group_id, f'group_quit：微信群id不能为空。'
    #     await self._send_task('group_quit', {'group_id': group_id})

    # wechaty-puppet-wechat4u 不支持
    # async def set_group_name(self, group_id:str, new_group_name:str):
    #     await self._send_task('set_group_name',
    #                           {'group_id': group_id, 'new_group_name': new_group_name})

    # wechaty-puppet-wechat4u 不支持
    # async def set_group_notice(self, group_id:str, new_group_notice:str):
    #     await self._send_task('set_group_notice',
    #                           {'group_id': group_id, 'new_group_notice': new_group_notice})

    # wechaty-puppet-wechat4u 不支持
    # async def set_friend_alias(self, friend_id:str, new_alias:str):
    #     await self._send_task('set_friend_alias',
    #                           {'friend_id': friend_id, 'new_alias': new_alias})

    async def _get_list(self, task_name: str, cls: Type[Union[Contact, Group]], items:Union[dict, None]=None):
        uuid = str(uuid4())
        await self._send_task(task_name, items=items, return_key=uuid)
        ret = await self._get_task_return(uuid)
        return [cls(items) for items in ret]


    async def get_contact_list(self):
        return await self._get_list('get_contact_list', Contact)

    async def get_friend_list(self):
        return await self._get_list('get_friend_list', Contact)

    async def get_group_list(self):
        return await self._get_list('get_group_list', Group)

    async def get_group_member_list(self, group_id: str):
        assert group_id, 'get_group_member_list：微信群id不能为空。'
        return await self._get_list('get_group_member_list', Contact, items={'group_id': group_id})

    # wechaty-puppet-wechat4u 不支持
    # async def get_group_qrcode(self, group_id: str):
    #     assert group_id, 'get_group_qrcode：微信群id不能为空。'
    #     uuid = str(uuid4())
    #     await self._send_task('get_group_qrcode', items={'group_id': group_id}, return_key=uuid)
    #     return await self._get_task_return(uuid)

    async def find_contacts(self, contact_name:str):
        assert contact_name, 'find_contacts：联系人名称不能为空。'
        return await self._get_list('find_contacts', Contact,
                                    items={'contact_name': contact_name})

    async def find_contacts_in_group(self, group_id: str, contact_name: str):
        assert contact_name, 'find_contacts_in_group：联系人名称不能为空。'
        return await self._get_list('find_contacts_in_group', Contact,
                                    items={'contact_name': contact_name, 'group_id': group_id})

    async def find_groups(self, group_name:str):
        assert group_name, 'find_groups：微信群名称不能为空。'
        return await self._get_list('find_groups', Group, items={'group_name': group_name})

