from fastapi import APIRouter, File, UploadFile
from tags_agr import db_tools
from tags_agr.api import service

router = APIRouter()


@router.get('/items-by-tag/{tag}')
def get_items_by_tag(tag: str):
    """Get items by tag."""
    try:
        search_result = db_tools.get_items_by_tag(tag)
    except ValueError as val_err:
        return {'error': val_err.args}
    return search_result


@router.get('/items-by-title/{title}')
def get_items_by_title(title: str):
    """Get items by title."""
    try:
        search_result = db_tools.get_items_by_title(title)
    except ValueError as val_err:
        return {'error': val_err.args}
    return search_result


@router.post('/items_xls')
def push_items_xls(file_data: UploadFile = File(...)):
    """Push item to db."""
    try:
        service.push_xls_to_db(file_data)
    except ValueError as val_err:
        return {'error': val_err.args}
    return {'ok': 200}
