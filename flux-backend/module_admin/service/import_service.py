import os
import time
from datetime import datetime
from pathlib import Path

import oss2
from Crypto.SelfTest.Cipher.test_OFB import file_name
from fastapi import BackgroundTasks, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.testing import not_in

from config.env import UploadConfig, OSSConfig
from exceptions.exception import ServiceException
from module_admin.dao.import_dao import ImportDao
from module_admin.entity.vo.common_vo import CrudResponseModel, UploadResponseModel
from module_admin.service.common_service import CommonService
from module_gen.constants.gen_constants import GenConstants
from utils.upload_util import UploadUtil
import pandas as pd


class ImportService:
    """
    解析Excel和数据表的Columns
    """

    @classmethod
    async def analysis_excel(cls, query_db: AsyncSession, table_name: str, file: UploadFile = File(...)):
        upload_result = await CommonService.upload_local(file)
        table_columns = await ImportDao.select_table_columns_by_name(query_db, table_name)
        excel_columns = pd.read_excel(upload_result.result.file_name, sheet_name=0, engine="openpyxl").columns

        edit_columns = [col for col in table_columns if col.column_name not in GenConstants.COLUMN_NAME_NOT_EDIT]
        result = {
            "excelColumns": list(excel_columns),
            "tableColumns": edit_columns,
        }
        return result
