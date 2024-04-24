import asyncpg
import requests
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'library_service/app'))
sys.path.append(str(BASE_DIR / 'search_service/app'))

from library_service.app.main import service_alive as library_status
from search_service.app.main import service_alive as search_status

@pytest.mark.asyncio
async def test_database_connection():
    try:
        connection = await asyncpg.connect("postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query")
        assert connection
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"

@pytest.mark.asyncio
async def test_books_api():
    r = requests.get("https://www.googleapis.com/books/v1/volumes?q=potter")
    assert r.status_code == 200

@pytest.mark.asyncio
async def test_library_service_connection():
    r = await library_status()
    assert r == {'message': 'service alive'}

@pytest.mark.asyncio
async def test_search_service_connection():
    r = await search_status()
    assert r == {'message': 'service alive'}