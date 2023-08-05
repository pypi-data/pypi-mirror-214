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

class Condition(object):
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
        'field': 'str',
        'operator': 'object',
        'value': 'object'
    }

    attribute_map = {
        'field': 'field',
        'operator': 'operator',
        'value': 'value'
    }

    def __init__(self, field=None, operator=None, value=None):  # noqa: E501
        """Condition - a model defined in Swagger"""  # noqa: E501
        self._field = None
        self._operator = None
        self._value = None
        self.discriminator = None
        self.field = field
        if operator is not None:
            self.operator = operator
        self.value = value

    @property
    def field(self):
        """Gets the field of this Condition.  # noqa: E501


        :return: The field of this Condition.  # noqa: E501
        :rtype: str
        """
        return self._field

    @field.setter
    def field(self, field):
        """Sets the field of this Condition.


        :param field: The field of this Condition.  # noqa: E501
        :type: str
        """
        if field is None:
            raise ValueError("Invalid value for `field`, must not be `None`")  # noqa: E501

        self._field = field

    @property
    def operator(self):
        """Gets the operator of this Condition.  # noqa: E501


        :return: The operator of this Condition.  # noqa: E501
        :rtype: object
        """
        return self._operator

    @operator.setter
    def operator(self, operator):
        """Sets the operator of this Condition.


        :param operator: The operator of this Condition.  # noqa: E501
        :type: object
        """

        self._operator = operator

    @property
    def value(self):
        """Gets the value of this Condition.  # noqa: E501


        :return: The value of this Condition.  # noqa: E501
        :rtype: object
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Condition.


        :param value: The value of this Condition.  # noqa: E501
        :type: object
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

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
        if issubclass(Condition, dict):
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
        if not isinstance(other, Condition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
