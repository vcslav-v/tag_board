from typing import List
from tags_agr import models
from tags_agr.db import SessionLocal
from collections import Counter
from tags_agr import schemas


def push(raw_title: str, tags: List[str], batch_num: int):
    db = SessionLocal()
    title = raw_title.strip()
    batch_item = db.query(models.Batch).filter_by(number=batch_num).first()
    stock_item = db.query(models.StockItem).filter_by(
        title=title,
        batch=batch_item,
    ).first()
    if stock_item:
        db.close()
        return

    if not batch_item:
        batch_item = models.Batch(number=batch_num)
        db.add(batch_item)
    stock_item = models.StockItem(title=title, batch=batch_item)
    db.add(stock_item)

    for raw_tag in set(tags):
        tag = raw_tag.strip()
        tag_item = db.query(models.Tag).filter_by(name=tag).first()
        if not tag_item:
            tag_item = models.Tag(name=tag)
            db.add(tag_item)
        stock_item.tags.append(tag_item)
    db.commit()
    db.close()


def get_items_by_title(title: str) -> schemas.SearchResult:
    result = schemas.SearchResult(
        items=[],
        tags_stat=[],
    )
    with SessionLocal() as db:
        search = "%{}%".format(title)
        stock_items = db.query(models.StockItem).filter(
            models.StockItem.title.ilike(search)
        ).all()
        all_tags = []
        for stock_item in stock_items:
            tags = [tag.name for tag in stock_item.tags]
            all_tags.extend(tags)
            result.items.append(schemas.Item(
                batch=stock_item.batch.number,
                title=stock_item.title,
                tags=tags,
            ))
    result.tags_stat = sorted(
        Counter(all_tags).items(),
        key=lambda x: x[1],
        reverse=True
    )
    return result


def get_items_by_tag(tag: str) -> schemas.SearchResult:
    result = schemas.SearchResult(
        items=[],
        tags_stat=[],
    )
    with SessionLocal() as db:
        items_tag = db.query(models.Tag).filter_by(
            name=tag.lower()
        ).first()
        all_tags = []
        for stock_item in items_tag.stock_items:
            tags = [tag.name for tag in stock_item.tags]
            all_tags.extend(tags)
            result.items.append(schemas.Item(
                batch=stock_item.batch.number,
                title=stock_item.title,
                tags=tags,
            ))
    result.tags_stat = sorted(
        Counter(all_tags).items(),
        key=lambda x: x[1],
        reverse=True
    )
    return result
