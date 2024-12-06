# jdbl
A json based database library, RAM running and including basic read-write lock.

TODO:
- [ ] add documentation


# What is jdb?
`jdb` means json based database, but with some fixed structure.

## database & table
jdbl made its own file format, `.jdb`.

A `.jdb` file's data is a database(db) itself. Its each key is a table(tb) name, and the value is a table data.

Seems like this:
```json
// db1.jdb
{
    "tb1": {...},
    "tb2": {...}
}
```

## table data
As said above, the value of each key of jdb is a table data. A table data is a json format data too, with two fixed keys: `columns` and `rows`.

The value of `columns` is a list of columns' infos, and the value of `rows` is a list of rows' datas.

Seems like this:
```json
// db1.jdb
{
    "tb1": {
        "columns": [...],
        "rows": [...],
    },
    "tb2": {
        "columns": [...],
        "rows": [...],
    }
}
```

For understanding better, let's see `rows` structure first.

### rows
`rows` is a list of row data, it is a list of dict. And each row data is a dict, with attribute name as key, and attribute value as value. You can think a row data is descrbibing like: A person with name "Alice", age 18.

So rows datas seems like this:
```json
...
    "rows": [
        {"id": "32132654", "name": "Alice", "age": 18, ...},
        {"id": "65653251", "name": "Jerry", "age": 19, ...},
        ...
    ],
...
```
Each attribute name would have a corresponding column info in `columns`. As you can see below.

### columns
`columns` is a list of column infos, it is a list of dict too. Each column info is a dict, with column's info name as key, and column's info value as value.

There are two fixed info names are fixed.
- `name`: the name of the column.
- `rname`: the readable name of the column.

And any other info names are custom info names, you can define them by yourself. The jdbl library would make sure that every row data attribute name is in the `columns` list.

Seems like this:
```json
...
    "columns": [
        {"name": "id", "rname": "ID", ...},
        {"name": "name", "rname": "Person's name", ...},
        {"name": "age", "rname": "Person's age", ...},
    ],
...
```

# How to use
This `jdbl` library helps handle `.jdb` file, and it provides some functions to operate the database.

## install & import
You can install it by pip:
```
pip install jdbl
```
And import it:
```python
from jdbl import jdb_handler
```

## Lock & Unlock
In order to avoid data corruption for multi-threaded, multi-processed environment, `jdbl` provides read-write lock directly. It means when you used(read or write) one jdb file, the file would be locked up.
To make the api more readable, the function is named `use` and `un_use`.

### use & un_use
`use` function is used to lock the jdb file, and `un_use` function is used to unuse the jdb file.

```python
# lock the jdb file
jdb_handler.use("db1")

# unlock the jdb file
jdb_handler.un_use("db1")
```

When you use a jdb, you should make sure that you unlock it after you finish using it. Otherwise next time you use the same jdb, it would be block for five seconds and print a warning.

## Query Datas
As it is a json format with fixed structure, you can use `json` library to get datas directly. But `jdbl` provides some functions to make it more readable.

### get_tb_data
`get_tb_data` function is used to get the table data of a table.

```python
tb_data = jdb_handler.get_tb_data("db1", "tb1")
```

### query_rows
`query_row` function is used to query the rows that with some conditions. For now, it searches rows by `col_name` and `col_value` provided.

```python
rows = jdb_handler.query_rows("db1", "tb1", "name", "Alice")
```
This would return a list of row data dict that with `name` attribute value is "Alice".

## Write Datas
As it is a json format with fixed structure, you can use `json` library to write datas directly. But `jdbl` provides some functions to make it more readable.

### add_rows
`add_rows` function is used to add rows to a table. And it has upsert mode. Which would just update the row if it exists, or add the row if it doesn't exist.

```python
row_datas = [
    {"id": "32132654", "name": "Alice", "age": 18, ...},
    {"id": "65653251", "name": "Jerry", "age": 19, ...},
    ...
]
jdb_handler.add_rows("db1", "tb1", row_datas, "name", upsert_mode=True)
```

This would add the rows to `tb1` table in `db1` database. If the row with `name` attribute value is "Alice" exists, it would be updated. Otherwise it would be added.

## One-time functions
As said above, normally you need to `use` a jdb and do something with it, then you need to `un_use` it. It is for fast RAM running when you need to do many operations to one jdb. But for some one time operation like "reading the table and do nothing else", the use-do-un_use steps are a little bit annoying. So `jdbl` provides some one-time functions to make it more convenient.

Here're some one-time functions like:
- `get_tb_data_once`
- `query_rows_once`
- `add_rows_once`

They are the same as the normal functions, but you don't need to `use` and `un_use` the jdb yourself, the function would do it for you.