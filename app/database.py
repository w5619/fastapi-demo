from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession    # 从SQLAlchemy导入异步引擎和会话
from sqlalchemy.orm import sessionmaker, declarative_base   # 从SQLAlchemy导入会话工厂和声明基类
from app.config import settings   # 导入配置
from typing import AsyncGenerator

# 创建异步数据库引擎，负责与数据库通信
engine = create_async_engine(
    str(settings.DATABASE_URL),  # 数据库连接字符串
    echo=True,  # 开发环境下打印SQL语句，方便调试
    future=True,  # 使用SQLAlchemy 2.0风格的API
    pool_pre_ping=True,  # 连接池检查连接有效性，防止使用失效连接
)

# 创建异步会话工厂，用于创建数据库会话
AsyncSessionLocal = sessionmaker(
    engine,  # 使用上面创建的引擎
    class_=AsyncSession,  # 使用异步会话类
    expire_on_commit=False,  # 提交后不使对象过期
    autoflush=False  # 关闭自动刷新，手动控制刷新时机
)

# 声明基类，所有ORM模型都将继承这个类
Base = declarative_base()

# 定义获取数据库会话的依赖项  依赖项：为每个请求提供数据库会话
async def get_db() -> AsyncGenerator[AsyncSession, None]:   #异步生成器函数（使用 yield 的异步函数）的返回类型不是普通的 AsyncSession，
                                                            #而是 AsyncGenerator[AsyncSession, None] 
                                                            # 第一个类型参数 AsyncSession 表示生成的值的类型  第二个类型参数 None 表示发送回生成器的值的类型（这里不需要，所以用 None）
    async with AsyncSessionLocal() as session:       # 使用上下文管理器确保会话正确关闭
        try:
            yield session  # 提供会话给依赖它的函数   将会话注入到路由处理函数
            await session.commit()  # 如果没有异常，提交事务
        except Exception as e:
            await session.rollback()  # 如果有异常，回滚事务
            raise e  # 重新抛出异常，让FastAPI处理
        finally:
            await session.close()  # 无论成功失败，最终关闭会话（释放连接）