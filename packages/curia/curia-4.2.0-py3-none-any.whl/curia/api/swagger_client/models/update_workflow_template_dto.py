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

class UpdateWorkflowTemplateDto(object):
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
        'parameters': 'WorkflowTemplateParameters',
        'definition': 'WorkflowTemplateDefinition'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'parameters': 'parameters',
        'definition': 'definition'
    }

    def __init__(self, name=None, description=None, parameters=None, definition=None):  # noqa: E501
        """UpdateWorkflowTemplateDto - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._description = None
        self._parameters = None
        self._definition = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if parameters is not None:
            self.parameters = parameters
        if definition is not None:
            self.definition = definition

    @property
    def name(self):
        """Gets the name of this UpdateWorkflowTemplateDto.  # noqa: E501


        :return: The name of this UpdateWorkflowTemplateDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateWorkflowTemplateDto.


        :param name: The name of this UpdateWorkflowTemplateDto.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this UpdateWorkflowTemplateDto.  # noqa: E501


        :return: The description of this UpdateWorkflowTemplateDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this UpdateWorkflowTemplateDto.


        :param description: The description of this UpdateWorkflowTemplateDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def parameters(self):
        """Gets the parameters of this UpdateWorkflowTemplateDto.  # noqa: E501


        :return: The parameters of this UpdateWorkflowTemplateDto.  # noqa: E501
        :rtype: WorkflowTemplateParameters
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """Sets the parameters of this UpdateWorkflowTemplateDto.


        :param parameters: The parameters of this UpdateWorkflowTemplateDto.  # noqa: E501
        :type: WorkflowTemplateParameters
        """

        self._parameters = parameters

    @property
    def definition(self):
        """Gets the definition of this UpdateWorkflowTemplateDto.  # noqa: E501


        :return: The definition of this UpdateWorkflowTemplateDto.  # noqa: E501
        :rtype: WorkflowTemplateDefinition
        """
        return self._definition

    @definition.setter
    def definition(self, definition):
        """Sets the definition of this UpdateWorkflowTemplateDto.


        :param definition: The definition of this UpdateWorkflowTemplateDto.  # noqa: E501
        :type: WorkflowTemplateDefinition
        """

        self._definition = definition

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
        if issubclass(UpdateWorkflowTemplateDto, dict):
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
        if not isinstance(other, UpdateWorkflowTemplateDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
