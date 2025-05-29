from django.contrib.admin import ModelAdmin


class ReadOnlyAdmin(ModelAdmin):
    """
    Abstract read only admin that prevents non-superusers from editing,
    deleting, or adding objects.
    """

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)

    def get_actions(self, request):
        if not request.user.is_superuser:
            return {}
        return super().get_actions(request)
