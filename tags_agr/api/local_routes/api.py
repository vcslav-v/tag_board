import os
import secrets

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from tags_agr import db_tools
from tags_agr.api import service

router = APIRouter()
security = HTTPBasic()


username = os.environ.get('API_USERNAME') or 'root'
password = os.environ.get('API_PASSWORD') or 'pass'


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get('/items-by-tag/{tag}')
def get_items_by_tag(tag: str, _: str = Depends(get_current_username)):
    """Get items by tag."""
    try:
        search_result = db_tools.get_items_by_tag(tag)
    except ValueError as val_err:
        return {'error': val_err.args}
    return search_result


@router.get('/items-by-title/{title}')
def get_items_by_title(title: str,  _: str = Depends(get_current_username)):
    """Get items by title."""
    try:
        search_result = db_tools.get_items_by_title(title)
    except ValueError as val_err:
        return {'error': val_err.args}
    return search_result


@router.post('/items_xls')
def push_items_xls(_: str = Depends(get_current_username), file_data: UploadFile = File(...)):
    """Push item to db."""
    try:
        service.push_xls_to_db(file_data)
    except ValueError as val_err:
        return {'error': val_err.args}
    return {'ok': 200}
