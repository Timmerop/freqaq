from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from questions.models import *
import simplejson as json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def index(request):
    request.session['name'] = 'Fred'
    questions = Question.objects.order_by('-standing', 'created')

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
            response = {'success': True}
        except Exception as e:
            print "Could not add question", e
            response = {"success": False }
    return HttpResponse(json.dumps(response), mimetype='application/json')

def vote(request, id, vote):
    print vote
    response = {}
    ses_call = 'question_'+ id
    print request.session[ ses_call ]
    if request.session[ses_call] == vote:
        response = {'success': False}
    else:
        new_vote = Vote(
            question = Question.objects.get(pk=id),
            vote = vote
        )
        new_vote.save()
        question = Question.objects.get(pk=id)
        request.session[ses_call] = vote
        print request.session[ ses_call ], request.session[ 'name' ]
        response = {"success": True, 'standing' : question.standing }
    return HttpResponse(json.dumps(response), mimetype='application/json')
