
![Build Status](https://drone-ext.mcos.nc/api/badges/scrippy/scrippy-db/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

![Scrippy, my scrangourou friend](./scrippy-db.png "Scrippy, my scrangourou friend")

# `scrippy-db`

Generic database client for the [`Scrippy`](https://codeberg.org/scrippy) framework.

## Requirements

### Python modules

#### List of required modules

The modules listed below will be installed automatically.

- psycopg2-binary
- cx-Oracle
- mysql-connector-python

## Installation

### With `pip`

```bash
pip install scrippy-db
```

### Manual installation

```bash
git clone https://codeberg.org/scrippy/scrippy-db.git
cd scrippy-db
python -m pip install -r requirements.txt
make install
```


### Usage

The `scrippy_db.db` module provides the `Database` object, which is intended to offer database usage functionality.

Connection to a database can be done either by directly providing connection parameters (`db_type`,  `username`, `host`, `database`, `port`, `password`) to the constructor, or by providing the name of the _service_ to connect to.

The `db_type` parameter allows you to specify the type of database (`sqlite3`, `postgres`, `mysql` or `oracle`).

Note that *Oracle* database is not tested as much as the other types of database.


#### Simple query

Query execution is performed with the `Database.execute()` method, which accepts the following parameters:
- `query`: The query itself (required)
- `params`: The query parameters in the exact order of appearance within the query (optional)
- `verbose`: Boolean. If set to `True`, each query, parameter and result will be sent to the logger.
- `commit`: Boolean. When set to `True`, a commit statement will be sent to the database immediately after the query execution. default to `False`.
- `exit_on_error`: Boolean. If set to `True`, any error encountered while query execution will raise an error and exit the script after query rollback. Default to `True`.

A query may contain one or more variable parameters requiring the query to be adapted to these parameters.

In conformance to [*Python Database API v2.0*](https://peps.python.org/pep-0249), parameters may be provided as sequence or mapping and will be bound to variables in the operation. If error occurs while query execution, the query will be *rollbacked*.

The query format depends on the database type. See the [query formatting section](#query-formatting) below for further details.

For security reasons, **never** try to manage the interpolation of parameters inside the query yourself.


#### Multiple queries

A single query can be executed multiple times with multiple set of parameters using the `Database.multi_query()` method, which accepts the following parameters:
- `query`: The query itself as a string with placeholders for parameters (required)
- `paramlist`: A mandatory list of dictionaries specifying the needed parameters to be mapped on each execution of the `query` string.
- `verbose`: Boolean. If set to `True`, each query, parameter and result will be sent to the logger.
- `commit`: Boolean. When set to `True`, a commit statement will be sent to the database immediately after each query execution. default to `False`.
- `exit_on_error`: Boolean. If set to `True`, any error encountered while query execution will raise an error and exit the script after query rollback. Default to `True`.

In conformance to [*Python Database API v2.0*](https://peps.python.org/pep-0249), parameters may be provided as sequence or mapping and will be bound to variables in the operation. If error occurs while query execution, the query will be *rollbacked*.

This method is intended to insert data or update the database. It is not intended to retrieve data.

The query format depends on the database type. See the [query formatting section](#query-formatting) below for further details.

For security reasons, **never** try to manage the interpolation of parameters inside the query yourself.


#### Transactions

Transactions can be performed withe the `Database.transaction()` method, which accpets the following parmeters:
- `queries`: A list of dictionaries specifying all queries and needed parameters to be executed within the transaction. The SQL query to execute. The string query should use the `named paramstyle` (see https://peps.python.org/pep-0249/#paramstyle) for parameters mapping.
- `verbose`: Boolean. If set to `True`, each query, parameter and result will be sent to the logger.
- `exit_on_error`: Boolean. If set to `True`, any error encountered while query execution will raise an error and exit the script after query rollback. Default to `False`.

The whole transaction is committed only if all queries specified in the `queries` argument are executed without error. If an error occurs within the transaction, the whole transaction is *rollbacked*.

This method is intended to insert data or update the database. It is not intended to retrieve data.

Each dictionary in the `queries` list must provide at least a `query` item specifying a query to execute. It may also provide a `params` item which is a dictionary of parameters to be mapped onto the corresponding `query` string (see the `query()` method for further details).

The query format depends on the database type. See the [query formatting section](#query-formatting) below for further details.


#### Query formatting

In order to prevent SQL injection, SQL queries must use placeholders for data binding.

While the principe is the same amongst the different supported database types, the placeholder formats vary.

##### *Postgres* and *MySQL*

Placeholders are identified by `%(placeholder)s`. The name of the placeholders can then be utilized to transmit data to the query through a dictionary with keys matching the query parameter names.

Exemples:

  ```python
  query = "INSERT INTO people VALUES(%(firstname)s, %(lastname)s, %(age)s)"
  data = {"firstname": "Luiggi", "lastname": "Vercotti", "age": 42}
  ```

  ```python
  query = "select * from people where age = %(age)s"
  data = {"age": 42}
  ```

##### *sqlite3* and *Oracle*

Placeholders are identified by a colon followed by the name of the placeholder. The name of the placeholders can then be utilized to transmit data to the query through a dictionary with keys matching the query parameter names.

Exemples:

  ```python
  query = "INSERT INTO people VALUES(:firstname, :lastname, :age)"
  data = {"firstname": "Luiggi", "lastname": "Vercotti", "age": 42}
  ```

  ```python
  query = "select * from people where age = :age"
  data = {"age": 42}
  ```

#### Examples


```python
from scrippy_db import ScrippyDbError, logger
from scrippy_db.db import Database

# Simple query
with Database(db_type="pgsql", username="luiggi.vercotti", password="D3ADP4ARR0T",
              host="db.flying.circus", port="5432", database="monty_python") as db:
  query = "INSERT INTO people VALUES(:firstname, :lastname, :age)"
  data = {"firstname": "Harry", "lastname": "Fink", "age": 42}
  db.query(query=query, params=data, commit=True, exit_on_error=True)

with Database(db_type="pgsql", username="luiggi.vercotti", password="D3ADP4ARR0T",
              host="db.flying.circus", port="5432", database="monty_python") as db:
  query = "select * from people where age = :age"
  data = {"firstname": "Harry", "lastname": "Fink", "age": 42}
  rows = db.query(query=query, params=data, commit=True, exit_on_error=True)
  for firstname, lastname, age in rows:
    logger.info(f"{firstname} {lastname} is {age} years old")

# Multiple queries
with Database(db_type="pgsql", username="luiggi.vercotti", password="d34dP4rr0t",
              host="db.flying.circus", port="5432", database="monty_python") as db:
  query = "INSERT INTO people VALUES(:firstname, :lastname, :age)"
  data = [{"firstname": "Harry", "lastname": "Fink", "age": 42},
          {"firstname": "Eric", "lastname": "Parline", "age": 50},
          {"firstname": None, "lastname": "Gumby", "age": 36}]
  db.multi_query(query=query, params=data, commit=True,
                 exit_on_error=True, verbose=True)

# transaction
with Database(db_type="pgsql", username="luiggi.vercotti", password="d34dP4rr0t",
              host="db.flying.circus", port="5432", database="monty_python") as db:
  queries = [{"query": "INSERT INTO people VALUES(:firstname, :lastname, :age)",
              "params": {"firstname": "Harry", "lastname": "Fink", "age": 42}},
             {"query": "delete from people where age > :age", "params": 30}]
  db.transaction(queries=queries, exit_on_error=True)
```


