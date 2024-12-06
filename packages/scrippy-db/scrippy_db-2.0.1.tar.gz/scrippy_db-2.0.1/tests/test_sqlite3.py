import os
from scrippy_db import ScrippyDbError
from scrippy_db.db import Database


db_base = os.path.join(os.path.dirname(__file__), "files", "scrippydb.db")
db_type = "sqlite3"
good_args_001 = {"database": db_base,
                 "db_type": "sqlite3"}
good_args_002 = {"service": "scrippy",
                 "db_type": "sqlite3"}
bad_args_001 = {"service": "scrippy",
                "username": "scrippy",
                "db_type": "sqlite3"}
base_users = [(1, 'Fink', 'Larry', 'D34dP4rr0t'),
              (2, 'Vercotti', 'Luiggi', '5p4n15h1nqu1s1t10n')]
new_users = [{"givenname": "Reg",
              "name": "Moss",
              "password": "P4bl0P1c4ss0"},
             {"givenname": "Ken",
              "name": "Shabby",
              "password": "RAnc1dP0leC4t"},
             {"givenname": "David",
              "name": "Mitzie",
              "password": "ItsTheArt"}]


def test_query_good_args_001():
  query = "select password from users where name=:name"
  params = {"name": "Vercotti"}
  with Database(db_type=db_type, database=db_base) as database:
    rows = database.query(query=query, params=params)
    assert rows[0][0] == base_users[1][3]


def test_service_good_query():
  query = "select password from users where name=:name"
  params = {"name": "Vercotti"}
  with Database(db_type=db_type, database=db_base) as database:
    rows = database.query(query=query, params=params)
    assert rows[0][0] == base_users[1][3]


def test_service_bad_query():
  query = "select password from user where name=:name"
  params = {"name": "Vercotti"}
  with Database(db_type=db_type, database=db_base) as database:
    try:
      rows = database.query(query=query, params=params)
      raise Exception("[Failed Test] test_service_bad_query")
    except ScrippyDbError as err:
      assert str(err).startswith("[DatabaseQueryError]")


def test_query_with_commit():
  new_user = new_users[0]
  query = "insert into users (name, givenname, password) values (:name, :givenname, :password)"
  with Database(db_type=db_type, database=db_base) as database:
    rows = database.query(query=query,
                          params=new_user,
                          commit=True)
    assert rows is None
    query = "select password from users where name=:name"
    rows = database.query(query=query,
                          params=new_user)
    assert rows[0][0] == new_user.get("password")


def test_multi_querys_with_commit():
  query = "insert into users (name, givenname, password) values (:name, :givenname, :password)"
  with Database(db_type=db_type, database=db_base) as database:
    rows = database.multi_query(query=query,
                                paramlist=new_users[1:],
                                commit=True)
    assert rows is None
    query = "select password from users where id > 2"
    rows = database.query(query=query, params=None)
    expected = [user.get("password") for user in new_users]
    assert expected == [user[0] for user in rows]


def test_query_rollback():
  new_user = {"givename": "Clodagh", "name": "Rodgers", "password": "JackIn TheBox"}
  query = "insert into users (name, givenname, password) values (:name, :givenname, :password)"
  with Database(db_type=db_type, database=db_base) as database:
    try:
      rows = database.query(query=query,
                            params=new_user,
                            commit=True,
                            exit_on_error=True)
      raise ScrippyDbError("Failed test: test_query_rollback")
    except ScrippyDbError as err:
      assert str(err) == "[DatabaseQueryError] An error occurred while querying the database: You did not supply a value for binding parameter :givenname."


def test_multi_query_rollback():
  bad_new_users = [{"givenname": "Harold",
                    "name": "Larch",
                    "password": "fr33d0m"},
                   {"givename": "Arthur",
                    "name": "Wilson",
                    "password": "k1l1m4nj4r0"}]
  query = "insert into users (name, givenname, password) values (:name, :givenname, :password)"
  with Database(db_type=db_type, database=db_base) as database:
    try:
      rows = database.multi_query(query=query,
                                  paramlist=bad_new_users,
                                  commit=True,
                                  exit_on_error=True)
      raise ScrippyDbError("Failed test: test_query_rollback")
    except ScrippyDbError as err:
      assert str(err) == "[DatabaseQueryError] An error occurred while querying the database: You did not supply a value for binding parameter :givenname."
    query = "select password from users where id > 2"
    rows = database.query(query=query, params=None)
    expected = [user.get("password") for user in new_users]
    expected.append(bad_new_users[0].get("password"))
    assert expected == [user[0] for user in rows]


def test_transaction():
  trans_new_users = [{"givenname": "Edward",
                      "name": "Ross",
                      "password": "PussyC4t"},
                     {"givenname": "Ron",
                      "name": "Geppo",
                      "password": "P4bl0Pic4ss0"},
                     {"givenname": "R.j",
                      "name": "Canning",
                      "password": "W0rlD0fH1st0ry"}]
  queries = [{"query": "insert into users (givenname, name, password) values (:givenname, :name, :password)",
              "params": trans_new_users[0]},
             {"query": "insert into users (givenname, name, password) values (:givenname, :name, :password)",
              "params": trans_new_users[1]},
             {"query": "delete from users where name = :name",
              "params": trans_new_users[0]},
             {"query": "delete from users where name = :name",
              "params": trans_new_users[1]}]
  with Database(db_type=db_type, database=db_base) as database:
    rows = database.transaction(queries=queries,
                                exit_on_error=True)
    assert rows is None
    query = "select password from users where id > 2"
    rows = database.query(query=query, params=None)
    expected = [user.get("password") for user in new_users]
    expected.append("fr33d0m")
    assert expected == [user[0] for user in rows]


def test_transaction_rollback():
  trans_new_users = [{"givenname": "Edward",
                      "name": "Ross",
                      "password": "PussyC4t"},
                     {"givenname": "Ron",
                      "name": "Geppo",
                      "password": "P4bl0Pic4ss0"},
                     {"givenname": "R.j",
                      "name": "Canning",
                      "password": "W0rlD0fH1st0ry"}]
  queries = [{"query": "insert into users (givenname, name, password) values (:givenname, :name, :password)",
              "params": trans_new_users[0]},
             {"query": "insert into users (givenname, name, password) values (:givenname, :name, :password)",
              "params": trans_new_users[1]},
             {"query": "insert into users (givenname, name, password) values (:givenname, :name, :password)",
              "params": trans_new_users[2]},
             {"query": "delete from users where name = :name",
              "params": trans_new_users[0]},
             {"query": "delete from users where name = :name",
              "params": trans_new_users[1]},
             {"query": "delet from users where name = :name",
              "params": trans_new_users[1]}]
  with Database(db_type=db_type, database=db_base) as database:
    try:
      rows = database.transaction(queries=queries,
                                  exit_on_error=True)
    except ScrippyDbError as err:
      assert str(err).startswith("[DatabaseQueryError] An error occurred while querying the database")
    query = "select password from users where id > 2"
    rows = database.query(query=query, params=None)
    expected = [user.get("password") for user in new_users]
    expected.append("fr33d0m")
    assert expected == [user[0] for user in rows]


def test_good_args_001():
  users = base_users.copy()
  for user in new_users:
    users.append((len(users) + 1,
                 user["name"],
                 user["givenname"],
                 user["password"]))
  users.append((len(users) + 1,
                "Larch",
                "Harold",
                "fr33d0m"))
  query = "select id, name, givenname, password from users order by id"
  with Database(db_type=db_type, database=db_base) as database:
    rows = database.query(query=query)
    assert rows == users


def test_good_args_002():
  users = base_users.copy()
  for user in new_users:
    users.append((len(users) + 1,
                 user["name"],
                 user["givenname"],
                 user["password"]))
  users.append((len(users) + 1,
                "Larch",
                "Harold",
                "fr33d0m"))
  query = "select id, name, givenname, password from users order by id"
  with Database(db_type=db_type, database=db_base) as database:
    rows = database.query(query=query, verbose=True)
    assert rows == users
