import logging.config


class MyLoggor():
    # 配置日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler()]
    )

    def __get_logger(self):
        logger = logging.getLogger(__name__)
        return logger

    def info(self, message):
        self.__get_logger().info(message)

    def warn(self, message):
        self.__get_logger().warning(message)

    def error(self):
        self.__get_logger().error("hello")


if __name__ == "__main__":
    log = MyLoggor()
    log.info("hello")
    print("hello")
