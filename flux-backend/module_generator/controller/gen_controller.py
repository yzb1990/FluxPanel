from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.data_scope import GetDataScope
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_generator.entity.vo.gen_vo import GenTableModel
from module_generator.utils.generator import render_all
from utils.response_util import ResponseUtil
from utils.log_util import logger

genController = APIRouter(prefix='/gen', dependencies=[Depends(LoginService.get_current_user)])


@genController.get('/list', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:list'))])
async def get_table_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db)
):

    return ResponseUtil.success(data=None)


@genController.post('/gen_code', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:code'))])
async def gen_code(
        request: Request,
        query_model: GenTableModel,
        query_db: AsyncSession = Depends(get_db)
):
    render_all(query_model.table_name, query_model.module_name)
    return ResponseUtil.success(data=None)