from django import template
from editor.models import *
from django.template.loader import get_template
import datetime


register = template.Library()
#t = get_template('details.html')
#register.inclusion_tag(t)(show_hyps)

def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


@register.simple_tag
def show_hyps(question_id):	
	template=Question_template.objects.get(question_upload_id=question_id).template
	paras=Question_para.objects.filter(question_upload_id=question_id)
	k=random.randint(0,paras.count()-1)
	l=paras[k].para_chains
	for i in range(len(l)):
		template=template.replace('{0['+str(i)+']}',str(l[i]))
	return template


@register.simple_tag
def generate_question(id):
	return Question_upload.objects.get(pk=id).question


@register.tag
def some_function(value):
    return value - 2