from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..models import Question, Answer, Comment
from ..serializers import QuestionSerializer, AnswerSerializer, CommentsSerializer
from django.utils import timezone


class QuestionList(APIView):
    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        print("CBV API VIEW 호출")
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['author'] = request.user
        data['create_date'] = timezone.now()
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        question = self.get_object(pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        question = self.get_object(pk=pk)
        data = request.data
        data['modify_data'] = timezone.now()
        data['modify_data'] += 1
        serializer = QuestionSerializer(question, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = self.get_object(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
