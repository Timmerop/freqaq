from django.db import models
import datetime

class Question(models.Model):
    question = models.CharField(max_length=200)
    created = models.DateTimeField(default=datetime.datetime.now())
    standing = models.IntegerField(default=0)

    def __str__(self):
        return self.question

    def save(self, *args, **kwargs):
        ups = Vote.objects.filter(question=self, vote='u').count()
        downs = Vote.objects.filter(question=self, vote='d').count()
        self.standing = (ups - downs)
        super(Question, self).save(*args, **kwargs)
        print "just saved", self.question, "standing is", self.standing

class Vote(models.Model):

    VOTE_CHOICES = (
        (u'u', u'up'),
        (u'd', u'down'),
        (u'n', u'neither'),
    )

    question = models.ForeignKey(Question)
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES, default='n')
    visitor = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        ''' On save, update standing '''
        super(Vote, self).save(*args, **kwargs)
        self.question.save()

    def __str__(self):
        return self.question.question