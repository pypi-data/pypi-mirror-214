# coding: utf-8

"""
    Mantium API

    Mantium API Documentation  # noqa: E501

    The version of the OpenAPI document: 1.0.358
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from mantium_spec.configuration import Configuration


class ContentCreationTemplateOptions(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'type': 'str',
        'is_activating': 'bool',
        'credentials': 'list[ApplicationCredential]'
    }

    attribute_map = {
        'type': 'type',
        'is_activating': 'is_activating',
        'credentials': 'credentials'
    }

    def __init__(self, type='content-creation', is_activating=False, credentials=None, local_vars_configuration=None):  # noqa: E501
        """ContentCreationTemplateOptions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._is_activating = None
        self._credentials = None
        self.discriminator = None

        if type is not None:
            self.type = type
        if is_activating is not None:
            self.is_activating = is_activating
        if credentials is not None:
            self.credentials = credentials

    @property
    def type(self):
        """Gets the type of this ContentCreationTemplateOptions.  # noqa: E501


        :return: The type of this ContentCreationTemplateOptions.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ContentCreationTemplateOptions.


        :param type: The type of this ContentCreationTemplateOptions.  # noqa: E501
        :type type: str
        """
        allowed_values = ["content-creation"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def is_activating(self):
        """Gets the is_activating of this ContentCreationTemplateOptions.  # noqa: E501


        :return: The is_activating of this ContentCreationTemplateOptions.  # noqa: E501
        :rtype: bool
        """
        return self._is_activating

    @is_activating.setter
    def is_activating(self, is_activating):
        """Sets the is_activating of this ContentCreationTemplateOptions.


        :param is_activating: The is_activating of this ContentCreationTemplateOptions.  # noqa: E501
        :type is_activating: bool
        """

        self._is_activating = is_activating

    @property
    def credentials(self):
        """Gets the credentials of this ContentCreationTemplateOptions.  # noqa: E501


        :return: The credentials of this ContentCreationTemplateOptions.  # noqa: E501
        :rtype: list[ApplicationCredential]
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """Sets the credentials of this ContentCreationTemplateOptions.


        :param credentials: The credentials of this ContentCreationTemplateOptions.  # noqa: E501
        :type credentials: list[ApplicationCredential]
        """

        self._credentials = credentials

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ContentCreationTemplateOptions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ContentCreationTemplateOptions):
            return True

        return self.to_dict() != other.to_dict()
