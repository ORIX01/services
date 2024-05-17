import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from typing import  Annotated
from sqlalchemy.orm import Session


from database import database as database
from database.database import BookDB
from model.book import Book

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}

@app.get("/get_books")
async def get_books(db: db_dependency):
    try:
        result = db.query(BookDB).limit(100).all()
        return result
    except Exception as e:
        return "Can't access database!"

@app.get("/get_book_by_id")
async def get_book_by_id(book_id: int, db: db_dependency):
    try:
        result = db.query(BookDB).filter(BookDB.id == book_id).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_book")
async def add_book(book: Book, db: db_dependency):
    try :
        book_db = BookDB(
            id=book.id,
            title=book.title,
            author=book.author,
            published_date=book.published_date,
            pages=book.pages
        )
        db.add(book_db)
        db.commit()
        return book_db
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add book")

@app.delete("/delete_book")
async def delete_book(book_id: int, db: db_dependency):
    try:
        book_db = db.query(BookDB).filter(BookDB.id == book_id).first()
        if book_db is None:
            raise HTTPException(status_code=404, detail="Book not found")
        db.delete(book_db)
        db.commit()
        return {"message": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
