import os
from appdirs import AppDirs

from .log_handle import SupLogger


class UtilUtils(object):
	@staticmethod
	def list_remove_duplicates_ordered(origin_list):
		seen = set()
		return [x for x in origin_list if not (x in seen or seen.add(x))]

	@staticmethod
	def form_k_dict(dict_list, k_name):
		"""
		对于给定的字典列表，构建以其 k_name 键的值为键的字典；意味着，原列表中每个字典的 k_name 对应的值需要不同。
		:param dict_list: 字典列表
		:param k_name: 需要作为新键的值，在原字典列表中的键
		:return: 以其 k_name 键的值为键的字典
		"""
		if not isinstance(dict_list, list):
			return {}
		k_dict = {}
		for d in dict_list:
			if not isinstance(d, dict):
				continue
			for k, v in d.items():
				if k == k_name:
					k_dict[v] = d
					break
		return k_dict


class DirFileUtils(object):
	@staticmethod
	def exist_and_is_type(file_path: str, type_name: str) -> bool:
		if not type_name.startswith('.'):
			type_name = f".{type_name}"
		return os.path.isfile(file_path) and file_path.endswith(type_name)

	@staticmethod
	def exist_and_of_types(file_path: str, type_names: list) -> bool:
		if not os.path.isfile(file_path):
			return False
		for type_name in type_names:
			if not type_name.startswith('.'):
				type_name = f".{type_name}"
			if file_path.endswith(type_name):
				return True
		return False

	@staticmethod
	def ensure_dir(dst_dir: str, auto_overwrite=True):
		if os.path.isdir(dst_dir):
			return
		if not auto_overwrite:
			confirm = input(f"([Y]/n) 确认要新建该路径么: {dst_dir}")
			if confirm not in ["Y", "y", "\n", ""]:
				return
		os.makedirs(dst_dir, True)
		SupLogger.info(f"已新建路径 {dst_dir}", "env_handle")

	@staticmethod
	def get_app_dir(app_name: str, app_author=""):
		return AppDirs(app_name, appauthor=app_author).user_data_dir


if __name__ == "__main__":
	pass
