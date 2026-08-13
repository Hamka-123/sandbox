CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS {table_name} (
    {params}
    );                  
"""

DELETE_TABLE = """
    DROP TABLE IF EXISTS {table_name};
"""

EDIT_TABLE_ADD_COLUMN = """
    ALTER TABLE {table_name} ADD {column} {data_type};
"""

EDIT_TABLE_DELETE_COLUMN = """
    ALTER TABLE {table_name} DROP COLUMN {column};
"""

EDIT_TABLE_CHANGE_COLUMN_TYPE = """
    ALTER TABLE {table_name} MODIFY {column} {new_data_type};
"""

SELECT_ALL = """
    SELECT * FROM {table_name};
"""

SELECT_ONE_BY_COLUMN = """
    SELECT * FROM {table_name} WHERE {column} = ?;
"""

ADD_ONE = """
    INSERT INTO {table_name} ({columns})
    VALUES ({values});
"""

UPDATE_ONE = """
    UPDATE {table_name}
    SET {set_clause}
    WHERE id = {user_id};
"""

DELETE_ONE = """
    DELETE FROM {table_name}
    WHERE id = {user_id};
"""
