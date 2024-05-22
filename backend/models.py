from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class ReviewComment(BaseModel):
    name: str
    comment: str

class Book(BaseModel):
    id: str
    goodreads_book_id: int
    best_book_id: int
    work_id: int
    books_count: int
    isbn: str
    isbn13: str
    authors: List[str]
    original_publication_year: int
    original_title: str
    title: str
    language_code: str
    average_rating: float
    ratings_count: int
    work_ratings_count: int
    work_text_reviews_count: int
    ratings_1: int
    ratings_2: int
    ratings_3: int
    ratings_4: int
    ratings_5: int