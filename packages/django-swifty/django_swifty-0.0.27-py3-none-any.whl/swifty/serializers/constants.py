"""Constants"""

from typing import Dict, Any
from rest_framework import serializers

STATIC_FIELDS = (
    "read_only",
    "write_only",
    "required",
    "default",
    "initial",
    "source",
    "label",
    "help_text",
    "style",
    "error_messages",
    "validators",
    "allow_null",
)

FIELD_TYPE_MAP: Dict[str, Dict[str, Any]] = {
    "CharField": {
        "type": serializers.CharField,
        "extra_args": ("allow_blank", "trim_whitespace", "max_length", "min_length"),
        "empty_value": "",
    },
    "EmailField": {
        "type": serializers.EmailField,
        "extra_args": ("allow_blank", "trim_whitespace", "max_length", "min_length"),
        "empty_value": "",
    },
    "URLField": {
        "type": serializers.URLField,
        "extra_args": ("allow_blank", "trim_whitespace", "max_length", "min_length"),
        "empty_value": "",
    },
    "UUIDField": {
        "type": serializers.UUIDField,
        "extra_args": (
            "allow_blank",
            "trim_whitespace",
            "max_length",
            "min_length",
            "format",
            "hex_verbose",
        ),
        "empty_value": "",
    },
    "IntegerField": {
        "type": serializers.IntegerField,
        "extra_args": ("max_value", "min_value"),
        "empty_value": 0,
    },
    "FloatField": {
        "type": serializers.FloatField,
        "extra_args": ("max_value", "min_value"),
        "empty_value": 0.0,
    },
    "DecimalField": {
        "type": serializers.DecimalField,
        "extra_args": (
            "max_digits",
            "decimal_places",
            "coerce_to_string",
            "max_value",
            "min_value",
            "normalize_output",
            "localize",
            "rounding",
        ),
        "empty_value": 0.0,
    },
    "BooleanField": {
        "type": serializers.BooleanField,
        "extra_args": ("allow_null",),
        "empty_value": False,
    },
    "DateField": {
        "type": serializers.DateField,
        "extra_args": ("format", "input_formats"),
        "empty_value": None,
    },
    "DateTimeField": {
        "type": serializers.DateTimeField,
        "extra_args": ("format", "input_formats", "default_timezone"),
        "empty_value": None,
    },
    "TimeField": {
        "type": serializers.TimeField,
        "extra_args": ("format", "input_formats"),
        "empty_value": None,
    },
    "ListField": {
        "type": serializers.ListField,
        "extra_args": ("child", "allow_empty", "max_length", "min_length"),
        "empty_value": [],
    },
    "DictField": {
        "type": serializers.DictField,
        "extra_args": ("child", "allow_empty"),
        "empty_value": {},
    },
    "ChoiceField": {
        "type": serializers.ChoiceField,
        "extra_args": ("choices", "html_cutoff", "html_cutoff_text", "allow_blank"),
        "empty_value": None,
    },
    "SlugField": {
        "type": serializers.SlugField,
        "extra_args": ("allow_unicode",),
        "empty_value": "",
    },
    "FileField": {
        "type": serializers.FileField,
        "extra_args": ("allow_empty_file", "use_url", "max_length"),
        "empty_value": None,
    },
    "ImageField": {
        "type": serializers.ImageField,
        "extra_args": (
            "allow_empty_file",
            "use_url",
            "max_length",
            "_DjangoImageField",
        ),
        "empty_value": None,
    },
    "SerializerMethodField": {
        "type": serializers.SerializerMethodField,
        "extra_args": ("method_name", "source", "read_only"),
        "empty_value": None,
    },
    "HyperlinkedIdentityField": {
        "type": serializers.HyperlinkedIdentityField,
        "extra_args": (
            "view_name",
            "lookup_field",
            "lookup_url_kwarg",
            "format",
            "read_only",
            "source",
        ),
        "empty_value": None,
    },
    "HyperlinkedRelatedField": {
        "type": serializers.HyperlinkedRelatedField,
        "extra_args": ("view_name", "lookup_field", "lookup_url_kwarg", "format"),
        "empty_value": None,
    },
    "PrimaryKeyRelatedField": {
        "type": serializers.PrimaryKeyRelatedField,
        "extra_args": (
            "pk_field",
            "queryset",
            "many",
            "read_only",
            "html_cutoff",
            "html_cutoff_text",
        ),
        "empty_value": None,
    },
    "RelatedField": {
        "type": serializers.RelatedField,
        "extra_args": (
            "queryset",
            "many",
            "read_only",
            "html_cutoff",
            "html_cutoff_text",
        ),
        "empty_value": None,
    },
}
