import os
import json
import uuid
import time

from .util_utils import UtilUtils, DirFileUtils

from .log_handle import SupLogger


class BatchQueryResult(object):
	def __init__(self):
		self.row_datas = []
		self.success_values = []
		self.success_v_rows_map = {}


class JDBHandler(object):
	"""
	自创的json形式数据库。JDB。
	每个数据库db为一个字典，一级key对应表tb，每个tb的key对应line
	默认每个tb拥有两个key：columns和rows。columns以列表形式存储列信息，rows以列表形式存储每行数据字典。
	默认每行数据都有id列。
	"""
	def __init__(self):
		self.db_datas = {}

	# region 通用方法
	@staticmethod
	def _get_uid():
		return str(uuid.uuid1())

	@staticmethod
	def ensure_app_databases_dir():
		app_dir = DirFileUtils.get_app_dir("py-jdb")
		db_dir = os.path.join(app_dir, "databases")
		DirFileUtils.ensure_dir(db_dir)
		return db_dir

	@staticmethod
	def _form_jdb_path(db_name, db_dir=None):
		if not db_name.endswith(".jdb"):
			db_name += ".jdb"
		if db_dir is None or db_dir == "":
			db_dir = JDBHandler.ensure_app_databases_dir()
		db_path = os.path.join(db_dir, db_name)
		return db_path

	@staticmethod
	def _form_jdb_key(db_path):
		db_key = db_path.replace(":", "")
		db_key = db_key.replace("\\", "")
		db_key = db_key.replace("/", "")
		db_key = db_key.replace(".jdb", "")
		return db_key

	@staticmethod
	def _get_checked_all_data(db_name, all_data):
		checked_all_data = all_data.copy()
		for tb_name, tb_data in all_data.items():
			if "rows" not in tb_data:
				continue
			checked_rows = [row for row in tb_data["rows"] if "rows" in tb_data and row]
			checked_all_data[tb_name]["rows"] = checked_rows
		return checked_all_data

	@staticmethod
	def _ensure_id(row_datas):
		if isinstance(row_datas, dict):
			row_datas = [row_datas]
		for i in range(len(row_datas)):
			row_data = row_datas[i]
			if "id" not in row_data or not row_data["id"]:
				row_datas[i]["id"] = JDBHandler._get_uid()
		return row_datas

	def _ensure_row_datas_col(self, db_name, tb_name, row_datas, db_dir=None):
		if not row_datas:
			return
		db_path = self._form_jdb_path(db_name, db_dir)
		if isinstance(row_datas, dict):
			row_datas = [row_datas]
		c_names = []
		for row_data in row_datas:
			c_names.extend(row_data.keys())
		c_names = UtilUtils.list_remove_duplicates_ordered(c_names)
		tb_data = self.get_tb_data(db_name, tb_name, db_dir)
		if not tb_data:
			tb_data = {}
		if "columns" not in tb_data:
			tb_data["columns"] = []
		if "rows" not in tb_data:
			tb_data["rows"] = row_datas
		cur_cols = UtilUtils.form_k_dict(tb_data["columns"], "name")
		c_names_need_add = [c_name for c_name in c_names if c_name not in cur_cols]
		for col_name in c_names_need_add:
			if col_name:
				tb_data["columns"].append({"name": col_name, "rname": col_name})
			# 其它行也刷一遍 需要么？
			for i in range(len(tb_data["rows"])):
				if col_name in tb_data["rows"][i]:
					continue
				tb_data["rows"][i][col_name] = ""

		self.db_datas[db_path][tb_name] = tb_data

	def new_db(self, db_name, db_dir=None, should_overwrite=False):
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		if os.path.isfile(db_path) and not should_overwrite:
			return
		self.db_datas[db_path] = {}

	def new_tb(self, db_name, tb_name, db_dir=None):
		db_path = self._form_jdb_path(db_name, db_dir)
		self.db_datas[db_path] = {tb_name: {}}
		if tb_name not in self.db_datas[db_path]:
			self.db_datas[db_path][tb_name] = {}
		self.db_datas[db_path][tb_name] = {"columns": [], "rows": []}

	# endregion

	# region 锁
	def _lock_db(self, db_name, db_dir=None):
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		db_lock_name = JDBHandler._form_jdb_key(db_path)
		db_dir = self.ensure_app_databases_dir()
		lock_file_path = os.path.join(db_dir, db_lock_name + ".lock")

		if not self.is_db_exist(db_name, db_dir):
			# 不存在直接获得锁
			open(lock_file_path, "w+", encoding="utf-8").close()
			return True
		if os.path.isfile(lock_file_path):
			return False
		open(lock_file_path, "w+", encoding="utf-8").close()
		return True

	def _unlock_db(self, db_name, db_dir=None):
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		db_lock_name = JDBHandler._form_jdb_key(db_path)
		db_dir = self.ensure_app_databases_dir()
		lock_file_path = os.path.join(db_dir, db_lock_name + ".lock")
		if not os.path.exists(lock_file_path):
			SupLogger.warning("存在调用问题，解锁文件不存在: " + lock_file_path, in_context="JDBHandler._unlock")
		else:
			os.remove(lock_file_path)

	# endregion

	# region 判断方法
	@staticmethod
	def is_db_exist(db_name, db_dir=None):
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		return os.path.isfile(db_path)

	def is_db_used(self, db_name, db_dir=None):
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		return db_path in self.db_datas

	@staticmethod
	def get_all_db_names(db_dir=None):
		if not db_dir:
			db_dir = JDBHandler.ensure_app_databases_dir()
		db_names = []
		for file in os.listdir(db_dir):
			if file.endswith(".jdb"):
				db_names.append(file[:-4])
		return db_names

	@staticmethod
	def del_db(db_name, db_dir=None):
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		if os.path.isfile(db_path):
			os.remove(db_path)

	def is_tb_exist(self, db_name, tb_name, db_dir=None):
		temp_use = False
		if not self.is_db_exist(db_name, db_dir):
			return False
		if not self.is_db_used(db_name, db_dir):
			self.use(db_name, db_dir)
			temp_use = True
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		db_data = self.db_datas.get(db_path)
		if not db_data:
			return False
		tb_exist = tb_name in db_data
		if temp_use:
			self.un_use(db_name, db_dir)
		return tb_exist

	def _ensure_db_tb(self, db_name, tb_name, db_dir=None):
		if not self.is_db_used(db_name, db_dir):
			self.new_db(db_name, db_dir)
			self._lock_db(db_name, db_dir)
		if tb_name not in self.db_datas[JDBHandler._form_jdb_path(db_name, db_dir)]:
			self.new_tb(db_name, tb_name, db_dir)

	def rows_count(self, db_name, tb_name, db_dir=None):
		if not self.is_tb_exist(db_name, tb_name, db_dir):
			return -1
		tb_data = self.get_tb_data(db_name, tb_name, db_dir)
		return len(tb_data["rows"])

	# endregion

	# region 加载保存
	def use(self, db_name, db_dir=None):
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		if not JDBHandler.is_db_exist(db_name, db_dir):
			self._lock_db(db_name, db_dir)
			self.db_datas[db_path] = {}
			return True
		t1 = time.time()
		while True:
			got_lock = self._lock_db(db_name, db_dir)
			if not got_lock:
				t = time.time()
				if t - t1 < 5:
					continue
				else:
					SupLogger.warning("jdb等锁超过5s，将直接读取" + db_path, in_context="JDBHandler.load_db")
			with open(db_path, "r+", encoding="utf-8") as fdb:
				try:
					db_data = json.load(fdb)
					self.db_datas[db_path] = db_data
					# if got_lock:
					# 	self._unlock_db(db_name, db_dir)
					return True
				except Exception as e:
					SupLogger.error("jdb文件错误: " + str(e), in_context="JDBHandler.get_all_data")
					return False

	def un_use(self, db_name, db_dir=None):
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		if db_path in self.db_datas:
			self.db_datas.pop(db_path)
		self._unlock_db(db_name, db_dir)

	def save(self, db_name, db_dir=None, indent=2):
		if not self.is_db_used(db_name, db_dir):
			return
		db_path = JDBHandler._form_jdb_path(db_name, db_dir)
		self._lock_db(db_name, db_dir)
		db_data = self.db_datas[db_path]
		checked_all_data = JDBHandler._get_checked_all_data(db_name, db_data)
		db_path = JDBHandler._form_jdb_path(db_name, db_dir=db_dir)
		with open(db_path, "w+", encoding="utf-8") as fdb:
			json.dump(checked_all_data, fdb, ensure_ascii=False, indent=indent)
		self.db_datas.pop(db_path)
		self._unlock_db(db_name, db_dir)

	def get_db_data(self, db_name, db_dir=None):
		db_path = self._form_jdb_path(db_name, db_dir)
		db_data = self.db_datas.get(db_path)
		if not db_data:
			SupLogger.warning(f"jdb未使用 {db_path}", "JDBHandler.get_db_data")
			return None
		return db_data

	def get_tb_data(self, db_name, tb_name, db_dir=None):
		db_path = self._form_jdb_path(db_name, db_dir)
		db_data = self.db_datas.get(db_path)
		if not db_data:
			SupLogger.warning(f"jdb未使用 {db_path}", "JDBHandler.get_tb_data")
			return None
		return db_data.get(tb_name)

	# endregion

	# region 查询
	def query_row(self, db_name, tb_name, col_name, col_value, db_dir=None, show_debug=True) -> dict | None:
		query_result = self.query_rows(db_name, tb_name, col_name, col_value, db_dir=db_dir)
		if not query_result:
			if show_debug:
				SupLogger.warning(f"该索引条件未得到数据结果: {db_name} 库 {tb_name} 表中，{col_name}: {col_value}", "JDBHandler.query_row")
			return None
		if len(query_result) > 1:
			if show_debug:
				SupLogger.warning(f"该索引条件存在多条数据结果，将返回第一条: {db_name} 库 {tb_name} 表中，{col_name}: {col_value}", "JDBHandler.query_row")
		return query_result[0]

	def batch_query_rows(self, db_name, tb_name, col_name, col_values, db_dir=None) -> BatchQueryResult:
		"""
		  批量查询指定列中包含不同指定值的行
		  :param db_name: 数据库名
		  :param tb_name: 表名
		  :param col_name: 列名
		  :param col_values: 不同指定值列表
		  :param db_dir: 数据库目录
		  :return: BatchQueryResult 包含查询结果和成功查询的值
		"""
		batch_result = BatchQueryResult()
		if not self.is_tb_exist(db_name, tb_name, db_dir=db_dir):
			return batch_result
		tb_data = self.get_tb_data(db_name, tb_name, db_dir=db_dir)
		rows_data = tb_data.get("rows") if tb_data else []
		if not rows_data:
			return batch_result
		query_results = []
		query_success_values = []
		for col_value in col_values:
			for row in rows_data:
				if col_name in row and row[col_name] == col_value:
					query_results.append(row)
					query_success_values.append(col_value)
					batch_result.success_v_rows_map[col_value] = row
					continue
		batch_result.row_datas = query_results
		batch_result.success_values = query_success_values
		return batch_result

	def query_rows(self, db_name, tb_name, col_name, col_value, db_dir=None):
		"""
		查询指定列中包含指定值的行
		:param db_name:
		:param tb_name:
		:param col_name:
		:param col_value:
		:param db_dir:
		:return:
		"""
		if not self.is_tb_exist(db_name, tb_name, db_dir):
			return []
		tb_data = self.get_tb_data(db_name, tb_name, db_dir=db_dir)
		row_datas = tb_data.get("rows") if tb_data else []
		if not row_datas:
			return []
		return [row for row in row_datas if (col_name in row and str(row[col_name]) and str(row[col_name]) == str(col_value))]

	def query_rows_filter_mode(self, db_name, tb_name, col_name, col_value, db_dir=None):
		"""
		查询指定列中包含指定值的行
		:param db_name:
		:param tb_name:
		:param col_name:
		:param col_value:
		:param db_dir:
		:return:
		"""
		if not self.is_tb_exist(db_name, tb_name, db_dir):
			return []
		tb_data = self.get_tb_data(db_name, tb_name, db_dir=db_dir)
		rows_data = tb_data.get("rows") if tb_data else []
		if not rows_data:
			return []
		query_result_rows = []
		for row_data in rows_data:
			if col_name in row_data and col_value in str(row_data[col_name]):
				query_result_rows.append(row_data)
		return query_result_rows

	def query_col_all_rows(self, db_name, tb_name, col_name, db_dir=None):
		"""
		查询指定列中所有行的值
		:param db_name:
		:param tb_name:
		:param col_name:
		:param db_dir:
		:return:
		"""
		if not self.is_tb_exist(db_name, tb_name, db_dir):
			return []
		tb_data = self.get_tb_data(db_name, tb_name, db_dir=db_dir)
		rows = tb_data.get("rows") if tb_data.get("rows") else []
		if not rows:
			return []
		query_result = []
		for row in rows:
			for key, value in row.items():
				if key == col_name and value not in query_result:
					query_result.append(value)
		return query_result

	# endregion

	# region 增删
	def add_rows(self, db_name, tb_name, row_datas, row_data_key, upsert_mode=False, db_dir=None, show_debug=True):
		if not row_datas:
			return

		self._ensure_db_tb(db_name, tb_name, db_dir=db_dir)
		self._ensure_row_datas_col(db_name, tb_name, row_datas, db_dir=db_dir)
		row_datas = self._ensure_id(row_datas)

		row_datas_to_extend = []
		row_datas_to_update = []

		# 筛选已有记录
		key_col_values = [row_data[row_data_key] for row_data in row_datas]
		batch_result = self.batch_query_rows(db_name, tb_name, row_data_key, key_col_values, db_dir=db_dir)

		for row_data in row_datas:
			if row_data[row_data_key] in batch_result.success_v_rows_map:
				data = batch_result.success_v_rows_map[row_data[row_data_key]]
				if upsert_mode:
					if row_data["id"]:
						row_data["id"] = data["id"]
					row_datas_to_update.append(row_data)
				else:
					if show_debug:
						SupLogger.warning(f"{db_name} 库 {tb_name} 表已有该行: {row_data[row_data_key]}",
						                  "JDBHandler.add_row")
				continue
			row_datas_to_extend.append(row_data)

		tb_data = self.get_tb_data(db_name, tb_name, db_dir=db_dir)
		if "rows" not in tb_data:
			tb_data["rows"] = []
		if row_datas_to_extend:
			tb_data["rows"].extend(row_datas_to_extend)
		for row_data in row_datas_to_update:
			for i in range(len(tb_data["rows"])):
				if not isinstance(tb_data["rows"][i], dict):
					continue
				if tb_data["rows"][i][row_data_key] == row_data[row_data_key]:
					tb_data["rows"][i] = row_data
		db_path = self._form_jdb_path(db_name, db_dir)
		self.db_datas[db_path][tb_name] = tb_data

	def remove_row(self, db_name, tb_name, row_data, db_dir=None):
		if not self.is_tb_exist(db_name, tb_name, db_dir):
			return
		tb_data = self.get_tb_data(db_name, tb_name, db_dir)
		if "id" not in row_data:
			return
		for i in range(len(tb_data["rows"])):
			row = tb_data["rows"][i]
			if "id" not in row:
				continue
			if row["id"] == row_data["id"]:
				del tb_data["rows"][i]
				db_path = self._form_jdb_path(db_name, db_dir)
				self.db_datas[db_path][tb_name] = tb_data
				break

	def add_cols(self, db_name, tb_name, col_datas, db_dir=None):
		if not col_datas:
			return
		self._ensure_db_tb(db_name, tb_name, db_dir=db_dir)
		tb_data = self.get_tb_data(db_name, tb_name, db_dir=db_dir)
		if "columns" not in tb_data:
			tb_data["columns"] = []
		for col_data in col_datas:
			if col_data not in tb_data["columns"]:
				tb_data["columns"].append(col_data)
		db_path = self._form_jdb_path(db_name, db_dir)
		self.db_datas[db_path][tb_name] = tb_data

	def remove_col(self, db_name, tb_name, col_name, db_dir=None):
		if not self.is_tb_exist(db_name, tb_name, db_dir):
			return
		tb_data = self.get_tb_data(db_name, tb_name, db_dir=db_dir)
		cols = tb_data.get("columns")
		if not cols:
			return
		for i in range(len(tb_data["columns"])):
			col = cols[i]
			if "name" not in col:
				continue
			if col["name"] == col_name:
				del cols[i]
				db_path = self._form_jdb_path(db_name, db_dir)
				self.db_datas[db_path][tb_name]["columns"] = cols
				break

	def replace_tb(self, db_name, tb_name, tb_data, db_dir=None):
		self._ensure_db_tb(db_name, tb_name, db_dir=db_dir)
		db_path = self._form_jdb_path(db_name, db_dir)
		self.db_datas[db_path][tb_name] = tb_data

	# endregion

	# region 单次操作方法
	def get_db_data_once(self, db_name, db_dir=None):
		self.use(db_name, db_dir)
		db_data = self.get_db_data(db_name, db_dir=db_dir)
		self.un_use(db_name, db_dir)
		return db_data

	def get_tb_data_once(self, db_name, tb_name, db_dir=None):
		self.use(db_name, db_dir)
		tb_data = self.get_tb_data(db_name, tb_name, db_dir=db_dir)
		self.un_use(db_name, db_dir)
		return tb_data

	def query_row_once(self, db_name, tb_name, col_name, col_value, db_dir=None):
		self.use(db_name, db_dir)
		result = self.query_row(db_name, tb_name, col_name, col_value, db_dir=db_dir)
		self.un_use(db_name, db_dir)
		return result

	def query_rows_once(self, db_name, tb_name, col_name, col_value, db_dir=None):
		self.use(db_name, db_dir)
		results = self.query_rows(db_name, tb_name, col_name, col_value, db_dir=db_dir)
		self.un_use(db_name, db_dir)
		return results

	def query_col_all_rows_once(self, db_name, tb_name, col_name, db_dir=None):
		self.use(db_name, db_dir)
		results = self.query_col_all_rows(db_name, tb_name, col_name, db_dir=db_dir)
		self.un_use(db_name, db_dir)
		return results

	def query_rows_filter_mode_once(self, db_name, tb_name, col_name, col_value, db_dir=None):
		self.use(db_name, db_dir)
		results = self.query_rows_filter_mode(db_name, tb_name, col_name, col_value, db_dir=db_dir)
		self.un_use(db_name, db_dir)
		return results

	def batch_query_rows_once(self, db_name, tb_name, col_name, col_values, db_dir=None):
		self.use(db_name, db_dir)
		b_q_results = self.batch_query_rows(db_name, tb_name, col_name, col_values, db_dir=db_dir)
		self.un_use(db_name, db_dir)
		return b_q_results

	def add_rows_once(self, db_name, tb_name, row_datas, row_data_key, upsert_mode=False, db_dir=None, show_debug=True):
		self.use(db_name, db_dir)
		self.add_rows(db_name, tb_name, row_datas, row_data_key, upsert_mode, db_dir=db_dir, show_debug=show_debug)
		self.save(db_name, db_dir)

	def replace_tb_once(self, db_name, tb_name, tb_data, db_dir=None):
		self.use(db_name, db_dir)
		self.replace_tb(db_name, tb_name, tb_data, db_dir=db_dir)
		self.save(db_name, db_dir)

	# endregion

	def test(self):
		pass


jdb_handler = JDBHandler()


if __name__ == "__main__":
	pass
