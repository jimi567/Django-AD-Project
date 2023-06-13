from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..models import Question, Answer, Comment
from ..serializers import QuestionSerializer, AnswerSerializer, CommentsSerializer
from django.utils import timezone
from rest_framework import permissions
from ..permission import IsAuthorOrReadonly

class QuestionList(APIView):

    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        print("CBV API VIEW 호출")
        return Response(serializer.data)

    def post(self, request):
        print("abc")
        print(request.user)
        data = request.data
        data['author'] = request.user.id
        data['create_date'] = timezone.now()
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    permission_classes = [IsAuthorOrReadonly]
    print("afsdafasfd")
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
        print(question.modify_count)
        data = request.data
        #print(question.data)
        data['author'] = request.user.id
        data['modify_date'] = timezone.now()
        data['modify_count'] = question.modify_count + 1
        serializer = QuestionSerializer(question, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = self.get_object(pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
