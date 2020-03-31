from nikola.plugin_categories import Command
from datetime import datetime
from nikola.post import get_meta


# You have to inherit Command for this to be a
# command plugin:

class CommandServe(Command):
    """Announce today's post on various services using webhooks"""

    name = "list-future-posts"
    doc_usage = "[options]"
    doc_purpose = "List all future posts' address (local server)"

    def _execute(self, options, args):
        """List all posts' address"""
        self.site.scan_posts()

        def validate(post):
            meta = get_meta(post, 'fr')
            has_reference = len(meta[0]['references']) > 0
            has_description = len(post.description()) > 0
            return has_reference & has_description

        [print(validate(x), " ",
               x.date,
               " http://127.0.0.1:8000", x.permalink(), sep='')
         for x in self.site.timeline
         if x.date.date() >= datetime.today().date()]

        return 0
