from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecordsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'records'
    verbose_name = _("数据统计")
    main_menu_index = 2
