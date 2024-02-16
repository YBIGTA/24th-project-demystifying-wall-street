from django.shortcuts import render
from django.http import *
import json
from django.http import JsonResponse
from .crawling import getFullTextfromURL
from .prompt import request_gemini

# Create your views here.

def website(request):
    return render(request, 'index.html', {'hello': "Hello, World!"})

def answer(request):
    if request.method == 'POST':
        url = ""
        
        try: 
            url = json.loads(request.body).get('url')
        except Exception as e:
            return HttpResponseBadRequest("Bad Request: url field is missing")
        
        if url is None or url == "":
            return HttpResponseBadRequest("Bad Request: invalid URL")
        
        news = getFullTextfromURL(url)
        result_from_gemini = request_gemini(news)
        
        answer = {
            "news": news,
            "summary": result_from_gemini['summary'],
            "economic_terminologies": result_from_gemini['economic_terminologies']
        }
        
        return JsonResponse(answer)
    
    else:
        return HttpResponseBadRequest("Bad Request: Only POST requests are allowed.")