import hvac
from hvac.exceptions import Forbidden
import os
import logging
from abc import ABCMeta
from dtrv import util

logger = logging.getLogger(__name__)

class Client(metaclass=ABCMeta):

    def __init__(self):

        super(Client, self).__init__()

        self.vault_host = util.default_vault_host()
        self.vault_token = util.default_vault_token()

        self.client = hvac.Client(url=self.vault_host, token=self.vault_token)
        self.sign()

    def sign(self):
        """
        身份验证
        :return:
        """
        return self.client.is_authenticated()

    def get_kv(self, key, point='dingtalk'):
        """
        读取 kv 数据
        :param key:
        :param point:
        :return:
        """
        try:
            return self.client.secrets.kv.read_secret_version(path=key, mount_point=point)["data"]["data"]
        except BaseException as err:
            return False

    def get_token_info(self, token=None):
        """
        获取凭证租约信息
        :param lease_id:
        :return:
        """
        try:
            if token:
                res = self.client.auth.token.lookup(token)
                util.set_vault_timestamp(res["data"]["expire_time"])
                return res
            res = self.client.auth.token.lookup_self()
            util.set_vault_timestamp(util.calculate_hours_for_both_timestamps(util.string_formatting_timestamp(res["data"]["expire_time"])))
            return res
        except BaseException as err:
            return err

    def set_token_renew(self, token=None):
        """
        凭证续租, 默认增加 3d
        :param lease_id:
        :return:
        """
        try:
            if token:
                return self.client.auth.token.renew(token=token)
            return self.client.auth.token.renew_self()
        except BaseException as err:
            return err