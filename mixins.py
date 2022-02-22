class RestDynamicSerializerFields:
    def __init__(self, *args, **kwargs):
        self.custom_fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

    def get_field_names(self, *args, **kwargs):
        fields_name = super().get_field_names(*args, **kwargs)
        if self.custom_fields:
            allowed, existing = set(self.custom_fields), set(fields_name)
            modifiy_fields = existing.intersection(allowed)
            return tuple(modifiy_fields)
        return fields_name


class RestDynamicViewSerializerFields:
    serializer_fields = None

    def __init__(self, *args, **kwargs) -> None:
        self.check_serializer_class_is_subclass_of_dynamic_fields()
        self.check_serializer_fields()
        super().__init__(*args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(fields=self.serializer_fields, *args, **kwargs)

    def check_serializer_fields(self) -> None:
        if self.serializer_fields and not isinstance(self.serializer_fields, (tuple, list)):
            raise TypeError("'serializer_fields' must be tuple or list instance.")

    def check_serializer_class_is_subclass_of_dynamic_fields(self) -> None:
        if not issubclass(self.serializer_class, RestDynamicSerializerFields):
            raise NotImplementedError("serializer class should inheritance from 'RestDynamicSerializerFields'")
