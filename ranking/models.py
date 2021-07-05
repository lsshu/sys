from django.db import models

# Create your models here.
from base.models import DefaultModel
from records.models import OperatingMarket, PromotionAccounts


class RankingParts(DefaultModel):
    """
    排名 词类
    """
    name = models.CharField(max_length=50, null=False, verbose_name='词类名称', unique=True)
    remarks = models.CharField(max_length=150, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'ranking_parts'
        verbose_name = "排名词类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class RankingVocabularies(DefaultModel):
    """
    排名词汇
    """
    ranking_part = models.ForeignKey(RankingParts, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name="排名词类")
    operating_market = models.ForeignKey(OperatingMarket, on_delete=models.CASCADE, null=False, blank=False,
                                         verbose_name="运营市场")
    words = models.CharField(max_length=100, null=False, verbose_name='排名词汇', unique=True)
    remarks = models.CharField(max_length=150, null=True, blank=True, verbose_name='备注')
    is_batch = models.CharField(max_length=5, choices=[('yes', '批量'), ('no', '不批量')], null=False,
                                default="no", verbose_name='是否批量', help_text="如果是批量 词类、市场、词汇、备注将不作生效")
    batch = models.TextField(null=True, blank=True, verbose_name='批量内容', help_text="格式：免税类	三亚	三亚免税店攻略")

    def save(self, *args, **kwargs):
        if self.is_batch == "yes":
            """批量操作"""
            try:
                batches = str(self.batch).split('\r\n')
                for batch in batches:
                    part_name, market_name, words = str(batch).split('\t')
                    part, is_part = RankingParts.objects.get_or_create(name=part_name)
                    market, is_market = OperatingMarket.objects.get_or_create(name=market_name)
                    try:
                        RankingVocabularies.objects.update_or_create(ranking_part=part, operating_market=market,
                                                                     words=words)
                    except:
                        pass
            except:
                pass
            return
        else:
            super().save(*args, **kwargs)

    class Meta:
        db_table = 'ranking_vocabularies'
        verbose_name = "排名词汇"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.words


class RankingRegions(DefaultModel):
    """
    代理地区
    """
    name = models.CharField(max_length=50, null=False, verbose_name='地区名称', unique=True)
    remarks = models.CharField(max_length=150, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'ranking_regions'
        verbose_name = "代理地区"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class RankingProxies(DefaultModel):
    """
    代理记录
    """
    proxy = models.CharField(max_length=10, choices=[('kdlapi', '快代理'), ], null=False,
                             default="kdlapi", verbose_name='代理公司')
    username = models.CharField(max_length=20, null=True, blank=True, verbose_name="代理账号")
    password = models.CharField(max_length=40, null=True, blank=True, verbose_name="代理密码")
    proxies = models.CharField(max_length=25, null=False, blank=False, verbose_name='地区代理')
    ranking_region = models.ForeignKey(RankingRegions, on_delete=models.SET_NULL, null=True, blank=False,
                                       verbose_name="代理地区")
    code = models.IntegerField(null=True, default=0, blank=True, verbose_name="返回码")
    order_count = models.IntegerField(null=True, default=0, blank=True, verbose_name="剩余数")
    dedup_count = models.IntegerField(choices=[(0, '否'), (1, '是')], null=True, default=0, blank=True,
                                      verbose_name="是否去重")
    area = models.CharField(max_length=50, null=False, verbose_name='地区详情')
    sep = models.IntegerField(null=False, default=0, verbose_name='时效')
    expires_time = models.DateTimeField(null=False, verbose_name='失效时间')

    class Meta:
        db_table = 'ranking_proxies'
        verbose_name = "代理记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.proxies


class RankingRecords(DefaultModel):
    """
    排名记录
    """
    ranking_vocabularie = models.ForeignKey(RankingVocabularies, on_delete=models.SET_NULL, null=True, blank=False,
                                            verbose_name="排名词汇")
    ranking_region = models.ForeignKey(RankingRegions, on_delete=models.SET_NULL, null=True, blank=False,
                                       verbose_name="代理地区")
    proxies = models.ForeignKey(RankingProxies, on_delete=models.SET_NULL, null=True, blank=False, verbose_name='地区代理')

    ad_device = models.CharField(max_length=10, choices=[('mobile', '移动'), ('computer', '电脑')], null=False, blank=False,
                                 default="computer", verbose_name='搜索设备')
    ad_position = models.CharField(max_length=6,
                                   choices=[('top', '顶部'), ('right', '右'), ('bottom', '底部'), ('left', '左')], null=False,
                                   blank=False, default="left",
                                   verbose_name='广告位置')
    ad_id = models.IntegerField(null=True, blank=False, verbose_name='广告排名')
    ad_title = models.CharField(max_length=80, null=False, blank=False, verbose_name='广告标题')
    ad_copyright = models.CharField(max_length=50, null=False, blank=False, verbose_name='广告版权')
    is_self = models.CharField(max_length=5, choices=[('yes', '是'), ('no', '否')], null=False,
                               default="no", verbose_name='是否自己', help_text="是不是自己公司的账户")
    promotion_account = models.ForeignKey(PromotionAccounts, on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name="推广账户")

    class Meta:
        db_table = 'ranking_records'
        verbose_name = "排名记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ad_title
