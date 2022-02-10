class DynamicSerializerFields:
    serializer_fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_serializer_fields()
        self.serializer_class.__init__ = self.overridden_init

    @staticmethod
    def overridden_init(self, *args, **kwargs) -> None:
        super(self.__class__, self).__init__(*args, **kwargs)
        view = self.context.get('view')
        fields = getattr(view, 'serializer_fields', None)

        if fields is not None:
            allowed, existing = set(fields), set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def check_serializer_fields(self) -> None:
        if self.serializer_fields and not isinstance(self.serializer_fields, (tuple, list)):
            raise TypeError("'serializer_fields' must be tuple or list instance.")
