青橄榄Django OpenAPI框架
=======================

## 框架简述

在django的基础上，保留django的便利ORM，以开发RESTful风格的接口为目标，构建一个支持输出openapi文档的框架。

最早本框架只用于OA的开发，因为数据平台相关开发类似，为避免重复维护框架代码，故而把框架代码抽象出来单独成库。

## 功能点

* 输出RESTful风格的openapi接口文档。支持Django原生的Model，兼容大部分常用字段类型。
* 接口输入输出的类型校验+转换，使接口与文档定义一致。
* 内置redoc，可直接配置文档展示。
* 接口URL路由根据目录结构自动索引，规避冗长的url.py配置文件。
* 多项核心附加工具：可输出的状态机，支持结构定义的JSONField等等。

## 核心依赖

* Django
* Pydantic<2

## 目录代码

### openapi

实现一个可以输出openapi文档的后端框架

#### django

生成针对django.db.models.Model支持输出读和写的pydantic model的代码。

#### models

供实现后端接口用的基础类定义。

#### base.py

openapi类入口，所有接口需要从该类定义。

#### exceptions.py

接口可抛出的异常

#### method_processor.py

接口方法生成器。用于快速生成一类具有固定功能的接口。

#### openapi_gen.py

具体实现输出openapi文档的代码

#### pdm_fields.py

实现一些常用的用于接口校验的数据类型

### status_machine

实现一个可与openapi框架协同工作的状态枚举工具（状态机）

#### base.py

实现了状态机内核。

#### exceptions.py

抛出异常基类

#### export.py

用于输出状态机文档的工具类

#### status_machine.py

状态机实体

### utils

其余与业务无关的通用工具类

#### apscheduler_utils.py

apscheduler相关的工具

#### cls_utils.py

类相关的工具

#### const.py

常量

#### decorators.py

装饰器工具

#### dict_utils.py

字典类工具

#### dt_utils.py

日期时间工具

#### ensured_dict.py

字典扩展（已弃用

#### expiring_set.py 

一个可按照时间针对数据过期的集合

#### extensive_raw_qs

定义了一个可扩展的django.db.QuerySet的接口类，用于构造一个支持在接口中分页的raw query

#### import_utils.py

导入工具

#### jwt_utils.py

jwt工具

#### logger_utils.py

loguru日志工具

#### perf_utils.py

性能检测类工具

#### privilege_utils.py

权限基类

#### pydantic_utils.py

pydantic工具，实现了一些pydantic的特殊功能

#### redis_key_utils.py

redis键定义工具

#### schema_utils.py

schema包的工具（已弃用

#### self_collecting_model.py

自收集类

#### serialize_utils.py

序列化工具

#### status_machine.py

(弃用)
代码已重构至外层目录，这里保留import以便旧代码能继续使用。

#### tmp_utils.py

临时文件工具
