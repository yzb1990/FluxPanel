# -*- coding:utf-8 -*-

from datetime import datetime, time
from sqlalchemy import and_, delete, desc, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.page_info_do import PageInfo
from module_admin.entity.vo.page_info_vo import PageInfoPageModel, PageInfoModel
from utils.page_util import PageUtil


class PageInfoDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, page_info_id: int) -> PageInfo:
        """根据主键获取单条记录"""
        page_info = (((await db.execute(
                            select(PageInfo)
                            .where(PageInfo.id == page_info_id)))
                       .scalars())
                       .first())
        return page_info

    @classmethod
    async def get_by_name(cls, db: AsyncSession, page_name: str) -> PageInfo:
        """根据主键获取单条记录"""
        page_info = (((await db.execute(
            select(PageInfo)
            .where(PageInfo.page_name == page_name)))
                      .scalars())
                     .first())
        return page_info

    """
    查询
    """
    @classmethod
    async def get_page_info_list(cls, db: AsyncSession,
                             query_object: PageInfoPageModel,
                             data_scope_sql: str,
                             is_page: bool = False) -> list[PageInfo]:

        query = (
            select(PageInfo)
            .where(
                

                PageInfo.description.like(f"%{query_object.description}%") if query_object.description else True,

                PageInfo.id == query_object.id if query_object.id else True,
                
                PageInfo.keywords.like(f"%{query_object.keywords}%") if query_object.keywords else True,
                
                PageInfo.news_category_id == query_object.news_category_id if query_object.news_category_id else True,
                
                PageInfo.page_alias.like(f"%{query_object.page_alias}%") if query_object.page_alias else True,
                
                PageInfo.page_name.like(f"%{query_object.page_name}%") if query_object.page_name else True,
                
                PageInfo.product_keywords.like(f"%{query_object.product_keywords}%") if query_object.product_keywords else True,
                
                PageInfo.title.like(f"%{query_object.title}%") if query_object.title else True,

                PageInfo.del_flag == '0',
                
                eval(data_scope_sql),
            )
            .order_by(desc(PageInfo.create_time))
            .distinct()
        )
        page_info_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return page_info_list


    @classmethod
    async def add_page_info(cls, db: AsyncSession, add_model: PageInfoModel) -> PageInfo:
        """
        增加
        """
        page_info =  PageInfo(**add_model.model_dump(exclude_unset=True))
        db.add(page_info)
        await db.flush()
        return page_info

    @classmethod
    async def edit_page_info(cls, db: AsyncSession, edit_model: PageInfoModel, auto_commit: bool = True):
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(PageInfo), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return edit_model

    @classmethod
    async def del_page_info(cls, db: AsyncSession, del_model: PageInfoModel, soft_del: bool = True, auto_commit: bool = True):
        """
        删除
        """
        if soft_del:
            await db.execute(update(PageInfo).where(PageInfo.id == del_model.id).values(del_flag='2'))
        else:
            await db.execute(delete(PageInfo).where(PageInfo.id == del_model.id))
        await db.flush()
        if auto_commit:
            await db.commit()