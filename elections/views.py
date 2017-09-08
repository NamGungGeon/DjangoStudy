from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from .models import Candidate

from .models import Candidate, Poll, Choice
from django.db.models import Sum
import datetime
# Create your views here.
def index(request):
    # Solution 1
    """
    candidates=Candidate.objects.all()
    str=''
    for candidate in candidates:
        str+="<p>"
        str+="{} 기호 {}번 {}".format(candidate.name, candidate.party_number, candidate.area)
        str+=candidate.introduction+"</p>"
    return HttpResponse(str)
    """
    
    # Solution 2
    # 특정 파일을 불러와 표시하는 방법
    candidates=Candidate.objects.all()
    context= {"candidates": candidates}
    return render(request, "elections/index.html", context)

def candidates(request, name):
    # try~except 없이 한번에 Http404와 객체처리를 동시에 할 수도 있다.
    # candidate= get_object_or_404(Candidate, name=name)
    print("###################", name)
    try:
        candidate= Candidate.objects.get(name= name)
    except:
        #return HttpResponseNotFound("없는 페이지 입니다.")
        raise Http404
    return HttpResponse(candidate.name)

def areas(request, area):
    today= datetime.datetime.now()
    #lte= less than equal
    #gte= grater than equal
    try:
        poll=Poll.objects.get(area=area, start_date__lte= today, end_date__gte=today)
        candidates=Candidate.objects.filter(area= area)
    except:
        poll= None
        candidates= None

    context={
        "candidates": candidates,
        "area": area,
        "poll": poll
        }
    return render(request, "elections/area.html", context)

def polls(request, poll_id):
    poll = Poll.objects.get(area = poll_id)
    
    selection = request.POST['choice']

    try: 
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()

    print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ", choice.votes)
    return HttpResponseRedirect("/elections/areas/{}/results".format(poll.area))

def results(request, area):
    candidates= Candidate.objects.filter(area= area)
    polls= Poll.objects.filter(area= area)

    poll_result=[]
    for poll in polls:
        result={}
        result['start_date']= poll.start_date
        result['end_date']= poll.end_date
        total_votes= Choice.objects.filter(poll_id= poll.id).aggregate(Sum('votes'))
        
        result["total_votes"]= total_votes["votes__sum"]
        rates=[]
        for candidate in candidates:
            try:
                choice= Choice.objects.get(poll_id= poll.id, candidate_id= candidate.id)
                
                rates.append(round(choice.votes*100/ result["total_votes"], 1))
            except: 
                rates.append(0)
        result["rates"]= rates
        poll_result.append(result)


    context={
        "candidates": candidates,
        "area": area,
        "poll_results": poll_result
    }
    return render(request, "elections/result.html", context)