from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    audio = serializers.FileField(required=False)
    video = serializers.FileField(required=False)

    class Meta:
        model = Note
        fields = '__all__'

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        audio = validated_data.pop('audio', None)
        video = validated_data.pop('video', None)

        note = super().create(validated_data)

        if image:
            note.image = image
        if audio:
            note.audio = audio
        if video:
            note.video = video

        note.save()
        return note

    def update(self, instance, validated_data):
        image = validated_data.pop('image', None)
        audio = validated_data.pop('audio', None)
        video = validated_data.pop('video', None)

        note = super().update(instance, validated_data)

        if image:
            note.image = image
        if audio:
            note.audio = audio
        if video:
            note.video = video

        note.save()
        return note
