import yaml


class SiteContext:
    def __init__(self):
        with open('site-config.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    @property
    def site_title(self):
        return self.config['SITE_TITLE']


site_context = SiteContext()


def inject_global_context():
    return site_context.config
