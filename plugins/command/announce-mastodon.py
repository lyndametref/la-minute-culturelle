from nikola.plugin_categories import Command
from nikola.post import get_meta
from datetime import datetime
from mastodon import Mastodon


# You have to inherit Command for this to be a
# command plugin:

class CommandServe(Command):
    """Announce today's post on various services using webhooks"""

    name = "announce-mastodon"
    doc_usage = "[options]"
    doc_purpose = "Announce today's post on Mastodon"

    cmd_options = (
        {
            'name': 'mastodon-token',
            'short': 't',
            'long': 'mastodon-token',
            'type': str,
            'default': '',
            'help': 'Token for mastodon node',
        },
        {
            'name': 'mastodon-node',
            'short': 'n',
            'long': 'mastodon-node',
            'type': str,
            'default': '',
            'help': 'Mastodon node',
        },
    )

    def _execute(self, options, args):
        """Announce today's post on Mastodon"""
        self.site.scan_posts()
        today_post = [x for x in self.site.timeline if x.date.date() == datetime.today().date()]
        if len(today_post) > 0:
            meta = get_meta(today_post[0], 'fr')
            content = list([today_post[0].title()])
            content.append(today_post[0].description())
            [content.append(x) for x in meta[0]['references']]
            content.insert(0, '#laminuteculturelle')
            content.append('archives: https://www.mad-scientists.net/la-minute-culturelle/')
            content_str = "\n".join(content)

            mastodon = Mastodon(
                access_token=options['mastodon-token'],
                api_base_url=options['mastodon-node']
            )
            mastodon.toot(content_str)

        return 0
