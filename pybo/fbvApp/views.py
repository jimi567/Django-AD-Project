from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..models import Question
from pybo.serializers import QuestionSerializer
from django.utils import timezone


from rest_framework import permissions


class IsAuthorOrReadonly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user and request.method in ['PUT', 'PATCH', 'DELETE']

#question_list
@api_view(['GET','POST']) # api 뷰 데코
@permission_classes([IsAuthenticated])
def question_list(request):

    if request.method == 'GET':
        question = Question.objects.all()
        serializer = QuestionSerializer(question,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        data['author'] = request.user.id
        data['create_date'] = timezone.now()
        data['voter'] = []
        # print("Log : " ,data)
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#question_detail
@api_view(['GET','PUT','DELETE'])
def question_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        data['author'] = request.user
        data['create_data'] = timezone.now()
        serializer = QuestionSerializer(question, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)