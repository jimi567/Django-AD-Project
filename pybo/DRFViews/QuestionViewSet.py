from rest_framework.viewsets import ModelViewSet
from pybo.serializers import QuestionSerializer
from ..models import Question

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer