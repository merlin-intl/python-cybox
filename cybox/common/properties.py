from datetime import datetime

import dateutil.parser

import cybox
import cybox.bindings.cybox_common as common_binding
from cybox.common.attribute_groups import PatternFieldGroup
from cybox.utils import normalize_to_xml, denormalize_from_xml


class BaseProperty(cybox.Entity, PatternFieldGroup):

    def __init__(self, value=None):
        super(BaseProperty, self).__init__()
        self.value = value

        # BaseObjectProperty Group
        self.id_ = None
        self.idref = None
        self.datatype = None
        self.appears_random = None
        self.is_obfuscated = None
        self.obfuscation_algorithm_ref = None
        self.is_defanged = None
        self.defanging_algorithm_ref = None
        self.refanging_transform_type = None
        self.refanging_transform = None

    def __str__(self):
        return str(self.serialized_value)

    def __int__(self):
        return int(self.serialized_value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value_):
        # This is done here, so the value is always parsed, regardless of
        # whether it is set via the __init__() function, via the from_*
        # static methods, or on an instance of the class after it has been
        # created.
        if isinstance(value_, list):
            self._value = map(self._parse_value, value_)
        else:
            self._value = self._parse_value(value_)

    @staticmethod
    def _parse_value(value):
        """Parse a user-supplied value into the internal representation.

        For most Property types, this does not modify `value`. However,
        some attributes may have a more specific representation.
        """
        return value

    @property
    def serialized_value(self):
        if isinstance(self.value, list):
            return map(self._serialize_value, self.value)
        else:
            return self.__class__._serialize_value(self.value)

    @staticmethod
    def _serialize_value(value):
        """Format the `value` for serialization (XML, JSON).

        For most attribute types, this will return the `value` unmodified.
        However, some attributes types may need additional formatting.
        """
        return value


    def __eq__(self, other):
        # It is possible to compare a Property to a single value if
        # the Property defines only the "value" property.
        if not isinstance(other, BaseProperty) and self.is_plain():
            return self.value == other

        return (
            self.value == other.value and
            self.id_ == other.id_ and
            self.idref == other.idref and
            self.datatype == other.datatype and
            self.appears_random == other.appears_random and
            self.is_obfuscated == other.is_obfuscated and
            self.obfuscation_algorithm_ref == other.obfuscation_algorithm_ref and
            self.is_defanged == other.is_defanged and
            self.defanging_algorithm_ref == other.defanging_algorithm_ref and
            self.refanging_transform_type == other.refanging_transform_type and
            self.refanging_transform == other.refanging_transform and

            PatternFieldGroup._conditions_equal(self, other) and

            self.bit_mask == other.bit_mask and
            self.pattern_type == other.pattern_type and
            self.regex_syntax == other.regex_syntax and
            self.has_changed == other.has_changed and
            self.trend == other.trend
        )

    def __ne__(self, other):
        return not (self == other)

    def is_plain(self):
        """Whether the Property can be represented as a single value.

        The `datatype` can be inferred by the particular BaseProperty subclass,
        so if `datatype` and `value` are the only non-None properties, the
        BaseProperty can be represented by a single value rather than a
        dictionary. This makes the JSON representation simpler without losing
        any data fidelity.
        """
        return (
            # ignore value
            self.id_ is None and
            self.idref is None and
            # ignore datatype
            self.appears_random is None and
            self.is_obfuscated is None and
            self.obfuscation_algorithm_ref is None and
            self.is_defanged is None and
            self.defanging_algorithm_ref is None and
            self.refanging_transform_type is None and
            self.refanging_transform is None and

            PatternFieldGroup.is_plain(self)
        )

    def _get_binding_class(self):
        """Each subclass must specify the class from the CybOX Common binding
        which used to represent that attribute type.

        Returns a class.
        """
        raise NotImplementedError

    def __nonzero__(self):
        return (not self.is_plain()) or (self.value is not None)

    __bool__ = __nonzero__

    def to_obj(self):
        AttrBindingClass = self._get_binding_class()

        attr_obj = AttrBindingClass()

        attr_obj.set_valueOf_(normalize_to_xml(self.serialized_value))
        # For now, don't output the datatype, as it is not required and is
        # usually not needed, as it can be inferred from the context.
        #attr_obj.set_datatype(self.datatype)

        if self.id_ is not None:
            attr_obj.set_id(self.id_)
        if self.idref is not None:
            attr_obj.set_idref(self.idref)
        if self.appears_random is not None:
            attr_obj.set_appears_random(self.appears_random)
        if self.is_obfuscated is not None:
            attr_obj.set_is_obfuscated(self.is_obfuscated)
        if self.obfuscation_algorithm_ref is not None:
            attr_obj.set_obfuscation_algorithm_ref(self.obfuscation_algorithm_ref)
        if self.is_defanged is not None:
            attr_obj.set_is_defanged(self.is_defanged)
        if self.defanging_algorithm_ref is not None:
            attr_obj.set_defanging_algorithm_ref(self.defanging_algorithm_ref)
        if self.refanging_transform_type is not None:
            attr_obj.set_refanging_transform_type(self.refanging_transform_type)
        if self.refanging_transform is not None:
            attr_obj.set_refanging_transform(self.refanging_transform)

        PatternFieldGroup.to_obj(self, attr_obj)

        return attr_obj

    def to_dict(self):
        if self.is_plain():
            return self.serialized_value

        attr_dict = {}
        if self.value is not None:
            attr_dict['value'] = self.serialized_value
        # For now, don't output the datatype, as it is not required and is
        # usually not needed, as it can be inferred from the context.
        #if self.datatype is not None:
        #    attr_dict['datatype'] = self.datatype

        if self.id_ is not None:
            attr_dict['id'] = self.id_
        if self.idref is not None:
            attr_dict['idref'] = self.idref
        if self.appears_random is not None:
            attr_dict['appears_random'] = self.appears_random
        if self.is_obfuscated is not None:
            attr_dict['is_obfuscated'] = self.is_obfuscated
        if self.obfuscation_algorithm_ref is not None:
            attr_dict['obfuscation_algorithm_ref'] = self.obfuscation_algorithm_ref
        if self.is_defanged is not None:
            attr_dict['is_defanged'] = self.is_defanged
        if self.defanging_algorithm_ref is not None:
            attr_dict['defanging_algorithm_ref'] = self.defanging_algorithm_ref
        if self.refanging_transform_type is not None:
            attr_dict['refanging_transform_type'] = self.refanging_transform_type
        if self.refanging_transform is not None:
            attr_dict['refanging_transform'] = self.refanging_transform

        PatternFieldGroup.to_dict(self, attr_dict)

        return attr_dict

    @classmethod
    def from_obj(cls, attr_obj):
        # Subclasses with additional fields should override this method
        # and use _populate_from_obj as necessary.

        # Use the subclass this was called on to initialize the object

        if not attr_obj:
            return None

        attr = cls()
        attr._populate_from_obj(attr_obj)
        return attr

    def _populate_from_obj(self, attr_obj):
        self.value = denormalize_from_xml(attr_obj.get_valueOf_())

        self.id_ = attr_obj.get_id()
        self.idref = attr_obj.get_idref()
        self.datatype = attr_obj.get_datatype()
        self.appears_random = attr_obj.get_appears_random()
        self.is_obfuscated = attr_obj.get_is_obfuscated()
        self.obfuscation_algorithm_ref = attr_obj.get_obfuscation_algorithm_ref()
        self.is_defanged = attr_obj.get_is_defanged()
        self.defanging_algorithm_ref = attr_obj.get_defanging_algorithm_ref()
        self.refanging_transform_type = attr_obj.get_refanging_transform_type()
        self.refanging_transform = attr_obj.get_refanging_transform()

        PatternFieldGroup.from_obj(attr_obj, self)

    @classmethod
    def from_dict(cls, attr_dict):
        # Subclasses with additional fields should override this method
        # and use _populate_from_dict as necessary.

        if not attr_dict:
            return None

        # Use the subclass this was called on to initialize the object.
        attr = cls()
        attr._populate_from_dict(attr_dict)
        return attr

    def _populate_from_dict(self, attr_dict):
        # If this attribute is "plain", use it as the value and assume the
        # datatype was set correctly by the constructor of the particular
        # BaseProperty Subclass.
        if not isinstance(attr_dict, dict):
            self.value = attr_dict
        else:
            # These keys should always be present
            self.value = attr_dict.get('value')
            self.datatype = attr_dict.get('datatype')

            # 'None' is fine if these keys are missing
            self.id_ = attr_dict.get('id')
            self.idref = attr_dict.get('idref')
            self.appears_random = attr_dict.get('appears_random')
            self.is_obfuscated = attr_dict.get('is_obfuscated')
            self.obfuscation_algorithm_ref = attr_dict.get('obfuscation_algorithm_ref')
            self.is_defanged = attr_dict.get('is_defanged')
            self.defanging_algorithm_ref = attr_dict.get('defanging_algorithm_ref')
            self.refanging_transform_type = attr_dict.get('refanging_transform_type')
            self.refanging_transform = attr_dict.get('refanging_transform')

            PatternFieldGroup.from_dict(attr_dict, self)


class String(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "string"

    def _get_binding_class(self):
        return common_binding.StringObjectPropertyType


class UnsignedLong(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "unsignedLong"

    def _get_binding_class(self):
        return common_binding.UnsignedLongObjectPropertyType

    @staticmethod
    def _parse_value(value):
        if value is None:
            return None
        return int(value)

class Integer(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "integer"

    def _get_binding_class(self):
        return common_binding.IntegerObjectPropertyType

    @staticmethod
    def _parse_value(value):
        if value is None:
            return None
        return int(value)


class PositiveInteger(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "positiveInteger"

    def _get_binding_class(self):
        return common_binding.PositiveIntegerObjectPropertyType

    @staticmethod
    def _parse_value(value):
        if value is None:
            return None
        return int(value)

class UnsignedInteger(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProeprty.__init__(self, *args, **kwargs)
        self.datatype = "unsignedInt"

    def _get_binding_class(self):
        return common_binding.UnsignedIntegerObjectPropertyType

class NonNegativeInteger(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProeprty.__init__(self, *args, **kwargs)
        self.datatype = "nonNegativeInteger"

    def _get_binding_class(self):
        return common_binding.NonNegativeIntegerObjectPropertyType

    @staticmethod
    def _parse_value(value):
        if value is None:
            return None
        return int(value)

class AnyURI(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "anyURI"

    def _get_binding_class(self):
        return common_binding.AnyURIObjectPropertyType

class HexBinary(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "hexBinary"

    def _get_binding_class(self):
        return common_binding.HexBinaryObjectPropertyType

class Duration(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "duration"

    def _get_binding_class(self):
        return common_binding.DurationObjectPropertyType

class DateTime(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "dateTime"

    def _get_binding_class(self):
        return common_binding.DateTimeObjectPropertyType

    def _parse_value(self, value):
        if not value:
            return None
        elif isinstance(value, datetime):
            return value
        return dateutil.parser.parse(value)

    @staticmethod
    def _serialize_value(value):
        if not value:
            return None
        return value.isoformat()

class Double(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "double"

    def _get_binding_class(self):
        return common_binding.DoubleObjectPropertyType

class Float(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "float"

    def _get_binding_class(self):
        return common_binding.FloatObjectPropertyType

class Long(BaseProperty):
    def __init__(self, *args, **kwargs):
        BaseProperty.__init__(self, *args, **kwargs)
        self.datatype = "long"

    def _get_binding_class(self):
        return common_binding.LongObjectPropertyType

# Mapping of binding classes to the corresponding BaseProperty subclass
BINDING_CLASS_MAPPING = {
        common_binding.StringObjectPropertyType: String,
        common_binding.IntegerObjectPropertyType: Integer,
        common_binding.PositiveIntegerObjectPropertyType: PositiveInteger,
        common_binding.UnsignedIntegerObjectPropertyType: UnsignedInteger,
        common_binding.UnsignedLongObjectPropertyType: UnsignedLong,
        common_binding.AnyURIObjectPropertyType: AnyURI,
        common_binding.HexBinaryObjectPropertyType: HexBinary,
        common_binding.DateTimeObjectPropertyType: DateTime,
        common_binding.DurationObjectPropertyType: Duration,
        common_binding.NonNegativeIntegerObjectPropertyType: NonNegativeInteger,
        common_binding.FloatObjectPropertyType: Float,
        common_binding.DoubleObjectPropertyType: Double,
        common_binding.LongObjectPropertyType: Long,
        common_binding.UnsignedLongObjectPropertyType: UnsignedLong,
        # This shouldn't be needed anymore, but we'll leave it here to be safe.
        common_binding.SimpleHashValueType: HexBinary,
#        common_binding.HashNameType: HashName,
    }
