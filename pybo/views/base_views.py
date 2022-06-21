import logging
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question, Answer, QuestionCount, Category

logger = logging.getLogger('pybo')

class ListParam:
    def __init__(self, page, kw, so):
        self.page = page
        self.kw = kw
        self.so = so

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request, category_name='qna'):
    """
    pybo 목록 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬 기준
    lp = ListParam(page, kw, so)
    request.session['lp'] = lp

    category_list = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    question_list = Question.objects.filter(category=category)

    # 정렬
    question_list = question_list.annotate(
        num_voter=Count('voter', distinct=True) + Count('answer__voter', distinct=True),
        num_answer=Count('answer', distinct=True) + Count('comment', distinct=True) + Count('answer__comment',
                                                                                            distinct=True))
    if so == 'recommend':
        question_list = question_list.order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = question_list.order_by('-create_date')

    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__content__icontains=kw)  # 답변내용검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'category': category, 'question_list': page_obj, 'page': page, 'kw': kw, 'so': so,
               'category_list': category_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # 입력 인자
    page = request.GET.get('page', '1')
    so = request.GET.get('so', 'recent')
    question = get_object_or_404(Question, pk=question_id)
    lp = request.session.get('lp')

    # 조회수
    ip = get_client_ip(request)
    cnt = QuestionCount.objects.filter(ip=ip, question=question).count()
    if cnt == 0:
        qc = QuestionCount(ip=ip, question=question)
        qc.save()
        if question.view_count:
            question.view_count += 1
        else:
            question.view_count = 1
        question.save()

    # 정렬
    answer_list = Answer.objects.filter(question=question).annotate(num_voter=Count('voter'))
    if so == 'recommend':
        answer_list = answer_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    else:
        answer_list = answer_list.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(answer_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question': question, 'answer_list': page_obj, 'page': page,
               'so': so, 'category': question.category, 'lp': lp}
    return render(request, 'pybo/question_detail.html', context)











