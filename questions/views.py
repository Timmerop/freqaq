from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from questions.models import *
import simplejson as json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def index(request):
    
    query = request.GET.get('q', '')
    qset = ( Q(question__icontains=query))
    sort = request.GET.get('sort', '')
    

    print "sort", sort
    if sort:
        if sort == 'a':
            questions = Question.objects.filter(standing__gt=-5).order_by('question')
        if sort == 'ab':
            questions = Question.objects.filter(standing__gt=-5).order_by('-question')
        if sort == 'd':
            questions = Question.objects.filter(standing__gt=-5).order_by('-created')
        if sort == 'db':
            questions = Question.objects.filter(standing__gt=-5).order_by('created')
        if sort == 'v':
            questions = Question.objects.filter(standing__gt=-5).order_by('-standing', '-created')
        if sort == 'vb':
            questions = Question.objects.filter(standing__gt=-5).order_by('standing', 'created')
    else:
        questions = Question.objects.filter(qset).filter(standing__gt=-5).order_by('-standing', '-created')
        sort = 'v'

    paginator = Paginator(questions, 100)

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
        print paginator.num_pages, 'hi'
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    except TypeError:
        questions = paginator.page(paginator.num_pages)

    template_args = {
        'questions' : questions,
        'query' : query,
        'sort': sort
    }
    return render_to_response('faqs.html', template_args, context_instance=RequestContext(request))

def add_question(request):
    response = {}
    print 'here'
    if request.POST:
        args = request.POST
        try:
            question = Question( question = args['question'])
            question.save()
            q = {}
            q['question'] = question.question
            q['id'] = question.id
            response = {'success': True, 'question' :q}
        except Exception as e:
            print "Could not add question", e
            response = {"success": False }
    return HttpResponse(json.dumps(response), mimetype='application/json')

def vote(request, id, vote):  
    user = request.session.session_key
    if not user:
        request.session.save()
        user = request.session.session_key

    question = Question.objects.get(pk=id)
    print vote
    
    response = {}
    try:
        
        new_vote, created = Vote.objects.get_or_create(question=question, visitor=user,
        defaults={'vote': vote} )
        if created:
            print "vote created", new_vote.vote 
        else:
            print "vote exists, it was", new_vote.vote
            new_vote.vote = vote
            print "new vote is", new_vote.vote
        new_vote.save()
        
        response = {"success": True, 'standing' : question.standing }
        
    except Exception as e:
        print "could not add vote", e
        response = {'success': False}

    return HttpResponse(json.dumps(response), mimetype='application/json')
