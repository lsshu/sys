from time import sleep

from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from ranking.methods import get_proxies, get_bd_computer_ranking, get_bd_mobile_ranking
from ranking.models import RankingVocabularies, RankingRegions
from ranking import tasks


def test(request):
    # 词汇
    vocabularies = RankingVocabularies.objects.all()
    # 代理地区
    regions = RankingRegions.objects.all()
    for region in regions:
        for vocabulary in vocabularies:
            datum = dict()
            datum['region'] = {"id": region.id, "name": region.name}
            datum['vocabulary'] = {"id": vocabulary.id, "words": vocabulary.words}
            tasks.ranking_task.delay(**datum)
    return HttpResponse('ok')
