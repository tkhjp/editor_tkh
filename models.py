from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django_mysql.models import ListCharField
import random

######
from bs4 import BeautifulSoup
import re
# Create your models here.

def with_formula(hypothesis):
	soup=BeautifulSoup(hypothesis)
	if len(soup('span',class_='math-tex'))==0:
		return False
	else:
		return True

def with_image(hypothesis):
	soup=BeautifulSoup(hypothesis)
	return 'img' in [tag.name for tag in soup.find_all(True)]
	
def with_table(hypothesis):
	soup=BeautifulSoup(hypothesis)
	return 'table' in [tag.name for tag in soup.find_all(True)]

def prettify(strings):
	soup=BeautifulSoup(strings)
	return soup.body.p.prettify()

def marking_numbers_formula(t):
	pattern = re.compile(r'(\d+\.?\d*|<span class="math-tex"><//span>)')
	soup=BeautifulSoup(t)
	c= 0
	l = re.findall(pattern,soup.span.text)
	sPos=0
	temp_str=soup.span.text
	temp_re =''
	template = ''
	for j in range(len(l)):
		nPos=temp_str[sPos:].index(l[j])+sPos
		if j==len(l)-1:
					#temp_re=temp_re+temp_str[sPos:].replace(l[j],'\color{red}{'+l[j]+'}',1)
			template=template+temp_str[sPos:].replace(l[j],'{0['+str(c)+']}',1)
			c=c+1
		else:
					#temp_re=temp_re+temp_str[sPos:nPos+len(l[j])].replace(l[j],'\color{red}{'+l[j]+'}',1)
			template=template+temp_str[sPos:nPos+len(l[j])].replace(l[j],'{0['+str(c)+']}',1)
			c=c+1
				#print(template)
		sPos=nPos+len(l[j])
	print(template)
	soup.span.string=template
	return [str(soup.span),l]

def marking_numbers_text(t):
	pattern = re.compile(r'-?\d+\.?\d*')
	soup = BeautifulSoup(t)
	k= str(soup.p)
	l = re.findall(pattern,k)
	sPos=0
	temp_str=k
	temp_re=''
	template= ''
	c=0
	for j in range(len(l)):
		nPos=temp_str[sPos:].index(l[j])+sPos
		if j==len(l)-1:
			#temp_re=temp_re+temp_str[sPos:].replace(l[j],'<span style="color:#e74c3c">'+l[j]+'</span>',1)
			template=template+temp_str[sPos:].replace(l[j],'{0['+str(c)+']}',1)
			c=c+1	
		else:
			#temp_re=temp_re+temp_str[sPos:nPos+1+len(l[j])].replace(l[j],'<span style="color:#e74c3c">'+l[j]+'</span>',1)
			template=template+temp_str[sPos:nPos+1+len(l[j])].replace(l[j],'{0['+str(c)+']}',1)
			c=c+1
		sPos=nPos+1+len(l[j])	
	return [template,l]

def make_template(question_id):
	h=Question_upload.objects.get(pk=question_id).hypothesis_set.all()
	k=0
	template=''
	para=[]
	for e in h:
		l=super_make_template(e.hypothesis)
		if k==0:
			template=l[0]
			para=l[1]
			k=len(l[1])
		else:
			for i in range(len(l[1])):
				before = '{0['+str(j)+']}'
				temp = '{0['+str(k)+']}'
				if l[0].count(temp)==1:
					l[0]=l[0].replace(before,temp)
				else:
					l[0]=l[0][::-1]
					before=before[::-1]
					temp=temp[::-1]
					l[0]=l[0].replace(before,temp,1)
					l[0]=l[0][::-1]
				k=k+1
				para.append(l[1][i])
	q=Question_upload.objects.get(pk=question_id)
	q.question_template_set.create(template=template)
	q.question_para_set.create(para_chains=para)
	return [template,para]


def super_make_template(strings):
	#h=Question_upload.objects.get(pk=question_id).hypothesis_set.all()
	k=0
	tempate=''
	para=[]
	para_formula=[]
	para_formula_counts=0
	para_text_counts=0
	para_text=[]
	soup=BeautifulSoup(strings)
	formula_counts =len(soup('span',class_='math-tex'))
	if formula_counts!=0:
		for i in range(formula_counts):
			para_formula.append(marking_numbers_formula(str(soup('span',class_='math-tex')[i])))
			soup('span',class_='math-tex')[i].string=''
	if formula_counts==1 and str(soup.text)=='':
		return marking_numbers_formula(strings)
	para_text=marking_numbers_text(str(soup.p))
	pattern = re.compile(r'(\d+\.?\d*|<span class="math-tex"></span>)')
	l=re.findall(pattern,str(soup.p))

	for i in range(len(l)):		
		if l[i]=='<span class="math-tex"></span>':
			#print(para_formula[formula_counts+1])
			#print('formula_counts',formula_counts)
			for j in range(len(para_formula[para_formula_counts][1])):
				before = '{0['+str(j)+']}'
				temp = '{0['+str(k)+']}'
				if para_formula[para_formula_counts][0].count(temp)==1:
					para_formula[para_formula_counts][0]=para_formula[para_formula_counts][0].replace(before,temp)
					
				else:
					para_formula[para_formula_counts][0]=para_formula[para_formula_counts][0][::-1]
					before=before[::-1]
					temp=temp[::-1]
					para_formula[para_formula_counts][0]=para_formula[para_formula_counts][0].replace(before,temp,1)
					para_formula[para_formula_counts][0]=para_formula[para_formula_counts][0][::-1]
				para.append(para_formula[para_formula_counts][1][j])
				k=k+1
			para_formula_counts=para_formula_counts+1
		else:
			before = '{0['+str(para_text_counts)+']}'
			temp = '{0['+str(k)+']}'
			para_text[0]=para_text[0].replace(before,temp)
			para.append(para_text[1][para_text_counts])
			para_text_counts=para_text_counts+1
			k=k+1
	soup=BeautifulSoup(str(para_text))
	for i in range(formula_counts):
		soup('span',class_='math-tex')[i].string=BeautifulSoup(para_formula[i][0]).span.string
	return [str(soup.p),para]

	

def paste_question(question_id):
	template=Question_template.objects.get(question_upload_id=question_id).template
	paras=Question_para.objects.filter(question_upload_id=question_id)
	k=random.randint(0,paras.count()-1)
	l=paras[k].para_chains
	for i in range(len(l)):
		template=template.replace('{0['+str(i)+']}',str(l[i]))
	print('l:')
	print(template)
	return template

def limit_knowledge_point(self):
	return 'a'


class Question_upload(models.Model):
	#grade = models.ForeignKey('Knowledge_point_grade',on_delete=models.CASCADE,default=111)

	#point = models.ForeignKey('Knowledge_point',on_delete=models.CASCADE,limit_choices_to=limit_knowledge_point)
	primary_second_grade='p2'
	primary_third_grade='p3'
	primary_forth_grade='p4'
	primary_fifth_grade='p5'
	primary_sixth_grade='p6'
	GRADE_CHOICE= (
			(primary_second_grade,'小二'),
			(primary_third_grade,'小三'),
			(primary_second_grade,'小四'),
			(primary_second_grade,'小五'),
			(primary_second_grade,'小六'),
		)
	years_of_question=models.CharField(
		'学年',
		max_length=2,
        choices=GRADE_CHOICE,
        default=primary_fifth_grade,)

	question = models.CharField('質問',blank=True,max_length=200)
	#tags = models.CharField(default='',max_length=200)

	def __str__(self):
		return self.question

	def has_formula(self):
		t = False
		for i in self.hypothesis_set.all():
			if with_formula(i.hypothesis)==True:
				t = True
		return t

	def has_img(self):
		t = False
		for i in self.hypothesis_set.all():
			if with_image(i.hypothesis)==True:
				t = True
		return t

	def has_table(self):
		t = False
		for i in self.hypothesis_set.all():
			if with_table(i.hypothesis)==True:
				t = True
		return t

	#boolean icon for admin list page.
	has_formula.boolean = True
	has_table.boolean = True
	has_img.boolean = True

	def all_hypothesis(self):
		t=''
		for i in self.hypothesis_set.all():
			t=t+i.hypothesis
		return t

	def save(self, *args, **kwargs):
		super(Question_upload, self).save(*args, **kwargs)
		t=self.all_hypothesis()
		t=t+'<br><p>'+self.question+'</p>'
		for i in self.question_template_set.all():
			i.delete()
		self.question_template_set.create(hardness=1, edited=False, template=t)


class Hypothesis(models.Model):
	question_upload = models.ForeignKey('Question_upload',on_delete=models.CASCADE)
	hypothesis = RichTextUploadingField(
		'条件',
		blank=True,
		#extra_plugins = ['mathjax',],s
	)

	def __str__(self):
		txt = BeautifulSoup(self.hypothesis)
		return txt.get_text()
	def save(self, *args, **kwargs):
		#self.hypothesis=prettify(self.hypothesis)
		super(Hypothesis, self).save(*args, **kwargs)
		t= ''
		for i in self.question_upload.question_template_set.all():
			i.delete()
		make_template(self.question_upload_id)
		#self.question_upload.question_template_set.create(hardness=1, edited=False, template=t)

class Question_para(models.Model):
	question_upload = models.ForeignKey('Question_upload',on_delete=models.CASCADE)
	#para_chains = RichTextUploadingField(config_name='ttt')
	para_chains =ListCharField(base_field=models.CharField(max_length=10),max_length=100)
	ans =models.TextField()
	def __str__(self):
		l= len(self.para_chains)
		s= '変数入力規則：'
		for i in range(l):
			s=s+'args({index})'.format(index=i)
		return '"'+self.question_upload.question+'"||'+s
	def test(self):
		s=Question_template.objects.get(question_upload_id=self.question_upload_id).template
		l=self.para_chains
		for i in range(len(l)):
			s=s.replace('{0['+str(i)+']}','args('+str(i)+')')

		return str(BeautifulSoup(s).body)



class Question_template(models.Model):
	question_upload = models.ForeignKey('Question_upload',on_delete=models.CASCADE)
	hardness = models.DecimalField(default=1.00, max_digits=5, decimal_places=2)
	edited = models.BooleanField(default=False)
	template = models.TextField()
'''	
	def save(self, *args, **kwargs):
		for i in self.question_upload.question_edit_set.all():
			i.delete()
		self.question_upload.question_edit_set.create(para_chains=self.template)
		super(Question_template,self).save(*args, **kwargs)
'''


class Tags_list(models.Model):
	question_upload = models.ForeignKey('Question_upload',on_delete=models.CASCADE)
	values =models.CharField(default='',max_length=200)
class Knowledge_point_list(models.Model):
	points=models.CharField(max_length=200,default='数学')
	grade=models.CharField(max_length=2,default='小学')

class Knowledge_point(models.Model):
	question_upload = models.ForeignKey('Question_upload',on_delete=models.CASCADE)
	points_with_question = models.CharField(max_length=100,default='not defined')



