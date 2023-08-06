import logging
from knifes import alarm
from knifes.envconfig import config


# # critical级别日志报警  TODO 废弃
# class TimedRotatingFileWithCriticalAlarmHandler(TimedRotatingFileHandler):
#     def emit(self, record):
#         super(TimedRotatingFileWithCriticalAlarmHandler, self).emit(record)
#         if record.levelno == logging.CRITICAL:   # 前面添加NODE_ID
#             msg = f"[{record.module}]{record.getMessage()}"
#             if config('NODE_ID'):
#                 msg = f"[{config('NODE_ID')}]" + msg
#             alarm.async_send_msg(msg)


class CriticalAlarmFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.CRITICAL:
            msg = f"[{record.module}]{record.getMessage()}"
            if config('NODE_ID'):
                msg = f"[{config('NODE_ID')}]" + msg
            alarm.async_send_msg(msg)
        return True
