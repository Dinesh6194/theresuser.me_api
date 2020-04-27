from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://Dinesh:DK#Amazon6194@database-1.cel2fvwg72oo.ap-southeast-2.rds.amazonaws.com:5432/RoyalFlush', convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db():
    metadata.create_all(bind=engine)