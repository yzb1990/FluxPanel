from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Any, List, Optional


class GenTableModel(BaseModel):
    """
    代码生成接口
    """

    model_config = ConfigDict(alias_generator=to_camel)

    table_name: Optional[str] = Field(default=None, description='表名字')
    module_name: Optional[str] = Field(default=None, description='模块名字')


