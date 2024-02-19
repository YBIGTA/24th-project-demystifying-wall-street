from django.shortcuts import render
from django.http import *
import json
from django.http import JsonResponse
from .crawling import normal_requests
from .ybigta_gemini import start as request_gemini

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
       
        news = normal_requests(url)
        print('done crawling, news:', news["text"])
        summary, terms, definitions = request_gemini(news["text"])
        print(definitions)
        
        if definitions == "error":
            error_response = {
                "news": news["text"],
                "summary": summary,
                "economic_terminologies": ""
            }
            return JsonResponse(error_response)
        
        economic_terminologies = convert_result(terms, definitions)
        
        answer = {
            "news": news["text"],
            "summary": summary,
            "economic_terminologies": economic_terminologies
        }
        
        print(answer)
        return JsonResponse(answer)
    
    else:
        return HttpResponseBadRequest("Bad Request: Only POST requests are allowed.")

def convert_result(terms, definitions):
    '''
    '''
    result = '<ui>'
    
    for term, definition in zip(terms, definitions):
        clean_term = term.split('. ', 1)[1]
        clean_definition = definition.split('. ', 1)[1]
        result += f'<li><b>{clean_term}</b>: {clean_definition}</li>'
    result += '</ui>'
    
    return result