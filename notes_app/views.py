from django.shortcuts import render
import requests


def Home(request):
    access_key = 'SB2xojVCvvmbfkqb7FAMDGAq1Y4e4S34ILoAcwTBv0k'
    headers = {
        'Authorization': f'Client-ID {access_key}'
    }
    response = requests.get('https://api.unsplash.com/photos/random', headers=headers)
    data = response.json()
    image_url = data['urls']['regular']
    context = {
        'image_url': image_url
    }
    return render(request, 'home.html', context)


