from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .model import Comment
from .database import (
    fetch_all_categories,
    fetch_category_name,
    fetch_comments_by_instrument_id,
    fetch_instruments_by_category,
    fetch_instrument_by_id,
    insert_comment,
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/categories")
def get_categories():
    all_categories = fetch_all_categories()

    return {"data": all_categories}


@app.get("/api/categories/{category_type}")
def get_instruments(category_type):
    instruments = fetch_instruments_by_category(category_type)
    category_name = fetch_category_name(category_type)

    if not category_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Current category was not found")

    for instrument in instruments:
        instrument["category_name"] = category_name

    return {"data": instruments}


@app.get("/api/categories/{category_type}/{instrument_id}")
def get_instrument_data(instrument_id):
    instrument_data = fetch_instrument_by_id(instrument_id)
    related_comments = fetch_comments_by_instrument_id(instrument_id)

    if not instrument_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Current instrument was not found")

    return {"data": {"instrument": instrument_data, "comments": related_comments}}


@app.post("/api/comments", status_code=status.HTTP_201_CREATED)
def create_comment(comment: Comment):
    comment_dict = comment.dict()
    responce = insert_comment(comment_dict)

    if not responce:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Something went wrong")

    return {"data": comment}
