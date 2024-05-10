from sqlalchemy import Column, Integer, BigInteger, VARCHAR, ForeignKey, DateTime

from db.base import Base


class Account(Base):
    __tablename__ = 'accounts'

    number = Column(BigInteger, primary_key=True, nullable=False)


class Crypto(Base):
    __tablename__ = 'crypto'

    account__ID = Column(BigInteger, ForeignKey("accounts.number"), primary_key=True, nullable=False)
    dateTimeLastTap = Column(DateTime(timezone=True), nullable=True, default=None)
    proxy = Column(VARCHAR(256), nullable=True, default=None)
    result = Column(VARCHAR(256), nullable=True, default=None)
    action = Column(Integer, nullable=True, default=None)
    unixTime = Column(Integer, nullable=True, default=None)
    userAgent = Column(VARCHAR(256), nullable=True, default=None)


class Logs(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, nullable=False)
    phone = Column(BigInteger, nullable=True, default=None)
    datetime = Column(DateTime, nullable=True, default=None)
    botName = Column(VARCHAR(50), nullable=True, default=None)
    status = Column(VARCHAR(50), nullable=True, default=None)
    amount = Column(VARCHAR(20), nullable=True, default=None)
