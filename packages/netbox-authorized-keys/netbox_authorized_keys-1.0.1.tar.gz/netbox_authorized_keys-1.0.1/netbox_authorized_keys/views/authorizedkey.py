from dcim.models import Device
from netbox.views import generic
from virtualization.models import VirtualMachine

from netbox_authorized_keys.filtersets import (
    AuthorizedKeyDeviceFilterSet,
    AuthorizedKeyFilterSet,
    AuthorizedKeyVirtualMachineFilterSet,
)
from netbox_authorized_keys.forms import (
    AuthorizedKeyDeviceFilterForm,
    AuthorizedKeyFilterForm,
    AuthorizedKeyForm,
    AuthorizedKeyVirtualMachineFilterForm,
)
from netbox_authorized_keys.models import AuthorizedKey, AuthorizedKeyDevice, AuthorizedKeyVirtualMachine
from netbox_authorized_keys.tables import AuthorizedKeyDeviceTable, AuthorizedKeyTable, AuthorizedKeyVirtualMachineTable


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


# Authorized Key Devices
class AuthorizedKeyDeviceListView(generic.ObjectListView):
    queryset = AuthorizedKeyDevice.objects.all()
    table = AuthorizedKeyDeviceTable
    filterset = AuthorizedKeyDeviceFilterSet
    filterset_form = AuthorizedKeyDeviceFilterForm


# Authorized Key Virtual Machines
class AuthorizedKeyVirtualMachineListView(generic.ObjectListView):
    queryset = AuthorizedKeyVirtualMachine.objects.all()
    table = AuthorizedKeyVirtualMachineTable
    filterset = AuthorizedKeyVirtualMachineFilterSet
    filterset_form = AuthorizedKeyVirtualMachineFilterForm
