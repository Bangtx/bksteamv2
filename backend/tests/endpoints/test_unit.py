from schemas.master import unit as unit_schemas
from typing import List

db_test_create_unit = """
    INSERT INTO public.unit_group(code, id, name, yomi, name_short, name_eng, order_num) 
    VALUES 
        (1, 1, 'group test', 'grouptest', 'group test', null, null);
    INSERT INTO public.unit(code, gid, name, yomi, name_short, name_eng, untg_id) 
    VALUES 
        (1, null, 'unit test', 'unit test', 'unit test', null, 1);
    """
db_test_update_unit = """
    INSERT INTO public.unit_group(code, id, name, yomi, name_short, name_eng, order_num) 
    VALUES 
        (1, 1, 'group test', 'grouptest', 'group test', null, null);
    INSERT INTO public.unit(code, gid, name, yomi, name_short, name_eng, untg_id) 
    VALUES 
        (1, null, 'unit test', 'unit test', 'unit test', null, 1);
    """
db_test_get_unit = """
    INSERT INTO public.unit_group(code, id, name, yomi, name_short, name_eng, order_num, search_str) 
    VALUES 
        (1, 1, 'group test', 'grouptest', 'group test', null, null, 'group test|grouptest'),
        (2, 2, 'group test 2', 'grouptest2', 'group test 2', null, null, 'group test 2|grouptest2');
    INSERT INTO public.unit(code, gid, name, yomi, name_short, name_eng, untg_id, search_str) 
    VALUES 
        (1, null, 'unit test', 'unit test', 'unit test', null, 1, 'unit test|unit test'),
        (2, null, 'unit test 2', 'unit test 2', 'unit test 2', null, 1, 'unit test 2|unit test 2'),
        (3, null, 'unit test 3', 'unit test 3', 'unit test 3', null, 2, 'unit test 3|unit test 3');
    """
db_test_sort_unit = """
    INSERT INTO public.unit_group(code, id, name, yomi, name_short, name_eng, search_str, order_num) 
    VALUES 
        (1, 1, 'group test', 'grouptest', 'group test', null, 'group test|grouptest', 1),
        (2, 2, 'group test 2', 'grouptest2', 'group test 2', null, 'group test 2|grouptest2', 2);
    INSERT INTO public.unit(code, gid, name, yomi, name_short, name_eng, untg_id, search_str, order_num) 
    VALUES 
        (1, null, 'unit test', 'unit test', 'unit test', null, 1, 'unit test|unit test', 1),
        (2, null, 'unit test 2', 'unit test 2', 'unit test 2', null, 1, 'unit test 2|unit test 2', null),
        (3, null, 'unit test 3', 'unit test 3', 'unit test 3', null, 2, 'unit test 3|unit test 3', null);
    """
# TEST CREATE UNIT
def test_create_normal_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": None,
        "name": "unit test 2",
        "yomi": "unit test 2",
        "name_short": "unit test 2",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.post(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    data = response.json()
    design_output: unit_schemas.Unit = {
        "code": None,
        "name": "unit test 2",
        "yomi": "unit test 2",
        "name_short": "unit test 2",
        "name_eng": None,
        "order_num": None,
        "id": 2,
        "untg": {
            "code": 1,
            "name": "group test",
            "yomi": "grouptest",
            "name_short": "group test",
            "name_eng": None,
            "order_num": None,
            "id": 1
        }
    }
    assert response.status_code == 200 and data == design_output


def test_create_null_name_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": None,
        "name": None,
        "yomi": "unit test 2",
        "name_short": "unit test 2",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.post(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    assert response.status_code == 422


def test_create_null_name_short_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": None,
        "name": "unit test 2",
        "yomi": "unit test 2",
        "name_short": None,
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.post(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    assert response.status_code == 422


def test_create_null_yomi_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": None,
        "name": "unit test 2",
        "yomi": None,
        "name_short": "unit test 2",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.post(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    assert response.status_code == 422


def test_create_duplicated_name_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": None,
        "name": "unit test",
        "yomi": "unit test",
        "name_short": "unit test",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.post(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    data = response.json()
    design_output = {
      "detail": {
        "error_code": "duplicate_name"
      }
    }
    assert response.status_code == 400 and data == design_output


def test_create_duplicated_code_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": 1,
        "name": "unit test 2",
        "yomi": "unit test 2",
        "name_short": "unit test 2",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.post(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    data = response.json()
    design_output = {
        "detail": {
            "error_code": "duplicate_code"
        }
    }
    assert response.status_code == 400 and data == design_output


def test_create_duplicated_name_short_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": None,
        "name": "unit test 2",
        "yomi": "unit test 2",
        "name_short": "unit test",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.post(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    data = response.json()
    design_output = {
        "detail": {
            "error_code": "duplicate_name_short"
        }
    }
    assert response.status_code == 400 and data == design_output


def test_create_duplicated_is_true_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": 1,
        "name": "unit test",
        "yomi": "unit test",
        "name_short": "unit test",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.post(
        "/master/unit/?is_duplicate=true",
        json=payload
    )
    assert response.status_code == 200


def test_create_null_group_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitCreate = {
        "code": None,
        "name": "unit test 2",
        "yomi": "unit test 2",
        "name_short": "unit test 2",
        "name_eng": None,
        "order_num": None,
        "untg": None
    }
    response = client.post(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    assert response.status_code == 422


# TEST UPDATE UNIT
def test_update_normal_unit(db, client):
    db.execute_sql(db_test_update_unit)
    payload: unit_schemas.UnitUpdate = {
        "id": 1,
        "code": 2,
        "name": "unit test 3",
        "yomi": "unit test 3",
        "name_short": "unit test 3",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.put(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    data = response.json()
    design_output: unit_schemas.Unit = {
        "id": 1,
        "code": 2,
        "name": "unit test 3",
        "yomi": "unit test 3",
        "name_short": "unit test 3",
        "name_eng": None,
        "order_num": None,
        "untg": {
            "code": 1,
            "name": "group test",
            "yomi": "grouptest",
            "name_short": "group test",
            "name_eng": None,
            "order_num": None,
            "id": 1
        }
    }
    assert response.status_code == 200 and data == design_output


def test_update_duplicated_unit(db, client):
    db.execute_sql(db_test_create_unit)
    payload: unit_schemas.UnitUpdate = {
        "code": 1,
        "name": "unit test 2",
        "yomi": "unit test 2",
        "name_short": "unit test 2",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.put(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    assert response.status_code == 422
    payload: unit_schemas.UnitUpdate = {
        "code": 1,
        "name": "unit test",
        "yomi": "unit test",
        "name_short": "unit test 2",
        "name_eng": None,
        "order_num": None,
        "untg": 1
    }
    response = client.put(
        "/master/unit/?is_duplicate=false",
        json=payload
    )
    assert response.status_code == 422


# TEST GET UNITS
def test_get_unit_without_search_string(db, client):
    db.execute_sql(db_test_get_unit)
    query = f"?untg={1}"
    response = client.get(
        f"/master/unit/{query}"
    )
    data = response.json()
    assert response.status_code == 200 and len(data) == 2
    query = f"?untg={2}"
    response = client.get(
        f"/master/unit/{query}"
    )
    data = response.json()
    assert response.status_code == 200 and len(data) == 1
    query = f""
    response = client.get(
        f"/master/unit/{query}"
    )
    data = response.json()
    assert response.status_code == 200 and len(data) == 3


def test_get_unit_with_search_string(db, client):
    db.execute_sql(db_test_get_unit)
    query = f"?untg={1}&search_input=2"
    response = client.get(
        f"/master/unit/{query}"
    )
    data = response.json()
    assert response.status_code == 200 and len(data) == 1 and data[0]['name'] == 'unit test 2'


# TEST SORT UNIT
def test_sort_normal_unit(db, client):
    db.execute_sql(db_test_sort_unit)
    response = client.put(
        f"/master/unit/sort",
        json=[
            {
                "id": 1,
                "order_num": 1
            }, {
                "id": 2,
                "order_num": 2
            }
        ]
    )
    assert response.status_code == 200


# TEST DELETE UNIT

def test_delete_normal_unit(db, client):
    db.execute_sql(db_test_create_unit)
    response = client.delete(
        f"/master/unit/{1}"
    )
    assert response.status_code == 200
