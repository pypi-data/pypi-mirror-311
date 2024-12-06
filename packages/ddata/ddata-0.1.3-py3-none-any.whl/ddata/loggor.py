import logging.config

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


def get_logger():
    return logger

# def get_logger(log_name=''):
#     log_config_path = os.path.dirname(os.path.abspath(__file__))
#     config_path = log_config_path + "/logging.conf"
#     # 当前相对目录下也有一份配置,实际生效的是下面绝对路径的配置文件
#     logging.config.fileConfig(config_path)
#     if log_name:
#         return logging.getLogger(log_name)
#     else:
#         logger = logging.getLogger()
#         return logger


def test():
    get_logger().info("hello")


if __name__ == "__main__":
    get_logger().info("hello")
