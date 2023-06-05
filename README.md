# Django-AD-Project

웹서버 컴퓨팅 AD프로젝트

### 팀원
|학번|이름|
|------|---|
|xxxx1583|김기범|
|xxxx1656|유성현|

----------------------

### 1. 질문 및 답변 수정에 대한 히스토리 viewing 
    
1. pybo/models.py 의 Question과 Answer 모델에 modify_count 변수를 추가하여 수정될 때마다 값을 저장하도록 한다.
```python
class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_count = models.IntegerField(default=0)
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):
        return self.subject
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_count = models.IntegerField(default=0)
    voter = models.ManyToManyField(User, related_name='voter_answer')
```
2. pybo/views/answer_views.py 와 question_views.py 에서 각각 answer_modify함수와 question_modify함수가 호출되어 저장될 때마다
modify_count가 1씩 증가하도록 한다.

```python
def answer_modify(request, answer_id):
    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.modify_count += 1
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)
```


3. 마지막으로 question_detail.html 템플릿을 수정하여 수정된 횟수가 보이도록 한다.
```html
    <div class="badge badge-light p-2 text-left mx-3">
        <div class="mb-2"> 수정된 횟수 : {{ question.modify_count }}</div>
        <div>{{ question.modify_date }}</div>
    </div>
```
![image](https://github.com/jimi567/Django-AD-Project/assets/31495131/3633a5e4-5bb5-41da-9899-237f22811dc0)

### 2.comment view 분리 

1. pybo/urls.py의 매핑정보를 다음처럼 변경  
   ```python
   ...(생략)...
    # comment_views.py
    # path('comment/create/question/<int:question_id>/', comment_views.comment_create_question, name='comment_create_question'),
    # path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
    # path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),
    # path('comment/create/answer/<int:answer_id>/', comment_views.comment_create_answer, name='comment_create_answer'),
    # path('comment/modify/answer/<int:comment_id>/', comment_views.comment_modify_answer, name='comment_modify_answer'),
    # path('comment/delete/answer/<int:comment_id>/', comment_views.comment_delete_answer, name='comment_delete_answer'),

    # comment_question_views.py
    path('comment/create/question/<int:question_id>/', comment_question_views.comment_create_question, name='comment_create_question'),
    path('comment/modify/question/<int:comment_id>/', comment_question_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>/', comment_question_views.comment_delete_question, name='comment_delete_question'),
    # comment_answer_views.py
    path('comment/create/answer/<int:answer_id>/', comment_answer_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>/', comment_answer_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>/', comment_answer_views.comment_delete_answer, name='comment_delete_answer'),
    ...(생략)...
    ```


2. 기존의 comment_views.py 삭제
3. comment_question_views.py 추가
 ```python
 from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Question, Comment


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    pybo 질문댓글등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.modify_count += 1
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    pybo 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question_id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question_id)
```
4. comment_answer_views.py 추가
```python
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import CommentForm
from ..models import Answer, Comment


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답글댓글등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.question = answer.question
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    pybo 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.modify_count += 1
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    pybo 답글댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)

```

### 3.댓글 추천 기능

1. Comment 모델에 voter 필드를 추가하고, related_name 옵션을 추가한다.
```python
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_count = models.IntegerField(default=0)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    voter = models.ManyToManyField(User, related_name='voter_comment')
```

2. vote_views에 vote_comment 함수를 추가한다.
```python
def vote_comment(request, comment_id):
    """
    pybo 댓글추천등록
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        comment.voter.add(request.user)
    return redirect('pybo:detail', question_id=comment.question.id)
```
![image](https://github.com/jimi567/Django-AD-Project/assets/31495131/31f22299-ed8b-44d7-a913-ad3954b6ae20)

- 질문에 달린 댓글의 경우 잘 작동하지만 답변에 달린 댓글의 경우 redirection 시 question_id가 없어 오류가 발생한다.

```python
if form.is_valid():
    comment = form.save(commit=False)
    comment.author = request.user
    comment.create_date = timezone.now()
    comment.answer = answer
    comment.question = answer.question
    comment.save()
```
- 따라서 Comment_create_answer 함수에서 answer의 question을 불러와 답변댓글도 question.id까지 저장하도록 수정한다.

3. question_detail.html 템플릿을 수정한다.
```html
... 생략 ...
{% if request.user == comment.author %}
                                <a href="{% url 'pybo:comment_modify_question' comment.id  %}" class="small">수정</a>,
                                <a href="#" class="small delete"
                                   data-uri="{% url 'pybo:comment_delete_question' comment.id  %}">삭제</a>
                                {% endif %}
                                <div class="float-right">
                                    <span class="bg-light text-center p-2 border">{{ comment.voter.count }}</span>
                                    <span href="#" data-uri="{% url 'pybo:vote_comment' comment.id  %}"
                                    class=" temp recommend btn btn-sm btn-secondary ">추천</span>
                                </div>
... 생략 ...
```

4. 작동 결과 화면
![image](https://github.com/jimi567/Django-AD-Project/assets/31495131/4da0457b-392d-4009-836e-7388c4b9c59f)



### 4. 댓글 수정 횟수 표시 기능
1. 1번 문제와 마찬가지로 pybo/models.py 의 Comment모델에 modify_count 변수를 추가하여 수정될 때마다 값을 저장하도록 한다.
```python
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_count = models.IntegerField(default=0)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    voter = models.ManyToManyField(User, related_name='voter_comment')
```

2. pybo/views/comment_views.py 에서 각각 comment_modify_answer함수와 comment_modify_question함수가 호출되어 저장될 때마다 modify_count가 1씩 증가하도록 한다.
```python
def comment_modify_answer(request, comment_id):
    """
    pybo 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.modify_count += 1
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)
```
```python
def comment_modify_question(request, comment_id):
    """
    pybo 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.modify_count += 1
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)
```
3. 마지막으로  question_detail.html 템플릿을 수정하여 수정된 횟수가 보이도록 한다.
```html
<span>
    - {{ comment.author }}, {{ comment.create_date }}
    {% if comment.modify_date %}
    (수정:{{ comment.modify_date }}, 수정된 횟수:{{ comment.modify_count }})
    {% endif %}
</span>
```
![image](https://github.com/jimi567/Django-AD-Project/assets/31495131/b71fcdcd-af78-4d07-96ad-18d1033ae8d0)

### 5. 질문 댓글에 대한 페이지네이션과 정렬 기능

1. 테스트용 질문글에 댓글 100개 임의로 추가
    
    + python manage.py shell을 통해서 다음과 같이 임의로 추가
    
    <img width="345" alt="2-1찐" src="https://github.com/jimi567/Django-AD-Project/assets/28584160/cf3cd2b0-cc75-42a7-98a1-8bea74c9c0c2">

    + 결과화면
    
    <img width="909" alt="2-2" src="https://github.com/jimi567/Django-AD-Project/assets/28584160/ea0a0d3a-2e66-4237-8f8b-27a68c474021">

2. base_views.py의 detail 함수 변경

```python
def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)

    page = request.GET.get('page', '1')  # 페이지
    


    comment_list = Comment.objects.filter(question=question, answer=None).order_by('-create_date')

    paginator = Paginator(comment_list, 8)  # 페이지당 8개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question': question, 'comment_list': page_obj}
    return render(request, 'pybo/question_detail.html', context)
 ```
 
 + 페이지네이터를 활용해 페이징기능 구현
 + page = request.GET.get('page', '1') : GET 방식으로 호출된 URL에서 page값을 가져올 때 사용한다.page값 없이 호출된 경우에는 디폴트로 1이라는 값을 설정한다.
 + comment_list = Comment.objects.filter(question=question, answer=None).order_by('-create_date') : Comment 모델의 객체를 해당 question와 answer가 null인 필드값으로 필터링하여 가져온다. ( answer가 None인 이유는 같은 질문글에 대한 **답글의 댓글을 가져오는것을 방지하기 위함***)
 + paginator = Paginator(comment_list, 8) : 첫 번째 파라미터 comment_list는 질문 댓글 전체를 의미하는 데이터이고 두번째 파라미터 8은 페이지당 보여줄 게시물의 개수이다.
 + page_obj = paginator.get_page(page) : paginator를 이용하여 요청된 페이지(page)에 해당되는 페이징 객체(page_obj)를 생성했다. 이렇게 하면 장고 내부적으로는 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하도록 쿼리가 변경된다.
 
 3. question_detail.html 변경
 ```html
...(생략)...
       <!-- 질문 댓글 Start -->
                    {% if comment_list.paginator.count > 0 %}
                    <div class="mt-3">
                    {% for comment in comment_list %}
                        {% if comment.answer_id == null %}
                            <a name="comment_{{ comment.id }}"></a>
                            <div class="comment py-3 text-muted">
                                <span style="white-space: pre-line;">{{ comment.content }}</span>
                                <span>
                                    - {{ comment.author }}, {{ comment.create_date }}
                                    {% if comment.modify_date %}
                                    (수정:{{ comment.modify_date }}, 수정된 횟수:{{ comment.modify_count }})
                                    {% endif %}
                                </span>
                                {% if request.user == comment.author %}
                                <a href="{% url 'pybo:comment_modify_question' comment.id  %}" class="small">수정</a>,
                                <a href="#" class="small delete"
                                   data-uri="{% url 'pybo:comment_delete_question' comment.id  %}">삭제</a>
                                {% endif %}
                                <div class="float-right">
                                    <span class="bg-light text-center p-2 border">{{ comment.voter.count }}</span>
                                    <span href="#" data-uri="{% url 'pybo:vote_comment' comment.id  %}"
                                    class=" temp recommend btn btn-sm btn-secondary ">추천</span>
                                </div>

                            </div>
                       {% endif %}
                    {% endfor %}
                    </div>
                    {% endif %}
                    <div>
                        <a href="{% url 'pybo:comment_create_question' question.id  %}"
                           class="small"><small>댓글 추가 ..</small></a>
                    </div>
                    <!-- 페이징처리 시작 -->
                <ul class="pagination justify-content-center">
                    <!-- 이전페이지 -->
                    {% if comment_list.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ comment_list.previous_page_number }}">이전</a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <a class="page-link" tabindex="-1" aria-disabled="true" href="#">이전</a>
                    </li>
                    {% endif %}
                    <!-- 페이지리스트 -->
                    {% for page_number in comment_list.paginator.page_range %}
                    {% if page_number >= comment_list.number|sub:5 and page_number <= comment_list.number|add:5 %}
                    {% if page_number == comment_list.number %}
                    <li class="page-item active" aria-current="page">
                        <a class="page-link" href="?page={{ page_number }}">{{ page_number }}</a>
                    </li>
                    {% else %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_number }}">{{ page_number }}</a>
                    </li>
                    {% endif %}
                    {% endif %}
                    {% endfor %}
                    <!-- 다음페이지 -->
                    {% if comment_list.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ comment_list.next_page_number }}">다음</a>
                    </li>
                    {% else %}
                    <li class="page-item disabled">
                        <a class="page-link" tabindex="-1" aria-disabled="true" href="#">다음</a>
                    </li>
                    {% endif %}
                </ul>
    <!-- 페이징처리 끝 -->
                    <!-- 질문 댓글 End -->
                </div>
            </div>
...(생략)...
```
실제 댓글 내용은 comment_list의 각 comment들을 루프를 돌며 나타냈다.  
이전 페이지가 있는 경우에는 "이전" 링크가 활성화되게 하였고 이전 페이지가 없는 경우에는 "이전" 링크가 비활성화되도록 하였다. (다음페이지의 경우도 마찬가지 방법으로 적용되었다.)  
페이지 리스트는 현재 페이지 기준으로 좌우 5개씩 보이도록 만든다(템플릿 필터 add와 수업에서 추가했던 템플릿필터 sub를 사용) . 현재 페이지를 의미하는 comment_list.number보다 5만큼 크거나 작은 값만 표시되도록 만든 것이다.  

4. 페이징 기능 결과화면

<img width="750" alt="페이징기능은 완성" src="https://github.com/jimi567/Django-AD-Project/assets/28584160/cadbf49c-6ba7-484b-8067-9f2af29cd755">

5. 댓글 정렬 기능 추가(추천순, 최근순)
+ question_detail.html 코드 추가
```html
...(생략)..
 <!-- 질문 댓글 Start -->

                <div class="row justify-content-between my-3">
                    <div class="col-2">
                        <select class="form-control so">
                            <option value="recent" {% if so == 'recent' %}selected{% endif %}>최신순 댓글</option>
                            <option value="recommend" {% if so == 'recommend' %}selected{% endif %}>추천순 댓글</option>
                        </select>
                    </div>
                </div>
...(생략)...
<form id="searchForm" method="get" action="{% url 'pybo:detail' question.id %}">
    <input type="hidden" id="page" name="page" value="{{ page }}">
    <input type="hidden" id="so" name="so" value="{{ so }}">
</form>
{% endblock %}
{% block script %}
<script type='text/javascript'>
$(document).ready(function(){
    $(".delete").on('click', function() {
        if(confirm("정말로 삭제하시겠습니까?")) {
            location.href = $(this).data('uri');
        }
    });
    $(".recommend").on('click', function() {
        if(confirm("정말로 추천하시겠습니까?")) {
            location.href = $(this).data('uri');
        }
    });
     $(".so").on('change', function() {
        $("#so").val($(this).val());
        $("#page").val(1);
        $("#searchForm").submit();
    });
});
</script>
{% endblock %}
```
질문 댓글 맨 상단에 셀렉트를 추가합니다.  
해당 셀렉트에 폼과 자바스크립트 코드를 추가 합니다.(셀렉트를 변경할때 마다 리다이렉션)

+ base_views.py의 detail함수 변경
```python
def detail(request, question_id):
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)

    page = request.GET.get('page', '1')  # 페이지
    so = request.GET.get('so', 'recent')  # 정렬 기준

    # 정렬
    if so == 'recommend':
        comment_list = Comment.objects.filter(question=question, answer=None) \
            .annotate(num_voter=Count('voter')) \
            .order_by('-num_voter', '-create_date')
    else:  # 최신순
        comment_list = Comment.objects.filter(question=question, answer=None).order_by('-create_date')

    paginator = Paginator(comment_list, 8)  # 페이지당 8개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question': question, 'comment_list': page_obj, 'so': so}
    return render(request, 'pybo/question_detail.html', context)
```

+ so = request.GET.get('so', 'recent') : 디폴트 정렬 기준을 최근순으로 설정한다.
+ 만약 셀렉트된 정렬 기준이 'recommend'일 경우 comment_list를 .annotate(num_voter=Count('voter'))를 통해 num_voter라는 어노테이션 필드를 추가한다. 이는 Comment 모델의 voter 필드에 대한 개수를 세는 카운트를 의미한다. 따라서 각 댓글의 num_voter 필드에는 해당 댓글을 추천한 사용자의 수가 저장한다.
+ 최신순일 경우는 동일하게 create_date를 기준으로 역순정렬

6. 질문 댓글 정렬 기능 결과 화면


+ 최신순
![image](https://github.com/jimi567/Django-AD-Project/assets/28584160/ae1da358-3839-4a1d-a65b-81614cefc8f8)

+ 추천순
![image](https://github.com/jimi567/Django-AD-Project/assets/28584160/17f7ebd7-1067-4a51-a1b4-46c87c61eb29)
