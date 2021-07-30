from sqlalchemy import Column, ForeignKey, Integer, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


association_table = Table(
    'tags_association',
    Base.metadata,
    Column('item_id', Integer, ForeignKey('stock_items.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
)


class StockItem(Base):
    """Stock items."""

    __tablename__ = 'stock_items'

    id = Column(Integer, primary_key=True)

    title = Column(Text)

    tags = relationship(
        'Tag',
        secondary=association_table,
        back_populates='stock_items')

    batch_id = Column(Integer, ForeignKey('batches.id'))
    batch = relationship('Batch', back_populates='stock_items')


class Tag(Base):
    """Stock item's tags."""

    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)

    name = Column(Text, unique=True)

    stock_items = relationship(
        'StockItem',
        secondary=association_table,
        back_populates='tags')


class Batch(Base):
    """Batch number."""

    __tablename__ = 'batches'

    id = Column(Integer, primary_key=True)

    number = Column(Integer, unique=True)

    stock_items = relationship('StockItem', back_populates='batch')
