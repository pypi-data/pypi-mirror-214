from enum import Enum
from typing import List, Union, Dict
from pydantic import BaseModel, Field
from ..util import time as time_lib


class TaskType(str, Enum):
    """
    任务类型枚举
    """
    # 商品基础信息
    SKU_INFO = 'sku_info'
    # 商品价格
    SKU_PRICE = 'sku_price'
    # 商品基础信息及价格等详细信息
    SKU_FULL = 'sku_full'
    # 商品主详图
    SKU_IMAGE = 'sku_image'
    # 信息抽取
    SKU_EXTRACT = 'sku_extract'
    # 流式采集商品编码（如编码）
    STREAM_SKU_ID = 'stream_sku_id'
    # 流式采集商品价格信息
    STREAM_SKU_PRICE = 'stream_sku_price'
    # 流式采集商品基础信息及价格等详细信息
    STREAM_SKU_FULL = 'stream_sku_full'
    # 流式采集商品主详图
    STREAM_SKU_IMAGE = 'stream_sku_image'
    # 流式采集同款商品
    STREAM_SKU_SAME = "stream_sku_same"


class BaseData(BaseModel):
    """
    通用基础数据模型
    """
    # 主键
    _id: str = None
    # 插入时间
    genTime: int = Field(
        default_factory=time_lib.current_timestamp10
    )


class TaskItem(BaseData):
    """
    任务物料模型
    """
    # 对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = None
    # 商品链接
    url: str
    # 用户指定编号(采图时需要)
    rowId: str = None
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = None


class ApiData(BaseModel):
    """
    通用数据接收模型
    """
    # 应用编码
    app_code: str
    # 批次编号
    batch_id: str = None
    # 租户编码
    tenant_code: str = None
    # 任务类型
    task_type: TaskType = None
    # 任务明细清单
    task_items: List[TaskItem] = None
    # 文件名称配置键
    file_name_config: str = 'default'
    # 是否重新打包
    force_rezip: bool = False


class StreamTaskItem(BaseData):
    """
    流式采集任务物料模型
    """
    # 【输入】对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = None
    # 【输入】商品链接
    url: str = None
    # 电商平台编码
    platCode: str = None
    # 【输入】来源APP（流采模式必填）
    appCode: str = None
    # 任务编号（批次）
    batchId: str = None
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = None


class StreamApiData(BaseModel):
    """
    流式采集通用数据接收模型
    """
    # 【输入】应用编码
    app_code: str
    # 【输入】任务类型
    task_type: TaskType = None
    # 【输入】任务明细清单
    task_items: List[StreamTaskItem] = None
    # 【输入】文件名称配置键
    file_name_config: str = 'default'


class StreamSearchItem(BaseData):
    """
    流采搜索单个
    """
    # 【输入】对象唯一序列号（全局唯一，可用于主键，等于_id）
    sn: str = Field(description="对象唯一序列号")
    # 【输入】搜索关键字
    keyword: str = Field(description="商品链接")
    # 【输入】搜索关键字
    page: int = Field(description="搜索页码", default=1)
    # 【输入】来源APP（流采模式）
    appCode: str = Field(description="应用编码", default=None)
    # 电商商品编码
    ecSkuId: str = Field(description="电商商品编码", default=None)
    # 电商平台编码（识别链接获得）
    platCode: str = Field(description="电商平台编码", default=None)
    # 电商平台名称（识别链接获得）
    platName: str = Field(description="电商平台名称", default=None)
    # 【输入】用户指定编号（可选，不填使用默认值，等于sn）
    rowId: str = Field(description="用户指定编号（可选，不填使用默认值，等于sn）", default=None)
    # 扩展字段，可是任意内容，透传
    callback: Union[str, Dict, List] = Field(description="扩展字段", default=None)

    def to_classify_result(self):
        rs = {
            'sn': self.sn,
            'keyword': self.keyword,
            'page': self.page,
            'ecSkuId': self.ecSkuId,
            'platCode': self.platCode,
            'platName': self.platName,
            'appCode': self.appCode,
        }
        # 可有可无
        if self.rowId is not None:
            rs['rowId'] = self.rowId
        if self.callback is not None:
            rs['callback'] = self.callback
        return rs


class StreamApiSearch(BaseModel):
    """
    流式采集搜索数据模型
    """
    # 【输入】应用编码
    app_code: str = Field(description="应用编码")
    # 【输入】任务类型
    task_type: TaskType = Field(description="任务类型", default=None)
    # 【输入】任务明细清单
    task_items: List[StreamSearchItem] = Field(description="任务明细清单")
    # 【输入】请求页码
    page: int = 1

