import os

import databases
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()

database = databases.Database(os.getenv('DATABASE_URL'))

metadata = sa.MetaData()

engine = sa.create_engine(
    os.getenv('DATABASE_URL'), connect_args={'check_same_thread': False}
)
