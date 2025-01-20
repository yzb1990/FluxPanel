import os
from jinja2 import Environment, FileSystemLoader

from config.env import DataBaseConfig
from module_generator.utils.database_utils import get_table_structure, get_columns_imports
from module_generator.utils.tools import snake_to_pascal_case, snake_to_camel, snake_2_colon

# 配置模板路径
TEMPLATES_DIR = os.path.abspath(os.path.join(os.getcwd(), 'module_generator/templates'))
OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), 'output'))

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
env.filters['snake_to_pascal_case'] = snake_to_pascal_case
env.filters['snake_to_camel'] = snake_to_camel
env.filters['snake_2_colon'] = snake_2_colon


# 数据库配置
DB_CONFIG = {
    "host": DataBaseConfig.db_host,
    "port": DataBaseConfig.db_port,
    "user": DataBaseConfig.db_username,
    "password": DataBaseConfig.db_password,
    "database": DataBaseConfig.db_database,
    "charset": "utf8mb4",
}

def __render_model(table_name, columns, module_name):
    """生成 SQLAlchemy Model"""
    template = env.get_template("model_template.jinja")
    columns_imports = get_columns_imports(columns)
    rendered_model = template.render(
        table_name=table_name,
        columns=columns,
        columns_imports=columns_imports,
    )
    output_file = f"{OUTPUT_DIR}/{module_name}/entity/do/{table_name}_do.py"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_model)
    print(f"Model generated: {output_file}")


def __render_service(table_name, columns, module_name):
    """生成 SQLAlchemy Service"""
    template = env.get_template("service_template.jinja")
    columns_imports = get_columns_imports(columns)
    rendered_model = template.render(
        table_name=table_name,
        columns=columns,
        columns_imports=columns_imports,
        module_name=module_name,
    )
    output_file = f"{OUTPUT_DIR}/{module_name}/service/{table_name}_service.py"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_model)
    print(f"Service generated: {output_file}")

def __render_controller(table_name, columns, module_name):
    """生成 SQLAlchemy Controller"""
    template = env.get_template("controller_template.jinja")
    columns_imports = get_columns_imports(columns)
    rendered_model = template.render(
        table_name=table_name,
        columns=columns,
        columns_imports=columns_imports,
        module_name=module_name,
    )
    output_file = f"{OUTPUT_DIR}/{module_name}/controller/{table_name}_controller.py"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_model)
    print(f"Controller generated: {output_file}")

def __render_dao(table_name, columns, module_name):
    """生成 SQLAlchemy Model"""
    template = env.get_template("dao_template.jinja")
    columns_imports = get_columns_imports(columns)
    rendered_curd = template.render(
        table_name=table_name,
        columns=columns,
        columns_imports=columns_imports,
        module_name=module_name,
    )
    output_file = f"{OUTPUT_DIR}/{module_name}/dao/{table_name}_dao.py"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_curd)
    print(f"Crud generated: {output_file}")


def __render_vo_model(table_name, columns, module_name):
    """生成 SQLAlchemy Model"""
    template = env.get_template("vo_model_template.jinja")
    columns_imports = get_columns_imports(columns)
    rendered_curd = template.render(
        table_name=table_name,
        columns=columns,
        columns_imports=columns_imports,
        module_name=module_name,
    )
    output_file = f"{OUTPUT_DIR}/{module_name}/entity/vo/{table_name}_vo.py"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered_curd)
    print(f"Crud generated: {output_file}")
    pass


def render_all(table_name, module_name):
    columns = get_table_structure(table_name, DB_CONFIG)
    __render_model(table_name, columns, module_name)
    __render_service(table_name, columns, module_name)
    __render_dao(table_name, columns, module_name)
    __render_controller(table_name, columns, module_name)
    __render_vo_model(table_name, columns, module_name)


if __name__ == "__main__":
    t_name = "user"  # 指定表名
    m_name = "module_admin"
    c_list = get_table_structure(t_name, DB_CONFIG)
    __render_model(t_name, c_list, m_name)
