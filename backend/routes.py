from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from models import Book



router = APIRouter()

@router.get("/getAllBooks", response_description="List of all books", response_model=List[Book])
async def list_books(request: Request):
    books = [book async for book in request.app.books_container.read_all_items()]
    return books

@router.get("/getBookById", response_description="Get a book by ID", response_model=Book)
async def get_book_by_id(request: Request, id: str, pk: str):
    book = await request.app.books_container.read_item(id, partition_key=pk)
    return book

@router.patch("/removeComment", response_description="Remove a comment from a book", response_model=Book)
async def remove_comment(request: Request, id: str, pk: str, comment_index: int):
    books_container = request.app.books_container
    operations = [
        { "op": 'remove', "path": '/reviewcomments/'+str(comment_index) }
    ]
    response = await books_container.patch_item(item=id, partition_key=pk, patch_operations=operations)
    return response

@router.get("/20", response_description="List of all books")
async def list_books20(request: Request, page_offset: int = 0, limit: int = 20, rating: float = 0.0, genre: str = None, author: str = None, title: str = None, sortby: str = "title"):
    books_container = request.app.books_container
    query_items_response = books_container.query_items(
            query="SELECT c.title, c.author, c.img, c.rating FROM c  WHERE c.rating > @rating ORDER BY c."+sortby+" OFFSET @offset LIMIT @limit",
            parameters=[
                dict(
                    name="@offset",
                    value=page_offset*limit
                ),
                dict(
                    name="@limit",
                    value=limit
                ),
            dict(
                name="@rating",
                value=rating
                )            
            ]
        )
        
    items = [jsonable_encoder(book) async for book in query_items_response]
    return JSONResponse(content=items)

@router.patch("/addComment", response_description="Add a new comment for a book")
async def add_comment(request: Request, id: str, pk: str, comment_name: str, comment: str):
    new_comment = { "name": comment_name, "comment": comment }
    books_container = request.app.books_container
    book = await books_container.read_item(id, partition_key=pk)
    if "reviewcomments" in book:
        print(book["reviewcomments"])
        book["reviewcomments"].append(new_comment)
    else:
        book["reviewcomments"] = [new_comment]
    operations = [
        { "op": 'set', "path": '/reviewcomments', "value":book["reviewcomments"]}
    ]
    response = jsonable_encoder(await books_container.patch_item(item=id, partition_key=pk, patch_operations=operations))
    return JSONResponse(response)

@router.get("/getDummy", response_description="List of all genres")
async def get_dummy() -> dict:
    # return {"original_title":"The Hunger Games","title":"The Hunger Games (The Hunger Games, #1)"}
    return JSONResponse(content={"book_id":1,"goodreads_book_id":2767052,"best_book_id":2767052,"work_id":2792775,"books_count":272,"isbn":"439023483","isbn13":9780000000000.0,"authors":"Suzanne Collins","original_publication_year":2008.0,"original_title":"The Hunger Games","title":"The Hunger Games (The Hunger Games, #1)","language_code":"eng","average_rating":4.34,"ratings_count":4780653,"work_ratings_count":4942365,"work_text_reviews_count":155254,"ratings_1":66715,"ratings_2":127936,"ratings_3":560092,"ratings_4":1481305,"ratings_5":2706317,"image_url":"https:\/\/images.gr-assets.com\/books\/1447303603m\/2767052.jpg","small_image_url":"https:\/\/images.gr-assets.com\/books\/1447303603s\/2767052.jpg"})

@router.get("/search", response_description="List of all genres")
async def search() -> dict:
    # return {"original_title":"The Hunger Games","title":"The Hunger Games (The Hunger Games, #1)"}
    return {"results": [
                                    {
                                    "score": 1,
                                    "highlights": null,
                                    "document": {
                                        "id": "20",
                                        "goodreads_book_id": 7260188,
                                        "best_book_id": 7260188,
                                        "work_id": 8812783,
                                        "books_count": 239,
                                        "isbn": "439023513",
                                        "isbn13": "9780000000000.0",
                                        "authors": [
                                        "Suzanne Collins"
                                        ],
                                        "original_publication_year": 2010,
                                        "original_title": "Mockingjay",
                                        "title": "Mockingjay (The Hunger Games, #3)",
                                        "language_code": "eng",
                                        "average_rating": 4,
                                        "ratings_count": 1719760,
                                        "work_ratings_count": 1870748,
                                        "work_text_reviews_count": 96274,
                                        "ratings_1": 30144,
                                        "ratings_2": 110498,
                                        "ratings_3": 373060,
                                        "ratings_4": 618271,
                                        "ratings_5": 738775,
                                        "image_url": "https://images.gr-assets.com/books/1358275419m/7260188.jpg",
                                        "small_image_url": "https://images.gr-assets.com/books/1358275419s/7260188.jpg"
                                    }
                                    },
                                    {
                                    "score": 1,
                                    "highlights": null,
                                    "document": {
                                        "id": "31",
                                        "goodreads_book_id": 4667024,
                                        "best_book_id": 4667024,
                                        "work_id": 4717423,
                                        "books_count": 183,
                                        "isbn": "399155341",
                                        "isbn13": "9780000000000.0",
                                        "authors": [
                                        "Kathryn Stockett"
                                        ],
                                        "original_publication_year": 2009,
                                        "original_title": "The Help",
                                        "title": "The Help",
                                        "language_code": "eng",
                                        "average_rating": 4,
                                        "ratings_count": 1531753,
                                        "work_ratings_count": 1603545,
                                        "work_text_reviews_count": 78204,
                                        "ratings_1": 10235,
                                        "ratings_2": 25117,
                                        "ratings_3": 134887,
                                        "ratings_4": 490754,
                                        "ratings_5": 942552,
                                        "image_url": "https://images.gr-assets.com/books/1346100365m/4667024.jpg",
                                        "small_image_url": "https://images.gr-assets.com/books/1346100365s/4667024.jpg"
                                    }
                                    },
                                    {
                                    "score": 1,
                                    "highlights": null,
                                    "document": {
                                        "id": "45",
                                        "goodreads_book_id": 4214,
                                        "best_book_id": 4214,
                                        "work_id": 1392700,
                                        "books_count": 264,
                                        "isbn": "770430074",
                                        "isbn13": "9780000000000.0",
                                        "authors": [
                                        "Yann Martel"
                                        ],
                                        "original_publication_year": 2001,
                                        "original_title": "Life of Pi",
                                        "title": "Life of Pi",
                                        "language_code": null,
                                        "average_rating": 3,
                                        "ratings_count": 1003228,
                                        "work_ratings_count": 1077431,
                                        "work_text_reviews_count": 42962,
                                        "ratings_1": 39768,
                                        "ratings_2": 74331,
                                        "ratings_3": 218702,
                                        "ratings_4": 384164,
                                        "ratings_5": 360466,
                                        "image_url": "https://images.gr-assets.com/books/1320562005m/4214.jpg",
                                        "small_image_url": "https://images.gr-assets.com/books/1320562005s/4214.jpg"
                                    }
                                    },
                                    {
                                    "score": 1,
                                    "highlights": null,
                                    "document": {
                                        "id": "126",
                                        "goodreads_book_id": 234225,
                                        "best_book_id": 234225,
                                        "work_id": 3634639,
                                        "books_count": 241,
                                        "isbn": "340839937",
                                        "isbn13": "9780000000000.0",
                                        "authors": [
                                        "Frank Herbert"
                                        ],
                                        "original_publication_year": 1965,
                                        "original_title": "Dune",
                                        "title": "Dune (Dune Chronicles #1)",
                                        "language_code": "eng",
                                        "average_rating": 4,
                                        "ratings_count": 485032,
                                        "work_ratings_count": 525976,
                                        "work_text_reviews_count": 13239,
                                        "ratings_1": 13354,
                                        "ratings_2": 22778,
                                        "ratings_3": 74206,
                                        "ratings_4": 154771,
                                        "ratings_5": 260867,
                                        "image_url": "https://images.gr-assets.com/books/1434908555m/234225.jpg",
                                        "small_image_url": "https://images.gr-assets.com/books/1434908555s/234225.jpg"
                                    }
                                    },
                                    {
                                    "score": 1,
                                    "highlights": null,
                                    "document": {
                                        "id": "136",
                                        "goodreads_book_id": 137791,
                                        "best_book_id": 137791,
                                        "work_id": 1010054,
                                        "books_count": 75,
                                        "isbn": "006075995X",
                                        "isbn13": "9780000000000.0",
                                        "authors": [
                                        "Rebecca Wells"
                                        ],
                                        "original_publication_year": 1996,
                                        "original_title": "Divine Secrets of the Ya-Ya Sisterhood",
                                        "title": "Divine Secrets of the Ya-Ya Sisterhood",
                                        "language_code": "en-US",
                                        "average_rating": 3,
                                        "ratings_count": 465676,
                                        "work_ratings_count": 470508,
                                        "work_text_reviews_count": 3867,
                                        "ratings_1": 15795,
                                        "ratings_2": 35314,
                                        "ratings_3": 120396,
                                        "ratings_4": 158451,
                                        "ratings_5": 140552,
                                        "image_url": "https://images.gr-assets.com/books/1408313524m/137791.jpg",
                                        "small_image_url": "https://images.gr-assets.com/books/1408313524s/137791.jpg"
                                    }
                                    },
                                    {
                                    "score": 1,
                                    "highlights": null,
                                    "document": {
                                        "id": "149",
                                        "goodreads_book_id": 4374400,
                                        "best_book_id": 4374400,
                                        "work_id": 4422413,
                                        "books_count": 130,
                                        "isbn": "525421033",
                                        "isbn13": "9780000000000.0",
                                        "authors": [
                                        "Gayle Forman"
                                        ],
                                        "original_publication_year": 2009,
                                        "original_title": "If I Stay",
                                        "title": "If I Stay (If I Stay, #1)",
                                        "language_code": "en-US",
                                        "average_rating": 3,
                                        "ratings_count": 503527,
                                        "work_ratings_count": 567087,
                                        "work_text_reviews_count": 34959,
                                        "ratings_1": 12666,
                                        "ratings_2": 34896,
                                        "ratings_3": 122977,
                                        "ratings_4": 190793,
                                        "ratings_5": 205755,
                                        "image_url": "https://images.gr-assets.com/books/1347462970m/4374400.jpg",
                                        "small_image_url": "https://images.gr-assets.com/books/1347462970s/4374400.jpg"
                                    }
                                    },
                                    {
                                    "score": 1,
                                    "highlights": null,
                                    "document": {
                                        "id": "174",
                                        "goodreads_book_id": 1812457,
                                        "best_book_id": 1812457,
                                        "work_id": 2666268,
                                        "books_count": 134,
                                        "isbn": "964729237",
                                        "isbn13": "9780000000000.0",
                                        "authors": [
                                        "William Paul Young"
                                        ],
                                        "original_publication_year": 2007,
                                        "original_title": "The Shack: Where Tragedy Confronts Eternity",
                                        "title": "The Shack",
                                        "language_code": "eng",
                                        "average_rating": 3,
                                        "ratings_count": 419539,
                                        "work_ratings_count": 438292,
                                        "work_text_reviews_count": 29377,
                                        "ratings_1": 35734,
                                        "ratings_2": 42977,
                                        "ratings_3": 84751,
                                        "ratings_4": 111923,
                                        "ratings_5": 162907,
                                        "image_url": "https://images.gr-assets.com/books/1344270232m/1812457.jpg",
                                        "small_image_url": "https://images.gr-assets.com/books/1344270232s/1812457.jpg"
                                    }
                                    },
                                    {
                                    "score": 1,
                                    "highlights": null,
                                    "document": {
                                        "id": "180",
                                        "goodreads_book_id": 52036,
                                        "best_book_id": 52036,
                                        "work_id": 4840290,
                                        "books_count": 972,
                                        "isbn": "553208845",
                                        "isbn13": "9780000000000.0",
                                        "authors": [
                                        "Hermann Hesse",
                                        " Hilda Rosner"
                                        ],
                                        "original_publication_year": 1922,
                                        "original_title": "Siddhartha",
                                        "title": "Siddhartha",
                                        "language_code": "eng",
                                        "average_rating": 3,
                                        "ratings_count": 372099,
                                        "work_ratings_count": 418653,
                                        "work_text_reviews_count": 11518,
                                        "ratings_1": 10229,
                                        "ratings_2": 25529,
                                        "ratings_3": 83698,
                                        "ratings_4": 138837,
                                        "ratings_5": 160360,
                                        "image_url": "https://images.gr-assets.com/books/1428715580m/52036.jpg",
                                        "small_image_url": "https://images.gr-assets.com/books/1428715580s/52036.jpg"
                                    }
                                    }
                                ]
                                }
    