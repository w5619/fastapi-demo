import sys
from pathlib import Path

# 将项目根目录添加到Python搜索路径
# 确保当前文件(migrations/env.py)的父目录是项目根目录
sys.path.append(str(Path(__file__).parent.parent))  # 关键：添加项目根路径

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 现在可以正常导入app模块了
from app.config import settings
from app.database import Base
from app.models import *  # 导入所有模型

# 从配置中获取数据库连接信息
config = context.config
config.set_main_option("DATABASE_URL_SYNC", str(settings.DATABASE_URL_SYNC))

# 配置日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 目标元数据
target_metadata = Base.metadata

# 以下是原有的迁移逻辑（保持不变）
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
