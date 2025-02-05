# -*- coding:utf-8 -*-

from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from typing import List
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.service.login_service import LoginService
from module_admin.aspect.data_scope import GetDataScope
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.annotation.log_annotation import Log
from utils.response_util import ResponseUtil
from utils.common_util import bytes2file_response

from module_admin.entity.vo.partner_info_vo import PartnerInfoPageModel, PartnerInfoModel
from module_admin.service.partner_info_service import PartnerInfoService

partnerInfoController = APIRouter(prefix='/partner/info', dependencies=[Depends(LoginService.get_current_user)])


@partnerInfoController.get('/list', dependencies=[Depends(CheckUserInterfaceAuth('partner:info:list'))])
async def get_partner_info_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        page_query: PartnerInfoPageModel = Depends( PartnerInfoPageModel.as_query),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    partner_info_result = await PartnerInfoService.get_partner_info_list(query_db, page_query, data_scope_sql)

    return ResponseUtil.success(model_content=partner_info_result)

@partnerInfoController.get('/getById/{partnerInfoId}', dependencies=[Depends(CheckUserInterfaceAuth('partner:info:list'))])
async def get_partner_info_by_id(
        request: Request,
        partnerInfoId: int,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    partner_info = await PartnerInfoService.get_partner_info_by_id(query_db, partnerInfoId)
    return ResponseUtil.success(data=partner_info)


@partnerInfoController.post('/add', dependencies=[Depends(CheckUserInterfaceAuth('partner:info:add'))])
@Log(title='partner_info', business_type=BusinessType.INSERT)
async def add_partner_info (
    request: Request,
    add_model: PartnerInfoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await PartnerInfoService.add_partner_info(query_db, add_model)
    return ResponseUtil.success(data=add_dict_type_result)

@partnerInfoController.put('/update', dependencies=[Depends(CheckUserInterfaceAuth('partner:info:update'))])
@Log(title='partner_info', business_type=BusinessType.UPDATE)
async def update_partner_info(
    request: Request,
    edit_model: PartnerInfoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await PartnerInfoService.update_partner_info(query_db, edit_model)
    return ResponseUtil.success(data=add_dict_type_result)


@partnerInfoController.delete('/delete/{partnerInfoIds}', dependencies=[Depends(CheckUserInterfaceAuth('partner:info:del'))])
@Log(title='partner_info', business_type=BusinessType.DELETE)
async def del_partner_info(
    request: Request,
    partnerInfoIds: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    ids = partnerInfoIds.split(',')
    del_result = await PartnerInfoService.del_partner_info(query_db, ids)
    return ResponseUtil.success(data=del_result)

@partnerInfoController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('partner:info:export'))])
@Log(title='partner_info', business_type=BusinessType.EXPORT)
async def export_partner_info(
    request: Request,
    partner_info_form: PartnerInfoPageModel = Form(),
    query_db: AsyncSession = Depends(get_db),
    data_scope_sql: str = Depends(GetDataScope('SysDept')),
):
    # 获取全量数据
    export_result = await PartnerInfoService.export_partner_info_list(
        query_db, partner_info_form, data_scope_sql
    )
    return ResponseUtil.streaming(data=bytes2file_response(export_result))