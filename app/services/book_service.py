from sqlalchemy.orm import Session
from app.models.book import Book

class BookService:
    def get_all_books(self, db: Session):
        return db.query(Book).all()

    def get_book_by_id(self, db: Session, book_id: int):
        return db.query(Book).filter(Book.id == book_id).first()

    def create_book(self, db: Session, book):
        new_book = Book(**book.dict())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book

    def update_book(self, db: Session, book_id: int, book):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return None
        for key, value in book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book

    def delete_book(self, db: Session, book_id: int):
        db_book = db.query(Book).filter(Book.id == book_id).first()
        if not db_book:
            return None
        db.delete(db_book)
        db.commit()
        return {"message": "Book deleted"}

    
    def search_books(self, db: Session, query: str):
        """Title yoki Author bo'yicha qidirish"""
        return db.query(Book).filter(
            (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
        ).all()

    def filter_books_by_year(self, db: Session, min_year: int, max_year: int):
        """Yillar oralig'i bo'yicha filterlash"""
        return db.query(Book).filter(Book.year >= min_year, Book.year <= max_year).all()