from django.contrib import admin

# Register your models here.
from records.models import OperatingMarket, MarketBrands, PromotionChannels, AccountAgents, PromotionAccounts, \
    AccountCopyrights


@admin.register(OperatingMarket)
class OperatingMarketAdmin(admin.ModelAdmin):
    """
    运营市场
    """
    fields = ('name', 'remarks')
    list_display = fields + ('updated_at',)
    list_display_links = ('name',)
    # list_editable = ('remarks',)
    # empty_value_display = '-empty-'


@admin.register(MarketBrands)
class MarketBrandsAdmin(admin.ModelAdmin):
    """
    市场品牌
    """
    fields = ('name', 'remarks')
    list_display = fields + ('updated_at',)
    list_display_links = ('name',)
    # list_editable = ('remarks',)
    # empty_value_display = '-empty-'


@admin.register(PromotionChannels)
class PromotionChannelsAdmin(admin.ModelAdmin):
    """
    推广渠道
    """
    fields = ('name', 'remarks')
    list_display = fields + ('updated_at',)
    list_display_links = ('name',)
    # list_editable = ('remarks',)
    # empty_value_display = '-empty-'


@admin.register(AccountAgents)
class AccountAgentsAdmin(admin.ModelAdmin):
    """
    账户代理
    """
    fields = ('name', 'contact_user', 'contact_phone', 'remarks')
    list_display = fields + ('updated_at',)
    list_display_links = ('name',)
    # list_editable = ('remarks',)
    # empty_value_display = '-empty-'


@admin.register(PromotionAccounts)
class PromotionAccountsAdmin(admin.ModelAdmin):
    """
    推广账户
    """
    fieldsets = (
        ("类目设置", {
            'fields': (('promotion_channel', 'operating_market', 'market_brand', 'account_agents',),)
        }),
        ("基本设置", {
            'fields': (
                ('name', 'password',), ('account_contact', 'account_phone',), ('account_rebate', 'account_domain',),
                'verify_phone', 'account_status', 'remarks',)
        }),
    )
    list_display = (
        'name', 'promotion_channel', 'operating_market', 'market_brand', 'account_agents', 'account_contact',
        'account_rebate', 'account_domain', 'account_status', 'remarks', 'updated_at',)
    list_display_links = ('name',)

    class AccountCopyrightsInline(admin.StackedInline):
        """
        账户版权
        """
        model = AccountCopyrights
        fields = (
            'copyright_company', 'copyright_record', 'copyright_address', 'copyright_telephone', 'copyright_logo',)

    inlines = (AccountCopyrightsInline,)


from django.apps import apps
from django.utils.text import capfirst


def find_app_index(app_label):
    app = apps.get_app_config(app_label)
    main_menu_index = getattr(app, 'main_menu_index', 9999)
    return main_menu_index


def find_model_index(name):
    count = 0
    for model, model_admin in admin.site._registry.items():
        if capfirst(model._meta.verbose_name_plural) == name:
            return count
        else:
            count -= 1
    return count


def index_decorator(func):
    def inner(*args, **kwargs):
        templateresponse = func(*args, **kwargs)
        app_list = templateresponse.context_data['app_list']
        app_list.sort(key=lambda r: find_app_index(r['app_label']))
        for app in app_list:
            app['models'].sort(key=lambda x: find_model_index(x['name']))
        return templateresponse

    return inner


admin.site.index = index_decorator(admin.site.index)
admin.site.app_index = index_decorator(admin.site.app_index)

admin.site.site_title = "System Admin-Lsshu"
admin.site.site_header = "System"
admin.site.index_title = "System Admin"
