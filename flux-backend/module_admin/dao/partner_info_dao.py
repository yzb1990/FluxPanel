# -*- coding:utf-8 -*-

from typing import List
from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.partner_info_do import PartnerInfo
from module_admin.entity.vo.partner_info_vo import PartnerInfoPageModel, PartnerInfoModel
from utils.page_util import PageUtil, PageResponseModel


class PartnerInfoDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, partner_info_id: int) -> PartnerInfo:
        """根据主键获取单条记录"""
        partner_info = (((await db.execute(
                            select(PartnerInfo)
                            .where(PartnerInfo.id == partner_info_id)))
                       .scalars())
                       .first())
        return partner_info

    """
    查询
    """
    @classmethod
    async def get_partner_info_list(cls, db: AsyncSession,
                             query_object: PartnerInfoPageModel,
                             data_scope_sql: str = None,
                             is_page: bool = False) -> [list | PageResponseModel]:

        query = (
            select(PartnerInfo)
            .where(
                PartnerInfo.partner_name == query_object.partner_name if query_object.partner_name else True,
                PartnerInfo.del_flag == '0',
                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(desc(PartnerInfo.create_time))
            .distinct()
        )
        partner_info_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return partner_info_list


    @classmethod
    async def add_partner_info(cls, db: AsyncSession, add_model: PartnerInfoModel, auto_commit: bool = True) -> PartnerInfo:
        """
        增加
        """
        partner_info =  PartnerInfo(**add_model.model_dump(exclude_unset=True))
        db.add(partner_info)
        await db.flush()
        if auto_commit:
            await db.commit()
        return partner_info

    @classmethod
    async def edit_partner_info(cls, db: AsyncSession, edit_model: PartnerInfoModel, auto_commit: bool = True) -> PartnerInfo:
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(PartnerInfo), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return await cls.get_by_id(db, edit_model.id)

    @classmethod
    async def del_partner_info(cls, db: AsyncSession, partner_info_ids: List[str], soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(PartnerInfo).where(PartnerInfo.id.in_(partner_info_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(PartnerInfo).where(PartnerInfo.id.in_(partner_info_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()