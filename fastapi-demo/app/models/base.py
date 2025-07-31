# 从SQLAlchemy导入列、日期时间和函数
from sqlalchemy import Column, DateTime, func
# 从SQLAlchemy导入声明属性装饰器
from sqlalchemy.ext.declarative import declared_attr
# 导入数据库基类
from app.database import Base

# 定义所有模型的基础类
class BaseModel(Base):
    """所有数据库模型的基础类，提供通用字段"""
    __abstract__ = True  # 抽象类，不会创建实际的表
    
    # 声明表名属性
    @declared_attr
    def __tablename__(cls) -> str:
        """自动生成表名，将类名转换为小写复数形式"""
        return cls.__name__.lower() + "s"
    
    # 记录创建时间的字段
    created_at = Column(
        DateTime(timezone=True),  # 带时区的日期时间类型
        server_default=func.now(),  # 服务器默认值为当前时间
        nullable=False  # 不允许为空
    )
    # 记录更新时间的字段
    updated_at = Column(
        DateTime(timezone=True),  # 带时区的日期时间类型
        onupdate=func.now()  # 更新时自动设置为当前时间
    )