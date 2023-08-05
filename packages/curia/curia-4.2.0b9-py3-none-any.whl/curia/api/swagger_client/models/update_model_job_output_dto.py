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

class UpdateModelJobOutputDto(object):
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
        'name': 'object',
        'data': 'object',
        'model_job_id': 'str',
        'dataset_id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'data': 'data',
        'model_job_id': 'modelJobId',
        'dataset_id': 'datasetId'
    }

    def __init__(self, name=None, data=None, model_job_id=None, dataset_id=None):  # noqa: E501
        """UpdateModelJobOutputDto - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._data = None
        self._model_job_id = None
        self._dataset_id = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if data is not None:
            self.data = data
        if model_job_id is not None:
            self.model_job_id = model_job_id
        if dataset_id is not None:
            self.dataset_id = dataset_id

    @property
    def name(self):
        """Gets the name of this UpdateModelJobOutputDto.  # noqa: E501


        :return: The name of this UpdateModelJobOutputDto.  # noqa: E501
        :rtype: object
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpdateModelJobOutputDto.


        :param name: The name of this UpdateModelJobOutputDto.  # noqa: E501
        :type: object
        """

        self._name = name

    @property
    def data(self):
        """Gets the data of this UpdateModelJobOutputDto.  # noqa: E501


        :return: The data of this UpdateModelJobOutputDto.  # noqa: E501
        :rtype: object
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this UpdateModelJobOutputDto.


        :param data: The data of this UpdateModelJobOutputDto.  # noqa: E501
        :type: object
        """

        self._data = data

    @property
    def model_job_id(self):
        """Gets the model_job_id of this UpdateModelJobOutputDto.  # noqa: E501


        :return: The model_job_id of this UpdateModelJobOutputDto.  # noqa: E501
        :rtype: str
        """
        return self._model_job_id

    @model_job_id.setter
    def model_job_id(self, model_job_id):
        """Sets the model_job_id of this UpdateModelJobOutputDto.


        :param model_job_id: The model_job_id of this UpdateModelJobOutputDto.  # noqa: E501
        :type: str
        """

        self._model_job_id = model_job_id

    @property
    def dataset_id(self):
        """Gets the dataset_id of this UpdateModelJobOutputDto.  # noqa: E501


        :return: The dataset_id of this UpdateModelJobOutputDto.  # noqa: E501
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """Sets the dataset_id of this UpdateModelJobOutputDto.


        :param dataset_id: The dataset_id of this UpdateModelJobOutputDto.  # noqa: E501
        :type: str
        """

        self._dataset_id = dataset_id

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
        if issubclass(UpdateModelJobOutputDto, dict):
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
        if not isinstance(other, UpdateModelJobOutputDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
