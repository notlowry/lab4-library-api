from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Library API")


class BookIn(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    year: int = Field(..., ge=0, le=2100)


class Book(BookIn):
    id: int


books: list[Book] = []
next_id = 1


def find_book(book_id: int) -> Book:
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books")
def get_books():
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return find_book(book_id)


@app.post("/books", status_code=201)
def add_book(data: BookIn):
    global next_id
    book = Book(id=next_id, **data.model_dump())
    next_id += 1
    books.append(book)
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, data: BookIn):
    book = find_book(book_id)
    book.title = data.title
    book.author = data.author
    book.year = data.year
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    books.remove(book)
    return {"detail": "Book deleted"}
