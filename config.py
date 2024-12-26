from app import app
import os

app.config.from_mapping({
    key: os.getenv(key) 
    for key in os.environ.keys() 
})