from pydantic import BaseModel, HttpUrl
from typing import Optional, List


class ReviewComment(BaseModel):
    name: str
    comment: str

class Book(BaseModel):
    _id: str
    id: Optional[str]
    author: Optional[str]
    bookformat: Optional[str]
    desc: str
    genre: List[str]
    img: HttpUrl
    isbn: str
    isbn13: int
    link: HttpUrl
    pages: int
    rating: float
    reviews: int
    title: str
    totalratings: int
    reviewcomments: List[ReviewComment]


