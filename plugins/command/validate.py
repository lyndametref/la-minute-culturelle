from nikola.plugin_categories import Command
from nikola.post import get_meta
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


# You have to inherit Command for this to be a
# command plugin:

class CommandServe(Command):
    """Announce today's post on various services using webhooks"""

    name = "validate"
    doc_usage = "[options]"
    doc_purpose = "Validate that all needed fields are filled"

    cmd_options = (
        {
            'name': 'validate',
            'short': 'v',
            'long': 'validate',
            'type': str,
            'default': '',
            'help': 'Validate that all needed fields are filled',
        },
    )

    def _execute(self, options, args):
        """Validate that all needed fields are filled"""
        self.site.scan_posts()

        def validate(post):
            meta = get_meta(post, 'fr')
            has_reference = len(meta[0]['references']) > 0
            has_description = len(post.description()) > 0
            return has_reference & has_description

        [print(validate(x), x.title()) for x in self.site.timeline if x.date.date() >= datetime.today().date()]

        return 0
