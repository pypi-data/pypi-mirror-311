from dcim.models import Device
from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from virtualization.models import VirtualMachine

from netbox_authorized_keys.filtersets import AuthorizedKeyFilterSet
from netbox_authorized_keys.models import AuthorizedKey
from netbox_authorized_keys.tables import AuthorizedKeyTable


def create_authorized_key_tab_view(model):
    view_name = f"{model._meta.model_name}-authorized-keys"
    view_path = f"{model._meta.model_name}-authorized-keys"

    class AuthorizedKeyTabView(generic.ObjectChildrenView):
        child_model = AuthorizedKey
        filterset = AuthorizedKeyFilterSet
        template_name = "generic/object_children.html"
        table = AuthorizedKeyTable
        queryset = model.objects.all()

        if model == Device:
            tab = ViewTab(
                label="Authorized Keys",
                badge=lambda obj: AuthorizedKey.objects.filter(devices=obj.id).count(),
                permission="netbox_authorized_keys.view_authorizedkey",
            )

            def get_children(self, request, parent):
                children = self.child_model.objects.filter(devices=parent.id).restrict(request.user, "view")
                return children

            def get_table(self, data, request, bulk_actions=True):
                table = super().get_table(data, request, bulk_actions)
                table.exclude = "actions"
                return table

        elif model == VirtualMachine:
            tab = ViewTab(
                label="Authorized Keys",
                badge=lambda obj: AuthorizedKey.objects.filter(virtual_machines=obj.id).count(),
                permission="netbox_authorized_keys.view_authorizedkey",
            )

            def get_children(self, request, parent):
                children = self.child_model.objects.filter(virtual_machines=parent.id).restrict(request.user, "view")
                return children

            def get_table(self, data, request, bulk_actions=True):
                table = super().get_table(data, request, bulk_actions)
                table.exclude = "actions"
                return table

    register_model_view(model, name=view_name, path=view_path)(AuthorizedKeyTabView)


for model in [Device, VirtualMachine]:
    create_authorized_key_tab_view(model)
