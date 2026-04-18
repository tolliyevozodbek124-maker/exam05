from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.services.book_service import BookService
from app.db.session import get_db

router = APIRouter(prefix="/books", tags=["Books"])
service = BookService()


@router.get("/search", response_model=List[BookResponse])
def search(search: str = Query(..., description="Qidiruv so'zi"), db: Session = Depends(get_db)):
    """Title yoki Author bo'yicha qidirish"""
    return service.search_books(db, search)

@router.get("/filter", response_model=List[BookResponse])
def filter_books(min: int = Query(0), max: int = Query(2026), db: Session = Depends(get_db)):
    """Yillar oralig'i bo'yicha filterlash"""
    return service.filter_books_by_year(db, min, max)


@router.get("/", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return service.get_all_books(db)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = service.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return book

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return service.create_book(db, book)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    updated = service.update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return updated


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = service.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return {"message": "Muvaffaqiyatli o'chirildi"}