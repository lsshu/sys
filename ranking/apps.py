from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RankingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ranking'
    verbose_name = _("排行统计")
    main_menu_index = 1
