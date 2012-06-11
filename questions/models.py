from django.db import models
import datetime

class Question(models.Model):
	question = models.CharField(max_length=200)
	created = models.DateTimeField(default=datetime.datetime.now())
	standing = models.IntegerField(default=0)

class Vote(models.Model):
	def save(self, *args, **kwargs):
		''' On save, update standing '''
		question = Question.objects.get(pk=self.question.id)
		agrees = Vote.objects.filter(question=question, vote='1').count()
		disagrees = Vote.objects.filter(question=question, vote='2').count()
		question.standing = agrees - disagrees
		question.save()
		super(Vote, self).save(*args, **kwargs)
		
	question = models.ForeignKey(Question)
	vote = models.IntegerField(default='0')