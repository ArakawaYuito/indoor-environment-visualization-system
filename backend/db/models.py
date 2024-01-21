from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import Base

# 分布データを保存するテーブル
class Distribution(Base):
    __tablename__ = "Distribution"

    id = Column(Integer, primary_key=True)
    date = Column(String)
    dist = Column(String)

    def toDict(self):
        return {
            "id": self.id,
            "date": self.date,
            "dist": self.dist,
        }
    
# Apiのリクエスト時間を管理するテーブル
class ApiLastRequest(Base):
    __tablename__ = "ApiLastRequest"

    id = Column(Integer, primary_key=True)
    date = Column(String)
