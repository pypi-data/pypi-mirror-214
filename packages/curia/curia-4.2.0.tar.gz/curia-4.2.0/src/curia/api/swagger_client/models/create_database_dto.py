# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 3.8.1-develop.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CreateDatabaseDto(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'description': 'str',
        'location': 'str',
        'last_synced_at': 'datetime'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'location': 'location',
        'last_synced_at': 'lastSyncedAt'
    }

    def __init__(self, name=None, description=None, location=None, last_synced_at=None):  # noqa: E501
        """CreateDatabaseDto - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._description = None
        self._location = None
        self._last_synced_at = None
        self.discriminator = None
        self.name = name
        if description is not None:
            self.description = description
        if location is not None:
            self.location = location
        if last_synced_at is not None:
            self.last_synced_at = last_synced_at

    @property
    def name(self):
        """Gets the name of this CreateDatabaseDto.  # noqa: E501


        :return: The name of this CreateDatabaseDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateDatabaseDto.


        :param name: The name of this CreateDatabaseDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this CreateDatabaseDto.  # noqa: E501


        :return: The description of this CreateDatabaseDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CreateDatabaseDto.


        :param description: The description of this CreateDatabaseDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def location(self):
        """Gets the location of this CreateDatabaseDto.  # noqa: E501


        :return: The location of this CreateDatabaseDto.  # noqa: E501
        :rtype: str
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this CreateDatabaseDto.


        :param location: The location of this CreateDatabaseDto.  # noqa: E501
        :type: str
        """

        self._location = location

    @property
    def last_synced_at(self):
        """Gets the last_synced_at of this CreateDatabaseDto.  # noqa: E501


        :return: The last_synced_at of this CreateDatabaseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._last_synced_at

    @last_synced_at.setter
    def last_synced_at(self, last_synced_at):
        """Sets the last_synced_at of this CreateDatabaseDto.


        :param last_synced_at: The last_synced_at of this CreateDatabaseDto.  # noqa: E501
        :type: datetime
        """

        self._last_synced_at = last_synced_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(CreateDatabaseDto, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateDatabaseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
