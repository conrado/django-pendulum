from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
import re

re_id = re.compile('id="([^"]+)"')

# see if the user has overridden the media
if hasattr(settings, 'PENDULUM_DATE_MEDIA'):
    PENDULUM_DATE_MEDIA = settings.PENDULUM_DATE_MEDIA
else:
    PENDULUM_DATE_MEDIA = {
        'js': (settings.STATIC_URL + 'js/jquery.js',
               settings.STATIC_URL + 'js/jquery.ui.js'),
        'css': {
            'all': (settings.STATIC_URL + 'css/jquery-ui.css',)
        }
    }

class DateWidget(forms.TextInput):
    class Media:
        js = PENDULUM_DATE_MEDIA['js']
        css = PENDULUM_DATE_MEDIA['css']

    def __init__(self, attrs={}):
        super(DateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'})

class TimeWidget(forms.TextInput):
    def __init__(self, attrs={}):
        super(TimeWidget, self).__init__(attrs={'class': 'vTimeField', 'size': '8'})

class PendulumDateTimeWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [DateWidget, TimeWidget]
        super(PendulumDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

    def format_output(self, rendered_widgets):
        # make things a little more accessible by adding labels to the output
        date_id = time_id = ''
        try:
            date_id = re_id.findall(rendered_widgets[0])[0]
        except:
            pass
        try:
            time_id = re_id.findall(rendered_widgets[1])[0]
        except:
            pass

        return mark_safe(u'''<div class="datetime">
    <label for="%s">Date:</label> %s<br />
    <label for="%s">Time:</label> %s
</div>''' % (date_id, rendered_widgets[0], time_id, rendered_widgets[1]))
