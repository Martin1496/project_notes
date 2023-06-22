from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
import requests
from .models import Note
from .serializers import NoteSerializer

class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = request.data.get('image', None)
        audio = request.data.get('audio', None)
        video = request.data.get('video', None)

        if image:
            serializer.validated_data['image'] = image
        if audio:
            serializer.validated_data['audio'] = audio
        if video:
            serializer.validated_data['video'] = video

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_update(self, serializer):
        serializer.save()

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        image = request.data.get('image', None)
        audio = request.data.get('audio', None)
        video = request.data.get('video', None)

        if image:
            serializer.validated_data['image'] = image
        if audio:
            serializer.validated_data['audio'] = audio
        if video:
            serializer.validated_data['video'] = video

        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class NoteShare(generics.GenericAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.share()
        return Response({'message': 'Note shared successfully.'}, status=status.HTTP_200_OK)


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
