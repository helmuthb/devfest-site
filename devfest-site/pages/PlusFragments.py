try:
  import settings_local as settings
except:
  import settings
from lib.view import FrontendPage
from lib.model import Event
from lib.cobjects import CEvent, CGPlusFeed
from datetime import datetime
import urllib
import json
import sys

# get the Gplus stream for an event
class PlusStreamFragment(FrontendPage):
  def show(self, event_id):
    event = CEvent(event_id).get()
    response = CGPlusFeed(event.hashtag).get()
    self.template = 'gplusstream'
    self.values["response"] = response

# get the Gplus stream globally
class GlobalPlusStreamFragment(FrontendPage):
  def show(self):
    response = CGPlusFeed(settings.GLOBAL_HASHTAG).get()
    self.template = 'gplusstream'
    self.values["response"] = response
    sys.stderr.write("%s\n" % str(response['items']))
