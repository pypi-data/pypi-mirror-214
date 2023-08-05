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


class ResponseGetApplicationDetail(object):
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
        'status': 'ApplicationStatus',
        'destination_id': 'str',
        'embedding_count': 'int',
        'template': 'Template',
        'chatgpt_name': 'str',
        'chatgpt_description': 'str',
        'chatgpt_query_description': 'str',
        'chatgpt_info_description': 'str',
        'logo_url': 'str',
        'contact_email_address': 'str',
        'legal_info_url': 'str',
        'access_token': 'str',
        'saved_response_enabled': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'created_at': 'created_at',
        'name': 'name',
        'description': 'description',
        'top_k': 'top_k',
        'status': 'status',
        'destination_id': 'destination_id',
        'embedding_count': 'embedding_count',
        'template': 'template',
        'chatgpt_name': 'chatgpt_name',
        'chatgpt_description': 'chatgpt_description',
        'chatgpt_query_description': 'chatgpt_query_description',
        'chatgpt_info_description': 'chatgpt_info_description',
        'logo_url': 'logo_url',
        'contact_email_address': 'contact_email_address',
        'legal_info_url': 'legal_info_url',
        'access_token': 'access_token',
        'saved_response_enabled': 'saved_response_enabled'
    }

    def __init__(self, id=None, created_at=None, name=None, description=None, top_k=None, status=None, destination_id=None, embedding_count=0, template=None, chatgpt_name=None, chatgpt_description=None, chatgpt_query_description=None, chatgpt_info_description=None, logo_url=None, contact_email_address=None, legal_info_url=None, access_token=None, saved_response_enabled=None, local_vars_configuration=None):  # noqa: E501
        """ResponseGetApplicationDetail - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._created_at = None
        self._name = None
        self._description = None
        self._top_k = None
        self._status = None
        self._destination_id = None
        self._embedding_count = None
        self._template = None
        self._chatgpt_name = None
        self._chatgpt_description = None
        self._chatgpt_query_description = None
        self._chatgpt_info_description = None
        self._logo_url = None
        self._contact_email_address = None
        self._legal_info_url = None
        self._access_token = None
        self._saved_response_enabled = None
        self.discriminator = None

        self.id = id
        self.created_at = created_at
        self.name = name
        self.description = description
        self.top_k = top_k
        self.status = status
        if destination_id is not None:
            self.destination_id = destination_id
        if embedding_count is not None:
            self.embedding_count = embedding_count
        if template is not None:
            self.template = template
        if chatgpt_name is not None:
            self.chatgpt_name = chatgpt_name
        if chatgpt_description is not None:
            self.chatgpt_description = chatgpt_description
        if chatgpt_query_description is not None:
            self.chatgpt_query_description = chatgpt_query_description
        if chatgpt_info_description is not None:
            self.chatgpt_info_description = chatgpt_info_description
        self.logo_url = logo_url
        self.contact_email_address = contact_email_address
        self.legal_info_url = legal_info_url
        self.access_token = access_token
        self.saved_response_enabled = saved_response_enabled

    @property
    def id(self):
        """Gets the id of this ResponseGetApplicationDetail.  # noqa: E501

        A unique identifier  # noqa: E501

        :return: The id of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ResponseGetApplicationDetail.

        A unique identifier  # noqa: E501

        :param id: The id of this ResponseGetApplicationDetail.  # noqa: E501
        :type id: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_at(self):
        """Gets the created_at of this ResponseGetApplicationDetail.  # noqa: E501

        Date the application was created  # noqa: E501

        :return: The created_at of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ResponseGetApplicationDetail.

        Date the application was created  # noqa: E501

        :param created_at: The created_at of this ResponseGetApplicationDetail.  # noqa: E501
        :type created_at: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def name(self):
        """Gets the name of this ResponseGetApplicationDetail.  # noqa: E501

        Name of the application  # noqa: E501

        :return: The name of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ResponseGetApplicationDetail.

        Name of the application  # noqa: E501

        :param name: The name of this ResponseGetApplicationDetail.  # noqa: E501
        :type name: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this ResponseGetApplicationDetail.  # noqa: E501

        Description of the application  # noqa: E501

        :return: The description of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ResponseGetApplicationDetail.

        Description of the application  # noqa: E501

        :param description: The description of this ResponseGetApplicationDetail.  # noqa: E501
        :type description: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def top_k(self):
        """Gets the top_k of this ResponseGetApplicationDetail.  # noqa: E501

        Number of results to return  # noqa: E501

        :return: The top_k of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: int
        """
        return self._top_k

    @top_k.setter
    def top_k(self, top_k):
        """Sets the top_k of this ResponseGetApplicationDetail.

        Number of results to return  # noqa: E501

        :param top_k: The top_k of this ResponseGetApplicationDetail.  # noqa: E501
        :type top_k: int
        """
        if self.local_vars_configuration.client_side_validation and top_k is None:  # noqa: E501
            raise ValueError("Invalid value for `top_k`, must not be `None`")  # noqa: E501

        self._top_k = top_k

    @property
    def status(self):
        """Gets the status of this ResponseGetApplicationDetail.  # noqa: E501


        :return: The status of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: ApplicationStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ResponseGetApplicationDetail.


        :param status: The status of this ResponseGetApplicationDetail.  # noqa: E501
        :type status: ApplicationStatus
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def destination_id(self):
        """Gets the destination_id of this ResponseGetApplicationDetail.  # noqa: E501

        Destination identifier  # noqa: E501

        :return: The destination_id of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._destination_id

    @destination_id.setter
    def destination_id(self, destination_id):
        """Sets the destination_id of this ResponseGetApplicationDetail.

        Destination identifier  # noqa: E501

        :param destination_id: The destination_id of this ResponseGetApplicationDetail.  # noqa: E501
        :type destination_id: str
        """

        self._destination_id = destination_id

    @property
    def embedding_count(self):
        """Gets the embedding_count of this ResponseGetApplicationDetail.  # noqa: E501

        Number of embeddings in the destination  # noqa: E501

        :return: The embedding_count of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: int
        """
        return self._embedding_count

    @embedding_count.setter
    def embedding_count(self, embedding_count):
        """Sets the embedding_count of this ResponseGetApplicationDetail.

        Number of embeddings in the destination  # noqa: E501

        :param embedding_count: The embedding_count of this ResponseGetApplicationDetail.  # noqa: E501
        :type embedding_count: int
        """
        if (self.local_vars_configuration.client_side_validation and
                embedding_count is not None and embedding_count < 0):  # noqa: E501
            raise ValueError("Invalid value for `embedding_count`, must be a value greater than or equal to `0`")  # noqa: E501

        self._embedding_count = embedding_count

    @property
    def template(self):
        """Gets the template of this ResponseGetApplicationDetail.  # noqa: E501


        :return: The template of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: Template
        """
        return self._template

    @template.setter
    def template(self, template):
        """Sets the template of this ResponseGetApplicationDetail.


        :param template: The template of this ResponseGetApplicationDetail.  # noqa: E501
        :type template: Template
        """

        self._template = template

    @property
    def chatgpt_name(self):
        """Gets the chatgpt_name of this ResponseGetApplicationDetail.  # noqa: E501

        Name of the application intended for ChatGPT consumption  # noqa: E501

        :return: The chatgpt_name of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._chatgpt_name

    @chatgpt_name.setter
    def chatgpt_name(self, chatgpt_name):
        """Sets the chatgpt_name of this ResponseGetApplicationDetail.

        Name of the application intended for ChatGPT consumption  # noqa: E501

        :param chatgpt_name: The chatgpt_name of this ResponseGetApplicationDetail.  # noqa: E501
        :type chatgpt_name: str
        """

        self._chatgpt_name = chatgpt_name

    @property
    def chatgpt_description(self):
        """Gets the chatgpt_description of this ResponseGetApplicationDetail.  # noqa: E501

        Description of the application intended for ChatGPT consumption. This is a prompt  # noqa: E501

        :return: The chatgpt_description of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._chatgpt_description

    @chatgpt_description.setter
    def chatgpt_description(self, chatgpt_description):
        """Sets the chatgpt_description of this ResponseGetApplicationDetail.

        Description of the application intended for ChatGPT consumption. This is a prompt  # noqa: E501

        :param chatgpt_description: The chatgpt_description of this ResponseGetApplicationDetail.  # noqa: E501
        :type chatgpt_description: str
        """

        self._chatgpt_description = chatgpt_description

    @property
    def chatgpt_query_description(self):
        """Gets the chatgpt_query_description of this ResponseGetApplicationDetail.  # noqa: E501

        The description used in the openai.yaml manifest for the /query endpoint  # noqa: E501

        :return: The chatgpt_query_description of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._chatgpt_query_description

    @chatgpt_query_description.setter
    def chatgpt_query_description(self, chatgpt_query_description):
        """Sets the chatgpt_query_description of this ResponseGetApplicationDetail.

        The description used in the openai.yaml manifest for the /query endpoint  # noqa: E501

        :param chatgpt_query_description: The chatgpt_query_description of this ResponseGetApplicationDetail.  # noqa: E501
        :type chatgpt_query_description: str
        """

        self._chatgpt_query_description = chatgpt_query_description

    @property
    def chatgpt_info_description(self):
        """Gets the chatgpt_info_description of this ResponseGetApplicationDetail.  # noqa: E501

        The top-level description used in the openai.yaml manifest  # noqa: E501

        :return: The chatgpt_info_description of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._chatgpt_info_description

    @chatgpt_info_description.setter
    def chatgpt_info_description(self, chatgpt_info_description):
        """Sets the chatgpt_info_description of this ResponseGetApplicationDetail.

        The top-level description used in the openai.yaml manifest  # noqa: E501

        :param chatgpt_info_description: The chatgpt_info_description of this ResponseGetApplicationDetail.  # noqa: E501
        :type chatgpt_info_description: str
        """

        self._chatgpt_info_description = chatgpt_info_description

    @property
    def logo_url(self):
        """Gets the logo_url of this ResponseGetApplicationDetail.  # noqa: E501

        URL of the application logo  # noqa: E501

        :return: The logo_url of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._logo_url

    @logo_url.setter
    def logo_url(self, logo_url):
        """Sets the logo_url of this ResponseGetApplicationDetail.

        URL of the application logo  # noqa: E501

        :param logo_url: The logo_url of this ResponseGetApplicationDetail.  # noqa: E501
        :type logo_url: str
        """
        if self.local_vars_configuration.client_side_validation and logo_url is None:  # noqa: E501
            raise ValueError("Invalid value for `logo_url`, must not be `None`")  # noqa: E501

        self._logo_url = logo_url

    @property
    def contact_email_address(self):
        """Gets the contact_email_address of this ResponseGetApplicationDetail.  # noqa: E501

        Contact email address for the plugin  # noqa: E501

        :return: The contact_email_address of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._contact_email_address

    @contact_email_address.setter
    def contact_email_address(self, contact_email_address):
        """Sets the contact_email_address of this ResponseGetApplicationDetail.

        Contact email address for the plugin  # noqa: E501

        :param contact_email_address: The contact_email_address of this ResponseGetApplicationDetail.  # noqa: E501
        :type contact_email_address: str
        """
        if self.local_vars_configuration.client_side_validation and contact_email_address is None:  # noqa: E501
            raise ValueError("Invalid value for `contact_email_address`, must not be `None`")  # noqa: E501

        self._contact_email_address = contact_email_address

    @property
    def legal_info_url(self):
        """Gets the legal_info_url of this ResponseGetApplicationDetail.  # noqa: E501

        URL to the legal information for the plugin  # noqa: E501

        :return: The legal_info_url of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._legal_info_url

    @legal_info_url.setter
    def legal_info_url(self, legal_info_url):
        """Sets the legal_info_url of this ResponseGetApplicationDetail.

        URL to the legal information for the plugin  # noqa: E501

        :param legal_info_url: The legal_info_url of this ResponseGetApplicationDetail.  # noqa: E501
        :type legal_info_url: str
        """
        if self.local_vars_configuration.client_side_validation and legal_info_url is None:  # noqa: E501
            raise ValueError("Invalid value for `legal_info_url`, must not be `None`")  # noqa: E501

        self._legal_info_url = legal_info_url

    @property
    def access_token(self):
        """Gets the access_token of this ResponseGetApplicationDetail.  # noqa: E501

        Access token for the plugin  # noqa: E501

        :return: The access_token of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: str
        """
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        """Sets the access_token of this ResponseGetApplicationDetail.

        Access token for the plugin  # noqa: E501

        :param access_token: The access_token of this ResponseGetApplicationDetail.  # noqa: E501
        :type access_token: str
        """
        if self.local_vars_configuration.client_side_validation and access_token is None:  # noqa: E501
            raise ValueError("Invalid value for `access_token`, must not be `None`")  # noqa: E501

        self._access_token = access_token

    @property
    def saved_response_enabled(self):
        """Gets the saved_response_enabled of this ResponseGetApplicationDetail.  # noqa: E501

        Whether saved responses are enabled  # noqa: E501

        :return: The saved_response_enabled of this ResponseGetApplicationDetail.  # noqa: E501
        :rtype: bool
        """
        return self._saved_response_enabled

    @saved_response_enabled.setter
    def saved_response_enabled(self, saved_response_enabled):
        """Sets the saved_response_enabled of this ResponseGetApplicationDetail.

        Whether saved responses are enabled  # noqa: E501

        :param saved_response_enabled: The saved_response_enabled of this ResponseGetApplicationDetail.  # noqa: E501
        :type saved_response_enabled: bool
        """
        if self.local_vars_configuration.client_side_validation and saved_response_enabled is None:  # noqa: E501
            raise ValueError("Invalid value for `saved_response_enabled`, must not be `None`")  # noqa: E501

        self._saved_response_enabled = saved_response_enabled

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
        if not isinstance(other, ResponseGetApplicationDetail):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResponseGetApplicationDetail):
            return True

        return self.to_dict() != other.to_dict()
