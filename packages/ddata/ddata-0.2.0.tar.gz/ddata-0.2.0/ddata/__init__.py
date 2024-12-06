from .date import DateUtil
date = DateUtil()

from .loggor import MyLoggor
log = MyLoggor()


# 将方法绑定到包级别，使得可以直接用包名调用
from.test import log_message
test = log_message


