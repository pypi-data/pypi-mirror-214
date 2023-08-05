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


class ApplicationResponse(object):
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
        'id': 'str',
        'created_at': 'datetime',
        'name': 'str',
        'description': 'str',
        'top_k': 'int',
        'status': 'ApplicationStatus'
    }

    attribute_map = {
        'id': 'id',
        'created_at': 'created_at',
        'name': 'name',
        'description': 'description',
        'top_k': 'top_k',
        'status': 'status'
    }

    def __init__(self, id=None, created_at=None, name=None, description=None, top_k=None, status=None, local_vars_configuration=None):  # noqa: E501
        """ApplicationResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._created_at = None
        self._name = None
        self._description = None
        self._top_k = None
        self._status = None
        self.discriminator = None

        self.id = id
        self.created_at = created_at
        self.name = name
        self.description = description
        self.top_k = top_k
        self.status = status

    @property
    def id(self):
        """Gets the id of this ApplicationResponse.  # noqa: E501

        A unique identifier  # noqa: E501

        :return: The id of this ApplicationResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ApplicationResponse.

        A unique identifier  # noqa: E501

        :param id: The id of this ApplicationResponse.  # noqa: E501
        :type id: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_at(self):
        """Gets the created_at of this ApplicationResponse.  # noqa: E501

        Date the application was created  # noqa: E501

        :return: The created_at of this ApplicationResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ApplicationResponse.

        Date the application was created  # noqa: E501

        :param created_at: The created_at of this ApplicationResponse.  # noqa: E501
        :type created_at: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def name(self):
        """Gets the name of this ApplicationResponse.  # noqa: E501

        Name of the application  # noqa: E501

        :return: The name of this ApplicationResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ApplicationResponse.

        Name of the application  # noqa: E501

        :param name: The name of this ApplicationResponse.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this ApplicationResponse.  # noqa: E501

        Description of the application  # noqa: E501

        :return: The description of this ApplicationResponse.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ApplicationResponse.

        Description of the application  # noqa: E501

        :param description: The description of this ApplicationResponse.  # noqa: E501
        :type description: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def top_k(self):
        """Gets the top_k of this ApplicationResponse.  # noqa: E501

        Number of results to return  # noqa: E501

        :return: The top_k of this ApplicationResponse.  # noqa: E501
        :rtype: int
        """
        return self._top_k

    @top_k.setter
    def top_k(self, top_k):
        """Sets the top_k of this ApplicationResponse.

        Number of results to return  # noqa: E501

        :param top_k: The top_k of this ApplicationResponse.  # noqa: E501
        :type top_k: int
        """
        if self.local_vars_configuration.client_side_validation and top_k is None:  # noqa: E501
            raise ValueError("Invalid value for `top_k`, must not be `None`")  # noqa: E501

        self._top_k = top_k

    @property
    def status(self):
        """Gets the status of this ApplicationResponse.  # noqa: E501


        :return: The status of this ApplicationResponse.  # noqa: E501
        :rtype: ApplicationStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ApplicationResponse.


        :param status: The status of this ApplicationResponse.  # noqa: E501
        :type status: ApplicationStatus
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

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
        if not isinstance(other, ApplicationResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApplicationResponse):
            return True

        return self.to_dict() != other.to_dict()
