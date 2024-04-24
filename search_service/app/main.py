import os
import uvicorn
from fastapi import FastAPI, status
import requests

app = FastAPI()

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}

@app.get("/search_books")
async def search_books(query: str):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch data", "status_code": response.status_code}

@app.get("/book_details")
async def book_details(volume_id: str):
    url = f"https://www.googleapis.com/books/v1/volumes/{volume_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch data", "status_code": response.status_code}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
