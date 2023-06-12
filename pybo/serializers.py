from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from pybo.models import Question, Answer, Comment
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):

    question = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    class Meta:
        model = User
        field = ['id', 'username','question']

class QuestionSerializer(ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Question
        fields = ['id', 'author', 'subject', 'content', 'create_date', 'modify_date', 'modify_count']
        labels = {
            'subject': '제목',
            'content': '내용',

        }

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'author', 'question', 'content', 'create_date', 'modify_date', 'modify_count', 'voter']
        labels = {
            'content': '답변내용',
        }

class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'create_date', 'modify_date', 'modify_count', 'question', 'answer', 'voter']
        labels = {
            'content': '댓글내용',
        }
