from django.utils import simplejson as json
from createsend import CreateSendBase
from utils import json_to_py

class Campaign(CreateSendBase):
  """Represents a campaign and provides associated funtionality."""

  def __init__(self, campaign_id=None):
    self.campaign_id = campaign_id
    super(Campaign, self).__init__()

  def create(self, client_id, subject, name, from_name, from_email, reply_to, html_url,
    text_url, list_ids, segment_ids):
    """Creates a new campaign for a client."""
    body = {
      "Subject": subject,
      "Name": name,
      "FromName": from_name,
      "FromEmail": from_email,
      "ReplyTo": reply_to,
      "HtmlUrl": html_url,
      "TextUrl": text_url,
      "ListIDs": list_ids,
      "SegmentIDs": segment_ids }
    response = self._post("/campaigns/%s.json" % client_id, json.dumps(body))
    return json_to_py(response)

  def send_preview(self, recipients, personalize="fallback"):
    """Sends a preview of this campaign."""
    body = {
      "PreviewRecipients": [ recipients ] if isinstance(recipients, str) else recipients,
      "Personalize": personalize }
    response = self._post(self.uri_for("sendpreview"), json.dumps(body))

  def send(self, confirmation_email, send_date="immediately"):
    """Sends this campaign."""
    body = {
      "ConfirmationEmail": confirmation_email,
      "SendDate": send_date }
    response = self._post(self.uri_for("send"), json.dumps(body))

  def delete(self):
    """Deletes this campaign."""
    response = self._delete("/campaigns/%s.json" % self.campaign_id)

  def summary(self):
    """Gets a summary of this campaign"""
    response = self._get(self.uri_for("summary"))
    return json_to_py(response)

  def lists_and_segments(self):
    """Retrieves the lists and segments to which this campaaign will be (or was) sent."""
    response = self._get(self.uri_for("listsandsegments"))
    return json_to_py(response)

  def recipients(self, page=1, page_size=1000, order_field="email", order_direction="asc"):
    """Retrieves the recipients of this campaign."""
    params = { 
      "page": page,
      "pagesize": page_size,
      "orderfield": order_field,
      "orderdirection": order_direction }
    response = self._get(self.uri_for("recipients"), params=params)
    return json_to_py(response)

  def opens(self, date, page=1, page_size=1000, order_field="date", order_direction="asc"):
    """Retrieves the opens for this campaign."""
    params = { 
      "date": date,
      "page": page,
      "pagesize": page_size,
      "orderfield": order_field,
      "orderdirection": order_direction }
    response = self._get(self.uri_for("opens"), params=params)
    return json_to_py(response)

  def clicks(self, date, page=1, page_size=1000, order_field="date", order_direction="asc"):
    """Retrieves the subscriber clicks for this campaign."""
    params = { 
      "date": date,
      "page": page,
      "pagesize": page_size,
      "orderfield": order_field,
      "orderdirection": order_direction }
    response = self._get(self.uri_for("clicks"), params=params)
    return json_to_py(response)

  def unsubscribes(self, date, page=1, page_size=1000, order_field="date", order_direction="asc"):
    """Retrieves the unsubscribes for this campaign."""
    params = { 
      "date": date,
      "page": page,
      "pagesize": page_size,
      "orderfield": order_field,
      "orderdirection": order_direction }
    response = self._get(self.uri_for("unsubscribes"), params=params)
    return json_to_py(response)

  def bounces(self, date="1900-01-01", page=1, page_size=1000, order_field="date", order_direction="asc"):
    """Retrieves the bounces for this campaign."""
    params = { 
      "date": date,
      "page": page,
      "pagesize": page_size,
      "orderfield": order_field,
      "orderdirection": order_direction }
    response = self._get(self.uri_for("bounces"), params=params)
    return json_to_py(response)

  def uri_for(self, action):
    return "/campaigns/%s/%s.json" % (self.campaign_id, action)
