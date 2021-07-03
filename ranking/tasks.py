from celery import shared_task

from ranking.methods import get_bd_computer_ranking, get_proxies, get_bd_mobile_ranking
from ranking.models import RankingRecords, RankingVocabularies, RankingRegions


@shared_task
def task_all_ranking():
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


@shared_task
def task_ranking(**kwargs):
    """
    全部 排名 task
    """
    region = kwargs.get('region')
    vocabulary = kwargs.get('vocabulary')
    proxy, proxies = get_proxies(area=region['name'])
    if not proxy:
        proxy = None
        proxies = {}

    ranking_response, error = get_bd_computer_ranking(keywords=vocabulary['words'], proxies=proxies)
    if ranking_response:
        for ranking_data in ranking_response:
            record_data = dict()
            record_data['ranking_vocabularie'] = RankingVocabularies.objects.get(pk=vocabulary['id'])
            record_data['ranking_region'] = RankingRegions.objects.get(pk=region['id'])
            record_data['proxies'] = proxy
            record_data['ad_device'] = ranking_data['device']
            record_data['ad_position'] = ranking_data['position']
            record_data['ad_id'] = ranking_data['ad_id'] if ranking_data['ad_id'] else 0
            record_data['ad_title'] = ranking_data['title']
            record_data['ad_copyright'] = ranking_data['domain']
            RankingRecords.objects.create(**record_data)
    else:
        return error

    ranking_response, error = get_bd_mobile_ranking(keywords=vocabulary['words'], proxies=proxies)
    if ranking_response:
        for ranking_data in ranking_response:
            record_data = dict()
            record_data['ranking_vocabularie'] = RankingVocabularies.objects.get(pk=vocabulary['id'])
            record_data['ranking_region'] = RankingRegions.objects.get(pk=region['id'])
            record_data['proxies'] = proxy
            record_data['ad_device'] = ranking_data['device']
            record_data['ad_position'] = ranking_data['position']
            record_data['ad_id'] = ranking_data['ad_id'] if ranking_data['ad_id'] else 0
            record_data['ad_title'] = ranking_data['title']
            record_data['ad_copyright'] = ranking_data['domain']
            RankingRecords.objects.create(**record_data)
    else:
        return error
