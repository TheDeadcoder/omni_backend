# Tech-stack Of the Project

- [Supabase](https://supabase.com/)
- [Python](https://www.python.org/)
- [FastApi](https://fastapi.tiangolo.com/) LLM model
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)

# Set up and usage

## Cloning the repository

You can clone the repository by simply

```bash
git clone https://github.com/TheDeadcoder/omni_backend.git
```

## Making Python Virtual Environment

```bash
python3 -m venv omni

source omni/bin/activate
```

## Set Up The project

Once you've cloned the project, install the required dependencies with

```bash
pip install -r requirements.txt
```

## Set up alembic

```bash
alembic init alembic
```

> go to alembic.ini file in your project directory. \
> set sqlalchemy.url = postgresql://user:password@host/dbname \
> go to alembic.ini file in your project directory. \
> sqlalchemy.url = postgresql://user:password@host/dbname \

> change env.py as following:

```
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from models import Base # Import your models here

config = context.config

if config.config_file_name is not None:
fileConfig(config.config_file_name)

target_metadata = Base.metadata # Set the target metadata to your Base metadata

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
```

> Finally \

```bash
alembic revision --autogenerate -m "commit message"
alembic upgrade head
```

## Run the application with

```bash
uvicorn main:app
```

> You can then go to the /docs endpoint to test API

## Environment file

> You will be needing an environment file copnsisting of the following entities

```bash
SUPABASE_DATABASE_URL = "******"
SUPABASE_URL = "******"
SUPABASE_API_KEY = "******"
```
