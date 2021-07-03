from django.http import HttpResponse

from ranking.models import RankingVocabularies, RankingRegions
from ranking.tasks import task_ranking


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
            task_ranking.delay(**datum)
    return HttpResponse('ok')
