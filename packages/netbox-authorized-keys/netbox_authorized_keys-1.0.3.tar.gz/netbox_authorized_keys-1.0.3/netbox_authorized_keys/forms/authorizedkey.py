from dcim.models import Device
from django import forms
from django.utils.translation import gettext_lazy as _
from netbox.forms import NetBoxModelFilterSetForm, NetBoxModelForm
from utilities.forms.fields import (
    CommentField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.rendering import FieldSet
from virtualization.models import VirtualMachine

from netbox_authorized_keys.models import AuthorizedKey, AuthorizedKeyDevice, AuthorizedKeyVirtualMachine


class AuthorizedKeyForm(NetBoxModelForm):
    public_key = forms.CharField(
        label=_("Public Key"), widget=forms.Textarea, required=True, help_text=_("Enter the public key (unique)")
    )
    username = forms.CharField(label=_("Username"), required=True)
    full_name = forms.CharField(label=_("Full Name"), required=False, help_text=_("Owner's Full Name"))

    devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), label=_("Devices"), required=False)
    virtual_machines = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(), label=_("Virtual Machines"), required=False
    )

    fieldsets = (
        FieldSet("public_key", "username", "full_name", "description", name=_("Base")),
        FieldSet("devices", "virtual_machines", name=_("Host Assignment")),
        FieldSet("tags", name=_("Misc")),
    )

    class Meta:
        comments = CommentField()
        model = AuthorizedKey
        fields = [
            "public_key",
            "username",
            "full_name",
            "description",
            "devices",
            "virtual_machines",
            "comments",
            "tags",
        ]


class AuthorizedKeyFilterForm(NetBoxModelFilterSetForm):
    model = AuthorizedKey
    public_key = forms.CharField(required=False, widget=forms.widgets.Textarea(attrs={"placeholder": _("Public Key")}))
    username = forms.CharField(required=False)
    full_name = forms.CharField(required=False)
    description = forms.CharField(required=False)

    devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), label=_("Devices"), required=False)
    virtual_machines = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(), label=_("Virtual Machines"), required=False
    )

    tag = TagFilterField(model)


class AuthorizedKeyDeviceFilterForm(NetBoxModelFilterSetForm):
    model = AuthorizedKeyDevice
    authorized_key = DynamicModelMultipleChoiceField(
        queryset=AuthorizedKey.objects.all(), label=_("Authorized Key"), required=False
    )
    device = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), label=_("Device"), required=False)


class AuthorizedKeyVirtualMachineFilterForm(NetBoxModelFilterSetForm):
    model = AuthorizedKeyVirtualMachine
    authorized_key = DynamicModelMultipleChoiceField(
        queryset=AuthorizedKey.objects.all(), label=_("Authorized Key"), required=False
    )
    virtual_machine = DynamicModelMultipleChoiceField(
        queryset=VirtualMachine.objects.all(), label=_("Virtual Machine"), required=False
    )
