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

from module_admin.entity.vo.car_seller_vo import CarSellerPageModel, CarSellerModel
from module_admin.service.car_seller_service import CarSellerService

carSellerController = APIRouter(prefix='/car/seller', dependencies=[Depends(LoginService.get_current_user)])


@carSellerController.get('/list', dependencies=[Depends(CheckUserInterfaceAuth('car:seller:list'))])
async def get_car_seller_list(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        page_query: CarSellerPageModel = Depends( CarSellerPageModel.as_query),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    car_seller_result = await CarSellerService.get_car_seller_list(query_db, page_query, data_scope_sql)

    return ResponseUtil.success(model_content=car_seller_result)

@carSellerController.get('/getById/{carSellerId}', dependencies=[Depends(CheckUserInterfaceAuth('car:seller:list'))])
async def get_car_seller_by_id(
        request: Request,
        carSellerId: int,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    car_seller = await CarSellerService.get_car_seller_by_id(query_db, carSellerId)
    return ResponseUtil.success(data=car_seller)


@carSellerController.post('/add', dependencies=[Depends(CheckUserInterfaceAuth('car:seller:add'))])
@Log(title='car_seller', business_type=BusinessType.INSERT)
async def add_car_seller (
    request: Request,
    add_model: CarSellerModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await CarSellerService.add_car_seller(query_db, add_model)
    return ResponseUtil.success(data=add_dict_type_result)

@carSellerController.put('/update', dependencies=[Depends(CheckUserInterfaceAuth('car:seller:update'))])
@Log(title='car_seller', business_type=BusinessType.UPDATE)
async def update_car_seller(
    request: Request,
    edit_model: CarSellerModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_dict_type_result = await CarSellerService.update_car_seller(query_db, edit_model)
    return ResponseUtil.success(data=add_dict_type_result)


@carSellerController.delete('/delete/{carSellerIds}', dependencies=[Depends(CheckUserInterfaceAuth('car:seller:del'))])
@Log(title='car_seller', business_type=BusinessType.DELETE)
async def del_car_seller(
    request: Request,
    carSellerIds: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    ids = carSellerIds.split(',')
    del_result = await CarSellerService.del_car_seller(query_db, ids)
    return ResponseUtil.success(data=del_result)

@carSellerController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('car:seller:export'))])
@Log(title='car_seller', business_type=BusinessType.EXPORT)
async def export_car_seller(
    request: Request,
    car_seller_form: CarSellerPageModel = Form(),
    query_db: AsyncSession = Depends(get_db),
    data_scope_sql: str = Depends(GetDataScope('SysDept')),
):
    # 获取全量数据
    export_result = await CarSellerService.export_car_seller_list(
        query_db, car_seller_form, data_scope_sql
    )
    return ResponseUtil.streaming(data=bytes2file_response(export_result))