import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import config as config

router = APIRouter()

url = config.WORD_API_URL


def get_random_word():
    try:
        response = requests.get('https://random-word-api.herokuapp.com/word')
        if response.status_code == 200:
            word = response.json()[0]  # 첫 번째 단어를 가져옴
            print(word)
            return word
    except Exception as e:
        print(f"오류 발생: {e}")
        return None
    
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