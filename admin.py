from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
#from django.contrib.sites.models import Site

# Register your models here.
from .models import *

class HypothesisInlines(admin.StackedInline):
	verbose_name = '条件'
	verbose_name_plural = '問題詳細'
	model = Hypothesis
	extra = 0




class QuestionAdmin(admin.ModelAdmin):
	
	list_display = ['question', 'has_formula', 'has_table','has_img']
	#fields=['types','hypothesis']

	inlines = [ HypothesisInlines ]

	fieldsets = [
        (None,      {'fields': ['question']}),
        ('学年', {'fields': ['years_of_question'], 
        			# 'classes': ['collapse']
        			}),
        ]
    #inlines = [ testa ]
    
class ParaAdmin(admin.ModelAdmin):

	#fields=('Question_upload','sample','para_chains','ans')
	readonly_fields =('sample',)
	def sample(self,obj):
		return mark_safe( obj.test())




admin.site.unregister(User)
admin.site.unregister(Group)
#admin.site.register(Question)
admin.site.register(Question_upload,QuestionAdmin)
admin.site.register(Question_para,ParaAdmin)
#admin.site.register(Hypothesis)
#admin.site.register(Parameter)
#admin.site.register(Tags_list)