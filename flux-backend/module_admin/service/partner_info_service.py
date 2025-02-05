# -*- coding:utf-8 -*-

from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.common_util import CamelCaseUtil, export_list2excel
from utils.page_util import PageResponseModel
from module_admin.dao.partner_info_dao import PartnerInfoDao
from module_admin.entity.do.partner_info_do import PartnerInfo
from module_admin.entity.vo.partner_info_vo import PartnerInfoPageModel, PartnerInfoModel


class PartnerInfoService:
    """
    用户管理模块服务层
    """

    @classmethod
    async def get_partner_info_list(cls, query_db: AsyncSession, query_object: PartnerInfoPageModel, data_scope_sql: str) -> [list | PageResponseModel]:
        partner_info_list = await PartnerInfoDao.get_partner_info_list(query_db, query_object, data_scope_sql, is_page=True)
        return partner_info_list

    @classmethod
    async def get_partner_info_by_id(cls, query_db: AsyncSession, partner_info_id: int) -> PartnerInfoModel:
        partner_info = await  PartnerInfoDao.get_by_id(query_db, partner_info_id)
        partner_info_model = PartnerInfoModel(**CamelCaseUtil.transform_result(partner_info))
        return partner_info_model


    @classmethod
    async def add_partner_info(cls, query_db: AsyncSession, query_object: PartnerInfoModel) -> PartnerInfoModel:
        partner_info = await PartnerInfoDao.add_partner_info(query_db, query_object)
        partner_info_model = PartnerInfoModel(**CamelCaseUtil.transform_result(partner_info))
        return partner_info_model


    @classmethod
    async def update_partner_info(cls, query_db: AsyncSession, query_object: PartnerInfoModel) -> PartnerInfoModel:
        partner_info = await PartnerInfoDao.edit_partner_info(query_db, query_object)
        partner_info_model = PartnerInfoModel(**CamelCaseUtil.transform_result(partner_info))
        return partner_info_model


    @classmethod
    async def del_partner_info(cls, query_db: AsyncSession, partner_info_ids: List[str]):
        await PartnerInfoDao.del_partner_info(query_db, partner_info_ids)


    @classmethod
    async def export_partner_info_list(cls, query_db: AsyncSession, query_object: PartnerInfoPageModel, data_scope_sql) -> bytes:
        partner_info_list = await PartnerInfoDao.get_partner_info_list(query_db, query_object, data_scope_sql, is_page=False)
        mapping_dict = {
            'description': '资料介绍 ',
            'image': '图片 ',
            'lat': '纬度 ',
            'lng': '经度 ',
            'location': '所在位置 ',
            'partnerName': '合作方名称 ',
            'price': '价格 ',
        }
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in partner_info_list
        ]
        binary_data = export_list2excel(new_data)
        return binary_data