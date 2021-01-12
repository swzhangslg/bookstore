import logging
logging.basicConfig(
    level=logging.INFO,  # 设置日志的显示级别为最低一级
    filename="logger.log",  # 设置日志的显示文件名
    filemode='w',  # 设置日志的写入方式为追加
    format='%(asctime)s %(filename)s [%(lineno)d] %(message)s',  # 设置一个输出模板格式
)
def a():
    logging.info("111")
a()