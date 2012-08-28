from wtforms import (Form, TextField, TextAreaField, SelectField,
     SelectMultipleField, DateTimeField, FileField, widgets,
     validators, IntegerField, FormField, FieldList, HiddenField)
from wtforms.ext.appengine.db import model_form
from lib.model import Event

# This file contains all the forms used at the backend (besides the
# admin-related forms)

# a multi-select list composed out of many checkboxes
class MultiCheckboxField(SelectMultipleField):
  widget = widgets.ListWidget(prefix_label=False)
  option_widget = widgets.CheckboxInput()

class EventForm(Form):
  gplus_event_url = TextField('Google+ Event URL',
        [validators.URL(), validators.Required()])
  external_url    = TextField('External URL (in an iframe or linked to)',
        [validators.Optional(),validators.URL()])
  external_width  = IntegerField('Width of the iframe (if embedded)',
        [validators.Optional(),validators.NumberRange(min=0,max=700)])
  external_height = IntegerField('Height of the iframe (if embedded)',
        [validators.Optional(),validators.NumberRange(min=0,max=500)])
  location        = TextField('Location',
        [validators.Length(min=3), validators.Required()])
  status          = SelectField('Status',
        choices=[('1', 'interested'), ('2', 'planned'), ('3', 'confirmed')])
  logo            = FileField('Logo')
  agenda          = MultiCheckboxField('Agenda',
        choices=[
           ('1', '<img src="/images/icons/conf-icon.png"> Conference'),
           ('2', '<img src="/images/icons/hack-icon.png"> '
                           'Hackathon/VHackAndroid'),
           ('3', '<img src="/images/icons/barcamp-icon.png"> Barcamp'),
           ('4', '<img src="/images/icons/gdl-icon.png"> '
                           'Google Developer Live sessions'),
           ('5', '<img src="/images/icons/others-icon.png"> Others')])
  start           = DateTimeField('Start', format="%Y-%m-%d %H:%M")
  end             = DateTimeField('End', format="%Y-%m-%d %H:%M")
  gdg_chapters    = TextField('GDG Chapters',
        [validators.Required()], description='Comma separated list')
  technologies    = MultiCheckboxField(
         'What products, technologies you propose to cover in the event',
        choices=[('Android', 'Android'),
                 ('Chrome', 'Chrome'),
                 ('Google+', 'Google+'),
                 ('App Engine', 'App Engine'),
                 ('Games', 'Games'),
                 ('Google Maps', 'Google Maps'),
                 ('Google Apps', 'Google Apps'),
                 ('Google TV', 'Google TV'),
                 ('Commerce', 'Commerce'),
                 ('Youtube', 'Youtube'),
                 ('Other', 'Other')])
  kind_of_support = TextAreaField(
         'What kind of support you expect for this event?',
        [validators.Required()])
  subdomain       = TextField('Preferred subdomain for the event website')
  register_url    = TextField('URL of external registration site',
        [validators.Optional(),validators.URL()])
  register_formkey = TextField('Formkey from Docs registration form')

class ContactForm(Form):
  name            = TextField('Your Name', [validators.Required()])
  email           = TextField('Email Address',
        [validators.Email(), validators.Required()])
  organizer       = SelectField('Are you GDG organizer?',
        choices=[('0', 'No'), ('1', 'Yes')])
  gdg_chapter     = TextField('Your GDG Chapter')
  subject         = TextField('Subject', [validators.Required()])
  message         = TextAreaField('Message', [validators.Required()])


class SponsorForm(Form):
  name            = TextField('Name of Sponsor', [validators.Required()])
  gplus_id        = IntegerField('Google+ ID (21 digits)',
        [validators.number_range(10 ** 20, 10 ** 21 - 1, "21 digits required")])
  description     = TextAreaField("Company Description",
        [validators.length(20, 250)])
  logo            = FileField('Sponsor\'s Logo')

# subform: a speaker - used in event-speakers form
class SingleSpeakerForm(Form):
  speaker         = HiddenField()
  first_name      = TextField('Given name', [validators.Required()])
  last_name       = TextField('Surname', [validators.Required()])
  gplus_id        = IntegerField('Google+ ID (21 digits)',
        [validators.Optional(),
         validators.number_range(10 ** 20, 10 ** 21 - 1, "21 digits required")])
  short_bio       = TextAreaField("Short biography", [validators.Required()])
  thumbnail       = FileField('Speaker\'s Picture')

# allow modification of list of speakers for an event
class SpeakersForm(Form):
  speakers        = FieldList(FormField(SingleSpeakerForm), min_entries=1)

# subform: a sponsor - used in event-sponsors form
class SingleSponsorForm(Form):
  sponsor         = HiddenField()
  name            = TextField('Name of Sponsor', [validators.Required()])
  gplus_id        = IntegerField('Google+ ID (21 digits)',
        [validators.number_range(10 ** 20, 10 ** 21 - 1, "21 digits required")])
  description     = TextAreaField("Company Description",
        [validators.length(20, 250)])
  level           = TextField('Level of Sponsorship (e.g. "Gold", "Platinum")')
  logo            = FileField('Sponsor\'s Logo')

# allow modification of list of speakers for an event
class SponsorsForm(Form):
  sponsors        = FieldList(FormField(SingleSponsorForm), min_entries=1)

# subform: a session - used in event-sessions form
class SingleSessionForm(Form):
  session         = HiddenField()
  title           = TextField('Name of the session', [ validators.Required()])
  abstract        = TextAreaField('Abstract')
  start           = DateTimeField('Start', format="%Y-%m-%d %H:%M")
  end             = DateTimeField('End', format="%Y-%m-%d %H:%M")
  room            = TextField('Room')
  level           = TextField('Level (e.g. "Intermediate")')
  track           = TextField('Track')
  live_url        = TextField('URL of Live Stream')
  youtube_url     = TextField('URL on Youtube')
  # this field will get its choices specified dynamically
  speakers        = MultiCheckboxField('Speakers')

# subform: a track - used in event-tracks form
class SingleTrackForm(Form):
  track           = HiddenField()
  name            = TextField('Name', [validators.Required()])
  color           = TextField('Color', [validators.Regexp('#[0-9A-Z]{6}')])
  abstract        = TextAreaField('Abstract')

# allow modification of list of sessions and tracks for an event
class SessionsTracksForm(Form):
  sessions        = FieldList(FormField(SingleSessionForm), min_entries=1)
  tracks          = FieldList(FormField(SingleTrackForm), min_entries=1)
