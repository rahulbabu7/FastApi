from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy import TIMESTAMP, Column,Integer,String,Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Posts(Base):
    __tablename__ = "Posts"  #table name

    # define columns
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))    #default to created now ()
    
      # add user_id as foreign key
    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=False)  # foreign key to Users table
    
    # define relationship to Users
    user = relationship("Users", back_populates="posts")
    

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))    #default to created now ()
    # define relationship to Posts
    posts = relationship("Posts", back_populates="user")
