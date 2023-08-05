from django.apps import AppConfig

import os


class MachineDataConfig(AppConfig):
    name = 'infx.machine_intel.data'

    label = 'InfX_MachineIntel_Data'

    verbose_name = '(Meta)Data'

    path = os.path.dirname(__file__)
