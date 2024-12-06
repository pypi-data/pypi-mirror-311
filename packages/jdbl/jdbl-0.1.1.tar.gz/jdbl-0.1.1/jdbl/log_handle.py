import time


class SupLogger(object):
	def __init__(self):
		pass

	@staticmethod
	def log(log_text, in_context, log_level, max_text_len=200):
		"""
		打印日志信息
		:param log_text: 打印信息
		:param in_context: 调用环境的上下文信息，可以调用时直接赋值 __name__
		:param log_level: 日志级别，Info、Warning、Error
		:param max_text_len: 最大打印长度，超过该长度会省略
		:return: None
		"""
		t_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		if in_context is None:
			in_context = ""
		if max_text_len != -1 and len(log_text) > max_text_len:
			log_text = f"{log_text[:max_text_len]}...(长度超过 {max_text_len} 省略)"
		if log_level == "Info":
			print(f"\033[1;32m[{log_level}]\033[0m {t_str} {in_context} {log_text}")
		elif log_level == "Warning":
			print(f"\033[1;33m[{log_level}]\033[0m {t_str} {in_context} {log_text}")
		elif log_level == "Error":
			print(f"\033[1;31m[{log_level}]\033[0m {t_str} {in_context} {log_text}")
		elif log_level == "Debug":
			print(f"\033[1;34m[{log_level}]\033[0m {t_str} {in_context} {log_text}")

	@staticmethod
	def info(text, in_context=None, max_text_len=200):
		SupLogger.log(text, in_context, "Info", max_text_len)

	@staticmethod
	def warning(text, in_context=None, max_text_len=200):
		SupLogger.log(text, in_context, "Warning", max_text_len)

	@staticmethod
	def error(text, in_context=None, max_text_len=200):
		SupLogger.log(text, in_context, "Error", max_text_len)

	@staticmethod
	def debug(text, in_context=None, max_text_len=200):
		SupLogger.log(text, in_context, "Debug", max_text_len)

