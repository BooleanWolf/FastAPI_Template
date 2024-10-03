from fastapi import FastAPI 
from typing import Optional

from pydantic  import BaseModel 
import uvicorn

app = FastAPI() 

@app.get('/')
def index():
    return {
        "data" : {
            "name" : "Tamim"
        }
    }


@app.get('/about')
def about():
    return {
        'data' : {'Hello'} # Return list 
    }

@app.get('/blog') #'/blog?limit=10&published=true' 
def blog(limit = 10, published: bool = False, sort: Optional[str] = None):

    if published: 
        return {'data' : f'published {sort} Blog list {limit}'}
    else:
        return {'data' : f"{limit} {sort}  blgos"}


@app.get('/blog/unpublished')
def param_f():
    return {'data' : "Unpbilished"}



@app.get('/blog/{id}')
def param_f(id: int):
    return {'data' : id} 


@app.get('/blog/{id}/comments')
def param_f(id):
    return {'data' : {'comments': id}} 


class Blog(BaseModel):
    title: str 
    body: str 
    published: Optional[bool] 


@app.post('/blog')
def create_blog(request: Blog):
    return {'data' : request.title}


if __name__ == "__main__":
    # uvicorn.run(app, host="192.168.0.167", port=9000)
    uvicorn.run(app, host="127.0.0.1", port=9000)