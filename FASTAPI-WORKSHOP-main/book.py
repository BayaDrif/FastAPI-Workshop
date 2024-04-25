from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import Base, get_db
from sqlalchemy import Column, Integer, String, ForeignKey
import schemas, models


route = APIRouter()




# Add new book
@route.post("/books")
def add_book(request: schemas.book, db: Session = Depends(get_db)):
    
    new_book = models.book (title = request.title,
                           author =  request.author,
                           description = request.description,
                           published_year = request.published_year,
                           publisher = request.publisher
                        )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

# Retrieve a list of all books
@route.get("/books")
def get_all_books(db: Session = Depends(get_db)):
    return db.query(models.book).all()

# Retrieve details for a specific book
@route.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.book).filter(models.book.id == book_id).first()

# Update an existing book
@route.put("/books/{book_id}")
def update_book(book_id: int, request: schemas.book, db: Session = Depends(get_db)):
    book = db.query(models.book).filter(models.book.id == book_id).first()
    if book:
        for key, value in request.dict().items():
            setattr(book, key, value)
        db.commit()
        db.refresh(book)
        return {"message": "Book updated successfully"}
    return {"error": "Book not found"}

# Delete an existing book
@route.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return {"message": "Book deleted successfully"}
    return {"error": "Book not found"}


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str

@route.app("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def add_new_book(book: Book):
    # Logic to add book to the database
    return book