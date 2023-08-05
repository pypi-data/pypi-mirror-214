from django.db.models.enums import IntegerChoices, TextChoices

# from djchoices import ChoiceItem, DjangoChoices


# Django
default_app_config = 'infx.machine_intel.data.apps.MachineDataConfig'


class MachineDataStreamTypeChoices(TextChoices):
    CONTROL = 'control', 'Control Data'

    SENSOR = 'sensor', 'Sensor Data'

    CALC = 'calc', '(Intermediate) Calculated Data'

    ALARM = 'alarm', 'Alarm Data'

    ERROR = 'error', 'Error Data'
