from django.urls.conf import path
from django_util.autocompletes import autocomplete_factory

from .models import \
    MachineHealthProblem, \
    MachineErrorCode


MachineHealthProblemAutoComplete = \
    autocomplete_factory(
        MachineHealthProblem,
        min_input_len=1)


MachineErrorCodeAutoComplete = \
    autocomplete_factory(
        MachineErrorCode,
        min_input_len=1)


AUTOCOMPLETE_URL_PATTERNS = [
    path(f'{MachineHealthProblemAutoComplete.name}/',
         MachineHealthProblemAutoComplete.as_view(),
         name=MachineHealthProblemAutoComplete.name)
]
