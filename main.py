from fastapi import FastAPI 


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

