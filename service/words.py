import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import config as config

router = APIRouter()

url = config.WORD_API_URL


def get_random_word():

    url = "https://wordsapiv1.p.rapidapi.com/words/"

    querystring = {"random":"true"}

    headers = {
        "x-rapidapi-key": "067d58673cmsh05e814e4763711dp1dd7bajsn28558bd8fa39",
        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()['word']
    
@router.post("/getEngWord")  
def get_word_info():
    
	word = get_random_word()

	url = config.WORD_API_URL + word

	headers = {
		"x-rapidapi-key": config.WORD_API_KEY,
		"x-rapidapi-host": "wordsapiv1.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers)

	return response.text