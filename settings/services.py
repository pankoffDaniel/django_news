from settings.models import SiteMainSettingsModel, SiteSocialNetModel


def get_site_mail_settings():
    """Returns model of site main settings."""
    return SiteMainSettingsModel.objects.first()


def get_site_social_net_list():
    """Returns list of site social net."""
    return SiteSocialNetModel.objects.all()
