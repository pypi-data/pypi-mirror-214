from functools import wraps
import dtrv
import time
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, filename='/dev/stdout', filemode='a', format='%(message)s')

def InitializeTheVaultTokenLease(func):
    """
    初始化 Value Token 租期
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        执行函数之前的方法
        :param args:
        :param kwargs:
        :return:
        """
        try:
            # 实例化 drv
            drv_object = dtrv.Client()
            # 获取租期
            drv_object.get_token_info()
            # 判定租期等于或小于 1 小时进行续租
            if float(dtrv.vault_token_timestamp) >= 1:
                drv_object.set_token_renew()
        except BaseException as err:
            logging.error("装饰器异常错误: {}".format(err))
        func(*args, **kwargs)
    return wrapper

def UpdateDingtalkKvData(func):
    """
    更新 DingTalk 秘钥数据
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        执行函数之前的方法
        :param args:
        :param kwargs:
        :return:
        """
        try:
            # 实例化 drv
            drv_object = dtrv.Client()
            _tmp_dingtalk_robot_token_list = []
            # 获取 keyName 列表并循环
            for keyName in dtrv.vault_kv_secret_namelist:
                res = drv_object.get_kv(key=keyName)
                if res:
                    _tmp_dingtalk_robot_token_list.append({"token": res["token"], "secret": res["secret"]})
            dtrv.dingtalk_robot_token_list = _tmp_dingtalk_robot_token_list
        except BaseException as err:
            logging.error("装饰器异常错误: {}".format(err))
        func(*args, **kwargs)

    return wrapper

def ChekcExecutionTime(CustomName=''):
    def chekcExecutionTime(func):
        def wrapper(*args, **kwargs):
            """
            检查方法执行时间
            :param args:
            :param kwargs:
            :return:
            """
            t = time.perf_counter()
            func(*args, **kwargs)
            logging.info(f"{CustomName} Coast:{time.perf_counter() - t:.8f}s")
        return wrapper
    return chekcExecutionTime