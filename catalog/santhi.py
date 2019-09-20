from sqlalchemy  import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base=declarative_base()

class Register(Base):
	__tablename__='register'

	id=Column(Integer,primary_key=True)
	name=Column(String(100))
	surname=Column(String(100))
	mobile=Column(String(20))
	email=Column(String(50))
	branch=Column(String(40))
	role=Column(String(50))



engine=create_engine('sqlite:///iii.db')
Base.metadata.create_all(engine)
print("Database is created...")