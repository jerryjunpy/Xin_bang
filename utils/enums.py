# coding: utf-8
from enum import IntEnum


class Status(IntEnum):
    SUCCESSFUL = 0  # 成功
    FAILURE = 1  # 失败

    NO_DATA = 2004  # 无数据

    ARGUMENT_ERROR = 4000  # 参数错误
    PERMISSION_ERROR = 4001  # 权限或签名错误
    REQUEST_METHOD_ERROR = 4005  # 请求的方法不存在

    SERVER_ERROR = 5000  # 服务器错误

    THIRD_PARTY_ERROR = 6000  # 第三方错误

    @property
    def code(self):
        return self.value

    @property
    def message(self):
        return Message[self] or self.name


class Message(object):
    __MAPPINGS = {
        Status.SUCCESSFUL: "成功",
        Status.FAILURE: "失败",

        Status.NO_DATA: "无数据",

        Status.ARGUMENT_ERROR: "参数错误",
        Status.PERMISSION_ERROR: "权限或签名错误",
        Status.REQUEST_METHOD_ERROR: "请求方法错误",

        Status.SERVER_ERROR: "服务器错误",

        Status.THIRD_PARTY_ERROR: "第三方错误",
    }

    def __getitem__(self, item):
        return self.__MAPPINGS.get(item)


Message = Message()


class HouseDataType(IntEnum):
    SECOND_HAND_HOUSE = 1  # 中介挂盘(二手房)
    TRADING_CASE = 2  # 成交案例
    JUDICIAL_SALE = 3  # 司法拍卖


class RequestDataReturnTypes(IntEnum):
    """
    response返回数据类型枚举
    废弃，别再使用
    """
    RAW = 0
    TEXT = 1
    BYTE = 2
    JSON = 3

    def __eq__(self, other):
        if isinstance(other, str):
            return other.upper() == self.name.upper()
        return super(RequestDataReturnTypes, self).__eq__(other)
