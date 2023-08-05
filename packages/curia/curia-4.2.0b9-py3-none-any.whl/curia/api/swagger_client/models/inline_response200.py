# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 2.11.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InlineResponse200(object):
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
        'status': 'str',
        'info': 'dict(str, InlineResponse200Info)',
        'error': 'dict(str, InlineResponse200Info)',
        'details': 'dict(str, InlineResponse200Info)'
    }

    attribute_map = {
        'status': 'status',
        'info': 'info',
        'error': 'error',
        'details': 'details'
    }

    def __init__(self, status=None, info=None, error=None, details=None):  # noqa: E501
        """InlineResponse200 - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._info = None
        self._error = None
        self._details = None
        self.discriminator = None
        if status is not None:
            self.status = status
        if info is not None:
            self.info = info
        if error is not None:
            self.error = error
        if details is not None:
            self.details = details

    @property
    def status(self):
        """Gets the status of this InlineResponse200.  # noqa: E501


        :return: The status of this InlineResponse200.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse200.


        :param status: The status of this InlineResponse200.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def info(self):
        """Gets the info of this InlineResponse200.  # noqa: E501


        :return: The info of this InlineResponse200.  # noqa: E501
        :rtype: dict(str, InlineResponse200Info)
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this InlineResponse200.


        :param info: The info of this InlineResponse200.  # noqa: E501
        :type: dict(str, InlineResponse200Info)
        """

        self._info = info

    @property
    def error(self):
        """Gets the error of this InlineResponse200.  # noqa: E501


        :return: The error of this InlineResponse200.  # noqa: E501
        :rtype: dict(str, InlineResponse200Info)
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this InlineResponse200.


        :param error: The error of this InlineResponse200.  # noqa: E501
        :type: dict(str, InlineResponse200Info)
        """

        self._error = error

    @property
    def details(self):
        """Gets the details of this InlineResponse200.  # noqa: E501


        :return: The details of this InlineResponse200.  # noqa: E501
        :rtype: dict(str, InlineResponse200Info)
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this InlineResponse200.


        :param details: The details of this InlineResponse200.  # noqa: E501
        :type: dict(str, InlineResponse200Info)
        """

        self._details = details

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
        if issubclass(InlineResponse200, dict):
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
        if not isinstance(other, InlineResponse200):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
