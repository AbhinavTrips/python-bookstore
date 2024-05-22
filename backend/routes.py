from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from models import Book
import json
from dotenv import dotenv_values
from openai import AzureOpenAI


# specify the name of the .env file name 
config = dotenv_values(".env")
openai_endpoint = config['openai_api_endpoint']
openai_key = config['openai_api_key']
openai_api_version = config['openai_api_version']
openai_embeddings_deployment = config['embedding_model_deployment_name']
openai_completions_deployment = config['completions_model_deployment_name']
# Create the OpenAI client
openai_client = AzureOpenAI(azure_endpoint=openai_endpoint, api_key=openai_key, api_version=openai_api_version)

router = APIRouter()

def generate_embeddings(text):
    '''
    Generate embeddings from string of text.
    This will be used to vectorize data and user input for interactions with Azure OpenAI.
    '''
    response = openai_client.embeddings.create(input=text, model=openai_embeddings_deployment)
    embeddings =response.model_dump()
    return embeddings['data'][0]['embedding']

@router.get("/getAllBooks", response_description="List of all books", response_model=List[Book])
async def list_books(request: Request):
    books = [book async for book in request.app.books_container.read_all_items()]
    return books

@router.get("/getBookById", response_description="Get a book by ID")
async def get_book_by_id(request: Request, id: str, isbn10: str):
    book = await request.app.books_container.read_item(id, partition_key=isbn10)
    book_response = {}
    book_response["id"] = book["id"]
    book_response["isbn10"] = book["isbn10"]
    book_response["title"] = book["title"]
    book_response["authors"] = [book["authors"]]
    book_response["thumbnail"] = book["thumbnail"]
    book_response["average_rating"] = book["average_rating"]
    book_response["description"] = book["description"]
    book_response["original_publication_year"] = book["published_year"]

    return book_response

@router.patch("/removeComment", response_description="Remove a comment from a book", response_model=Book)
async def remove_comment(request: Request, id: str, pk: str, comment_index: int):
    books_container = request.app.books_container
    operations = [
        { "op": 'remove', "path": '/reviewcomments/'+str(comment_index) }
    ]
    response = await books_container.patch_item(item=id, partition_key=pk, patch_operations=operations)
    return response


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



@router.get("/get_items_count", response_description="Get the count of all items")
async def get_items_count(request: Request):
    books_container = request.app.books_container
    get_items = books_container.query_items("Select VALUE COUNT(1) from c")
    count = [item async for item in get_items]
    data = {}  
    data["count"] = count[0]
    return JSONResponse(data)

@router.get("/list_books_by_page", response_description="List books by page")
async def list_books_by_page(request: Request, page_offset: int = 0, limit: int = 20, search_text: str = None, count:int = 100):
    books_container = request.app.books_container

    query_items_response = books_container.query_items(
            query="SELECT c.id, c.isbn10, c.title, c.authors, c.thumbnail, c.average_rating FROM c  OFFSET @offset LIMIT @limit",
            parameters=[
                dict(
                    name="@offset",
                    value=page_offset*limit
                ),
                dict(
                    name="@limit",
                    value=limit
                )         
            ]
        )
    
            
    items = [jsonable_encoder(book) async for book in query_items_response]
    full_response = {}    
    full_response["count"] = count
    full_response["facets"] = {}
    full_response["results"] = items
    return JSONResponse(full_response)


@router.get("/get_vector_search_results", response_description="Get top 5 results based on similarity search")
async def get_vector_search_results(request: Request, search_text: str, similarity_threshold: float = 0.3):
    books_container = request.app.books_container
    embedding = generate_embeddings(search_text)
    query_items_response = books_container.query_items(
                query='SELECT TOP 5 c.id, c.description, c.isbn10, c.title, c.authors, c.thumbnail, c.average_rating, VectorDistance(c.embeddings,@embedding, false, {"distanceFunction": "cosine"}) as SimilarityScore FROM c WHERE VectorDistance(c.embeddings,@embedding, true, {"distanceFunction": "cosine"}) > @similarity_score',
        parameters=[
            {"name": "@embedding", "value": embedding},
            {"name": "@similarity_score", "value": similarity_threshold}
        ])

    items = [jsonable_encoder(book) async for book in query_items_response]
    full_response = {}    
    full_response["count"] = 100
    full_response["facets"] = {}
    full_response["results"] = items
    return JSONResponse(full_response)