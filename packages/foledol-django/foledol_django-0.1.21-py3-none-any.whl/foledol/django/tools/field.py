import re
from datetime import datetime

from foledol.django.utils import to_float


class Field:
    def __init__(self, key, label, disabled):
        self.errors = []
        self.key = key
        self.label = label
        self.disabled = disabled
        self.errors = []
        self.value_as_str = ''
        self.external = False
        self.form = None

    def attach(self, form):
        self.form = form

    def namespace(self):
        return self.form.namespace if self.form else None

    def full_name(self):
        namespace = self.namespace()
        return namespace + "_" + self.key if namespace else self.key

    def set(self, value):
        pass

    def read(self, context, default):
        pass

    def validate(self):
        return True

    def has_error(self):
        return len(self.errors) > 0


class TextField(Field):
    def __init__(self, key, label,
                 placeholder=None,
                 min_length=None,
                 max_length=None,
                 regex=None,
                 blank=True,
                 disabled=False,
                 autocomplete=None,
                 autocomplete_url=None):
        super().__init__(key, label, disabled=disabled)
        self.min_length = min_length
        self.max_length = max_length
        self.placeholder = placeholder
        self.regex = regex
        self.blank = blank
        self.value = None
        self.autocomplete = autocomplete
        self.autocomplete_url = autocomplete_url

    def set(self, value):
        self.value = value if value is not None else None
        self.value_as_str = value if value is not None else ''

    def read(self, context, default):
        key = self.full_name()
        self.set(context[key] if key in context else default)

    def validate(self):
        self.errors = []
        length = len(str(self.value)) if self.value else 0
        if self.value is None and not self.blank:
            self.errors.append("Le champ est obligatoire")
        elif self.min_length and length < self.min_length:
            self.errors.append("La longueur minimale est " + str(self.min_length))
        elif self.max_length and length > self.max_length:
            self.errors.append("La longueur maximale est " + str(self.max_length))
        elif self.regex:
            if not bool(re.search(self.regex, self.value)):
                self.errors.append("Format incorrect")
        return not self.has_error()


class SelectField(Field):
    def __init__(self, key, label, values=None, blank=True, disabled=False, pairs=None):
        super().__init__(key, label, disabled=disabled)
        self.values = values
        self.blank = blank
        self.pairs = pairs
        self.value = None

    def set(self, value):
        self.value = None if value is None else value
        self.value_as_str = str(self.value)

    def read(self, context, default):
        key = self.full_name()
        self.set(context[key] if key in context else default)

    def get_value(self, value):
        if self.pairs:
            keys = [k for k, v in self.pairs.items() if re.search(v, value, re.IGNORECASE)]
            if len(keys) == 1:
                return keys[0]
        return value


class IntegerField(Field):
    def __init__(self, key, label, min_value=None, max_value=None, blank=True, disabled=False):
        super().__init__(key, label, disabled=disabled)
        self.min_value = min_value
        self.max_value = max_value
        self.blank = blank
        self.value = None

    def set(self, value):
        self.value = value if value != '' else None
        self.value_as_str = '' if value is None else str(value)

    def read(self, context, default):
        key = self.full_name()
        if key in context:
            try:
                self.value = int(context[key])
            except ValueError:
                self.value = None
            self.value_as_str = str(context[key])
        else:
            self.set(default)

    def validate(self):
        self.errors = []
        if len(self.value_as_str) < 1 and not self.blank:
            self.errors.append("Le champ est obligatoire")
        elif len(self.value_as_str) > 0 and self.value is None:
            self.errors.append("Format incorrect")
        elif self.min_value and self.value < self.min_value:
            self.errors.append("La valeur minimale est " + str(self.min_value))
        elif self.max_value and self.value > self.max_value:
            self.errors.append("La valeur maximale est " + str(self.max_value))
        return not self.has_error()


class FloatField(Field):
    def __init__(self, key, label, min_value=None, max_value=None, blank=True, disabled=False):
        super().__init__(key, label, disabled=disabled)
        self.min_value = min_value
        self.max_value = max_value
        self.blank = blank
        self.value = None

    def set(self, value):
        self.value = value
        self.value_as_str = '' if value is None else str(value).replace('.', ',')

    def read(self, context, default):
        key = self.full_name()
        if key in context:
            self.value = to_float(context[key])
            self.value_as_str = str(context[key])
        else:
            self.set(default)

    def validate(self):
        self.errors = []
        if len(self.value_as_str) < 1 and not self.blank:
            self.errors.append("Le champ est obligatoire")
        elif len(self.value_as_str) > 0 and self.value is None:
            self.errors.append("Format incorrect")
        elif self.min_value and self.value < self.min_value:
            self.errors.append("La valeur minimale est " + str(self.min_value))
        elif self.max_value and self.value > self.max_value:
            self.errors.append("La valeur maximale est " + str(self.max_value))
        return not self.has_error()


class DateField(Field):
    def __init__(self, key, label,
                 format="%d/%m/%Y",
                 blank=True,
                 disabled=False,
                 date_picker=False,
                 date_picker_format="DD/MM/YYYY",
                 date_picker_locale="fr",
                 placeholder=None):
        super().__init__(key, label, disabled=disabled)
        self.blank = blank
        self.value = None
        self.format = format
        self.date_picker = date_picker
        self.date_picker_format = date_picker_format
        self.date_picker_locale = date_picker_locale
        self.placeholder = placeholder

    def set(self, value):
        self.value = value
        self.value_as_str = value.strftime(self.format) if value else ''

    def read(self, context, default):
        key = self.full_name()
        if key in context:
            try:
                self.value = datetime.strptime(context[key], self.format)
            except ValueError:
                self.value = None
            self.value_as_str = str(context[key])
        else:
            self.set(default)

    def validate(self):
        self.errors = []
        if len(self.value_as_str) < 1 and not self.blank:
            self.errors.append("Le champ est obligatoire")
        elif len(self.value_as_str) > 0 and self.value is None:
            self.errors.append("Format incorrect")
        return not self.has_error()


class TimeField(Field):
    def __init__(self, key, label, format="%H:%M", blank=True, disabled=False):
        super().__init__(key, label, disabled=disabled)
        self.blank = blank
        self.value = None
        self.format = format

    def set(self, value):
        self.value = value
        self.value_as_str = value.strftime(self.format) if value else ''

    def read(self, context, default):
        key = self.full_name()
        if key in context:
            try:
                self.value = datetime.strptime(context[key], self.format)
            except ValueError:
                self.value = None
            self.value_as_str = str(context[key])
        else:
            self.set(default)

    def validate(self):
        self.errors = []
        if len(self.value_as_str) < 1 and not self.blank:
            self.errors.append("Le champ est obligatoire")
        elif len(self.value_as_str) > 0 and self.value is None:
            self.errors.append("Format incorrect")
        return not self.has_error()


class BooleanField(Field):
    def __init__(self, key, label, default=False, disabled=False):
        super().__init__(key, label, disabled=disabled)
        self.value = default

    def set(self, value):
        if isinstance(value, str):
            self.value = value == 'on'
        else:
            self.value = value
        self.value_as_str = str(value)

    def read(self, context, default):
        key = self.full_name()
        default_value = default if default is not None else False
        self.set(key in context if len(context) > 0 else default_value)
