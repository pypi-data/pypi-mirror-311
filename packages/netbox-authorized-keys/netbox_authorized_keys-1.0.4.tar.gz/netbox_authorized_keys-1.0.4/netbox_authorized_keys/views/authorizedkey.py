from dcim.models import Device
from netbox.views import generic
from virtualization.models import VirtualMachine

from netbox_authorized_keys.filtersets import (
    AuthorizedKeyFilterSet,
)
from netbox_authorized_keys.forms import (
    AuthorizedKeyBulkEditForm,
    AuthorizedKeyBulkImportForm,
    AuthorizedKeyFilterForm,
    AuthorizedKeyForm,
)
from netbox_authorized_keys.models import AuthorizedKey
from netbox_authorized_keys.tables import AuthorizedKeyTable


class AuthorizedKeyListView(generic.ObjectListView):
    queryset = AuthorizedKey.objects.all()
    table = AuthorizedKeyTable
    filterset = AuthorizedKeyFilterSet
    filterset_form = AuthorizedKeyFilterForm


class AuthorizedKeyView(generic.ObjectView):
    queryset = AuthorizedKey.objects.all()

    def get_extra_context(self, request, instance):
        device_ids = list(Device.objects.filter(authorized_keys=instance).values_list("id", flat=True))
        virtual_machine_ids = list(VirtualMachine.objects.filter(authorized_keys=instance).values_list("id", flat=True))

        return {
            "device_ids": device_ids,
            "virtual_machine_ids": virtual_machine_ids,
        }


class AuthorizedKeyEditView(generic.ObjectEditView):
    queryset = AuthorizedKey.objects.all()
    form = AuthorizedKeyForm


class AuthorizedKeyDeleteView(generic.ObjectDeleteView):
    queryset = AuthorizedKey.objects.all()


class AuthorizedKeyBulkImportView(generic.BulkImportView):
    queryset = AuthorizedKey.objects.all()
    model_form = AuthorizedKeyBulkImportForm


class AuthorizedKeyBulkEditView(generic.BulkEditView):
    queryset = AuthorizedKey.objects.all()
    filterset = AuthorizedKeyFilterSet
    table = AuthorizedKeyTable
    form = AuthorizedKeyBulkEditForm


class AuthorizedKeyBulkDeleteView(generic.BulkDeleteView):
    queryset = AuthorizedKey.objects.all()
    filterset = AuthorizedKeyFilterSet
    table = AuthorizedKeyTable
