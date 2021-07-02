from django.db import models

# Create your models here.
from base.models import DefaultModel


class OperatingMarket(DefaultModel):
    """
    运营市场
    """
    name = models.CharField(max_length=50, null=False, verbose_name='市场名称', unique=True)
    remarks = models.CharField(max_length=150, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'records_operating_markets'
        verbose_name = "运营市场"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class MarketBrands(DefaultModel):
    """
    市场品牌
    """
    name = models.CharField(max_length=50, null=False, verbose_name='品牌名称', unique=True)
    remarks = models.CharField(max_length=150, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'records_market_brands'
        verbose_name = "市场品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PromotionChannels(DefaultModel):
    """
    推广渠道
    """
    name = models.CharField(max_length=50, null=False, verbose_name='渠道名称', unique=True)
    remarks = models.CharField(max_length=150, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'records_promotion_channels'
        verbose_name = "推广渠道"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AccountAgents(DefaultModel):
    """
    账户代理
    """
    name = models.CharField(max_length=50, null=False, verbose_name='代理名称', unique=True)
    contact_user = models.CharField(max_length=10, null=False, verbose_name='联系人')
    contact_phone = models.CharField(max_length=15, null=False, verbose_name='联系电话')
    remarks = models.CharField(max_length=150, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'records_account_agents'
        verbose_name = "账户代理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PromotionAccounts(DefaultModel):
    """
    推广账户
    """
    account_agents = models.ForeignKey(AccountAgents, on_delete=models.CASCADE, null=False, blank=False,
                                       verbose_name="账户代理")
    promotion_channel = models.ForeignKey(PromotionChannels, on_delete=models.CASCADE, null=False, blank=False,
                                          verbose_name="推广渠道")
    operating_market = models.ForeignKey(OperatingMarket, on_delete=models.CASCADE, null=False, blank=False,
                                         verbose_name="运营市场")
    market_brand = models.ForeignKey(MarketBrands, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name="市场品牌")
    name = models.CharField(max_length=50, null=False, verbose_name='账户名称', unique=True)
    password = models.CharField(max_length=50, null=False, verbose_name='账户密码')
    account_contact = models.CharField(max_length=10, null=False, verbose_name='账户负责')
    account_phone = models.CharField(max_length=15, null=False, verbose_name='账户手机')
    account_rebate = models.DecimalField(max_length=15, max_digits=5, decimal_places=2, null=False, verbose_name='账户返点',
                                         help_text="如：0.40")
    account_domain = models.CharField(max_length=50, null=False, verbose_name='账户域名', help_text="如：www.baidu.com")
    account_status = models.CharField(max_length=15, choices=[('use', '使用中'), ('paused', '已暂停'), ('rejected', '被拒户'),
                                                              ('returning', '退户中'), ('returned', '已退户')], null=False,
                                      default="use", verbose_name='账户状态')
    verify_phone = models.CharField(max_length=15, null=False, verbose_name='验证手机')
    remarks = models.CharField(max_length=150, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'records_promotion_accounts'
        verbose_name = "推广账户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AccountCopyrights(DefaultModel):
    """
    账户版权
    """
    promotion_account = models.OneToOneField(PromotionAccounts, on_delete=models.CASCADE, null=False, blank=False,
                                             verbose_name="推广账户")
    copyright_company = models.CharField(max_length=50, null=False, verbose_name='版权公司')
    copyright_record = models.CharField(max_length=20, null=False, verbose_name='备案信息')
    copyright_address = models.CharField(max_length=50, null=False, verbose_name='备案地址')
    copyright_telephone = models.CharField(max_length=15, null=False, verbose_name='备案电话')
    copyright_logo = models.CharField(max_length=120, null=False, verbose_name='公司logo')

    class Meta:
        db_table = 'records_account_copyrights'
        verbose_name = "账户版权"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.copyright_company
