import pymysql
from pymysql.cursors import DictCursor

# MySQL -> SQLAlchemy 类型映射
MYSQL_TO_SQLALCHEMY = {
    "int": "Integer",
    "tinyint": "Boolean",
    "bigint": "BigInteger",
    "varchar": "String",
    "text": "Text",
    "date": "Date",
    "datetime": "DateTime",
    "timestamp": "DateTime",
    "decimal": "Numeric",
    "float": "Float",
    "double": "Float",
    "char": "String",
}

MYSQL_TO_PYTHON = {
        "VARCHAR": "str",
        "CHAR": "str",
        "LONGTEXT": "str",
        "TEXT": "str",
        "INT": "int",
        "TINYINT": "int",
        "BIGINT": "int",
        "FLOAT": "float",
        "DOUBLE": "float",
        "DECIMAL": "float",
        "DATETIME": "datetime",
        "DATE": "datetime.date",
        "TIME": "datetime.time",
        "TIMESTAMP": "datetime",
        "BOOLEAN": "bool",
        "JSON": "dict",
    }

def parse_mysql_type(mysql_type):
    """解析 MySQL 字段类型并映射到 SQLAlchemy"""
    mysql_type = mysql_type.lower()
    if "(" in mysql_type:  # 处理带参数的类型，如 VARCHAR(255)
        base_type, args = mysql_type.split("(", 1)
        args = args.strip(")").split(",")
        if base_type in MYSQL_TO_SQLALCHEMY:
            sqlalchemy_type = MYSQL_TO_SQLALCHEMY[base_type]
            if args:  # 处理类型参数，如 String(255)
                if base_type in ["varchar", "char"]:
                    return f"{sqlalchemy_type}(length={args[0]})"
                elif base_type == "decimal":
                    return f"{sqlalchemy_type}(precision={args[0]}, scale={args[1]})"
            return sqlalchemy_type
    else:  # 处理无参数的类型
        return MYSQL_TO_SQLALCHEMY.get(mysql_type, "String")  # 默认 String 类型


def parse_mysql_2_python_type(mysql_type):
    """
    将 MySQL 数据类型映射到 Python 类型
    """
    base_type = mysql_type.split("(")[0].upper()
    return MYSQL_TO_PYTHON.get(base_type, "Any")


def get_table_structure(table_name, db_config):
    """
    获取表结构，包括字段名、类型、是否主键、是否允许为空、默认值、索引、唯一约束、自增和外键信息
    """
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # 查询表的字段信息
    column_query = f"""
        SELECT 
            COLUMN_NAME as name,
            COLUMN_TYPE as type,
            IS_NULLABLE as nullable,
            COLUMN_DEFAULT as col_default,
            COLUMN_KEY as key_name,
            EXTRA as extra,
            COLUMN_COMMENT as comment
        FROM 
            information_schema.COLUMNS
        WHERE 
            TABLE_SCHEMA = '{db_config['database']}'
            AND TABLE_NAME = '{table_name}'
    """
    cursor.execute(column_query)
    columns = cursor.fetchall()

    # 查询外键约束信息
    fk_query = f"""
        SELECT 
            COLUMN_NAME,
            REFERENCED_TABLE_NAME,
            REFERENCED_COLUMN_NAME
        FROM 
            information_schema.KEY_COLUMN_USAGE
        WHERE 
            TABLE_SCHEMA = '{db_config['database']}'
            AND TABLE_NAME = '{table_name}'
            AND REFERENCED_TABLE_NAME IS NOT NULL
    """
    cursor.execute(fk_query)
    foreign_keys = cursor.fetchall()
    conn.close()

    # 将外键信息整理为字典，方便查找
    fk_dict = {
        fk['COLUMN_NAME']: (fk['REFERENCED_TABLE_NAME'], fk['REFERENCED_COLUMN_NAME'])
        for fk in foreign_keys
    }

    # 解析字段信息
    column_info = []
    for col in columns:
        sqlalchemy_type = parse_mysql_type(col['type'])
        python_type = parse_mysql_2_python_type(col['type'])
        mysql_type = col['type'].split('(')[0].upper()
        is_base_column = col['name'] in ('id', 'create_time', 'update_time', 'del_flag')

        options = []

        # 外键
        if col['name'] in fk_dict:
            ref_table, ref_column = fk_dict[col['name']]
            options.append(f"ForeignKey('{ref_table}.{ref_column}')")
        # 主键
        if col['key_name'] == "PRI":
            options.append("primary_key=True")
        # 唯一约束
        if col['key_name'] == "UNI":
            options.append("unique=True")
        # 索引（普通索引）
        if col['key_name'] == "MUL":
            options.append("index=True")
        # 是否允许为空
        if col['nullable'] == "NO":
            options.append("nullable=False")
        # 默认值
        if col['col_default'] is not None:
            options.append(f"default={repr(col['col_default'])}")
        # 自增
        if "auto_increment" in col['extra']:
            options.append("autoincrement=True")
        # 注释
        if col['comment'] is not None:
            options.append(f"comment='{col['comment']}'")



        column_info.append({
            "name": col['name'],
            "type": sqlalchemy_type,
            "python_type": python_type,
            "mysql_type": mysql_type,
            "options": ", ".join(options),
            "comment": col['comment'] or "",
            "is_base_column": is_base_column,
        })
    return column_info



def get_columns_imports(columns):
    """根据表结构的字段类型生成需要导入的 SQLAlchemy 类型"""
    imports = set()
    for column in columns:
        column_type = column['type'].split('(')[0]  # 提取字段类型的基类名
        imports.add(column_type)
    return ", ".join(sorted(imports))  # 去重并排序，便于阅读
