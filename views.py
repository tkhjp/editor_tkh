from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404

from .models import *

def index(request):
    latest_questions = Question_upload.objects.order_by('-id')[:5]
    context = {'latest_questions': latest_questions}
    return render(request,'editor/index.html',context)


def detail(request, question_upload_id):
    #question = get_object_or_404(Question_upload, pk = question_upload_id)
    question_id = question_upload_id
    #t = get_template('details.html')
    #register.inclusion_tag(t)(show_hyps)
    return render(request, 'editor/details.html',{'question_id':question_id})
    #return HttpResponse("You're looking at question %s." % question_upload_id)

def results(request, question_upload_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_upload_id)

def edit_answer(request, question_upload_id):
    return HttpResponse("You're editting the answer %s." % question_upload_id)