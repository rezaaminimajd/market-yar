from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey
from services.connections import Base
from sqlalchemy.dialects.postgresql import ENUM


class StatisticType(Enum):
    BEST_SELLING = 'BEST_SELLING'
    BASKET_MAKER = 'BASKET_MAKER'


class CategoryAreaStatistics(Base):
    __tablename__ = "category_area_statistic"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    city_id = Column(Integer, ForeignKey('city.id'))


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer, nullable=False)
    type = Column(ENUM(StatisticType), nullable=False, default=StatisticType.BEST_SELLING.value)
    product_name = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    category_area_id = Column(Integer, ForeignKey('category_area_statistic.id'))
