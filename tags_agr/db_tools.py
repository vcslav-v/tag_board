from typing import List
from tags_agr import models
from tags_agr.db import SessionLocal
from collections import Counter


def push(raw_title: str, tags: List[str]):
    db = SessionLocal()
    title = raw_title.strip()
    stock_item = models.StockItem(title=title)
    db.add(stock_item)

    for raw_tag in tags:
        tag = raw_tag.strip()
        tag_item = db.query(models.Tag).filter_by(name=tag).first()
        if not tag_item:
            tag_item = models.Tag(name=tag)
            db.add(tag_item)
        stock_item.tags.append(tag_item)
    db.commit()
    db.close()


def get_items_by_title(title: str):
    db = SessionLocal()
    search = "%{}%".format(title)
    stock_items = db.query(models.StockItem).filter(
        models.StockItem.title.like(search)
    ).all()
    result = []
    all_tags = []
    for i, stock_item in enumerate(stock_items):
        tags = [tag.name for tag in stock_item.tags]
        all_tags.extend(tags)
        result.append((i, stock_item.title, ', '.join(tags)))
    db.close()
    tag_stats = sorted(Counter(all_tags).items(), key=lambda x: x[1], reverse=True)
    return result, tag_stats


def get_items_by_tag(tag: str):
    db = SessionLocal()
    items_tag = db.query(models.Tag).filter_by(
        name=tag.lower()
    ).first()
    result = []
    all_tags = []
    for i, stock_item in enumerate(items_tag.stock_items):
        tags = [tag.name for tag in stock_item.tags]
        all_tags.extend(tags)
        result.append((i, stock_item.title, ', '.join(tags)))
    db.close()
    tag_stats = sorted(Counter(all_tags).items(), key=lambda x: x[1], reverse=True)
    return result, tag_stats
