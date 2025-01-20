

def snake_to_pascal_case(value):
    """将下划线命名 (snake_case) 转换为驼峰命名 (PascalCase)"""
    return ''.join(word.capitalize() for word in value.split('_'))


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def snake_2_colon(snake_str: str) -> str:
    return snake_str.replace('_', ':')