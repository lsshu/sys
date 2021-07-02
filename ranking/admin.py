from django.contrib import admin

# Register your models here.
from ranking.models import RankingParts, RankingVocabularies, RankingRegions, RankingRecords, RankingProxies


@admin.register(RankingRegions)
class RankingRegionsAdmin(admin.ModelAdmin):
    """
    代理地区
    """
    fields = ('name', 'remarks')
    list_display = fields + ('updated_at',)
    list_display_links = ('name',)


@admin.register(RankingProxies)
class RankingProxiesAdmin(admin.ModelAdmin):
    """
    代理记录
    """
    fields = (
        'proxy', 'username', 'password', 'ranking_region', 'proxies', 'code', 'order_count', 'dedup_count', 'area',
        'sep',
        'expires_time')
    list_display = fields + ('updated_at',)
    list_display_links = ('proxies',)
    ordering = ('-expires_time',)


@admin.register(RankingParts)
class RankingPartsAdmin(admin.ModelAdmin):
    """
    排名 词类
    """
    fields = ('name', 'remarks')
    list_display = fields + ('updated_at',)
    list_display_links = ('name',)


@admin.register(RankingVocabularies)
class RankingVocabulariesAdmin(admin.ModelAdmin):
    """
    排名词汇
    """
    default = ('ranking_part', 'operating_market', 'words', 'remarks')
    fields = default + ('is_batch', 'batch')
    list_display = default + ('updated_at',)
    list_display_links = ('words',)
    list_per_page = 20


@admin.register(RankingRecords)
class RankingRecordsAdmin(admin.ModelAdmin):
    """
    排名记录
    """
    fields = (
        'ranking_vocabularie', 'ranking_region', 'proxies', 'ad_device', 'ad_position', 'ad_id', 'ad_title',
        'ad_copyright', 'is_self', 'promotion_account')
    list_display = fields + ('updated_at',)
    # list_display_links = ('is_self',)
    ordering = ["-created_at"]
