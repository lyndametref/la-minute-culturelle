from nikola.plugin_categories import Command
from nikola.post import get_meta
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


# You have to inherit Command for this to be a
# command plugin:

class CommandServe(Command):
    """Announce today's post on various services using webhooks"""

    name = "announce"
    doc_usage = "[options]"
    doc_purpose = "announce today's post on various services using webhooks"

    cmd_options = (
        {
            'name': 'discord-webhook-url',
            'short': 'u',
            'long': 'discord-webhook-url',
            'type': str,
            'default': '',
            'help': 'Webhood of discord channel',
        },
    )

    def _execute(self, options, args):
        """Announce today's post on various services using webhooks"""
        self.site.scan_posts()
        today_post = [x for x in self.site.timeline if x.date.date() == datetime.today().date()]
        meta = get_meta(today_post[0], 'fr')
        content = list([today_post[0].title()])
        content.append(today_post[0].description())
        [content.append(x) for x in meta[0]['references']]
        content_str = "\n".join(content)

        webhook = DiscordWebhook(url=options['discord-webhook-url'], content=content_str)
        response = webhook.execute()
        return 0