from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Define the connection to the DB
engine = create_engine('sqlite:///database/dictionary.sqlite')

Base = automap_base()
Base.prepare(engine, reflect=True)
Dictionary = Base.classes.dictionary

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/test')
async def root():
    return 'Hello World'


@app.get('/definition')
async def home(q: str):
    
    session = Session(engine)
    
    results = session.query(Dictionary.definition, Dictionary.root, Dictionary.word, Dictionary.points).filter(Dictionary.word.like(f'{q}%')).limit(10).all()
    
    session.close()
    
    return results