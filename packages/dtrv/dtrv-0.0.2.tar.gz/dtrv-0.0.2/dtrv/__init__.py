import os
from dtrv.v1 import (
    Client, Method
)
from dtrv import util

# vault 地址及凭证
vault_host = os.environ.get("VAULT_HOST")
vault_token = os.environ.get("VAULT_TOKEN")

# 当前 token 有效时间 (hour)
vault_token_timestamp = 0.0

# vault 需要获取的 kv 列表名称
vault_kv_secret_namelist = []

# 钉钉机器人 token 列表
# example: {"token": "xx", "secret": "xx"}
dingtalk_robot_token_list = []

__all__ = [
    "Client",
    "Method",
    "vault_host",
    "vault_token",
    "vault_token_timestamp",
    "vault_kv_secret_namelist",
    "dingtalk_robot_token_list",
    "util"
]