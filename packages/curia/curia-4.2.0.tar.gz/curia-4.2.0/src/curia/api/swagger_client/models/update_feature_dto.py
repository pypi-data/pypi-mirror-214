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

class UpdateFeatureDto(object):
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
        'column_name': 'str',
        'column_alias': 'str',
        'display_name': 'str',
        'feature_sub_category_id': 'str',
        'aggregation_type': 'str',
        'is_filter': 'bool',
        'is_trainable': 'bool',
        'is_explainable': 'bool',
        'is_categorical': 'bool',
        'category_values': 'object',
        'type': 'str'
    }

    attribute_map = {
        'column_name': 'columnName',
        'column_alias': 'columnAlias',
        'display_name': 'displayName',
        'feature_sub_category_id': 'featureSubCategoryId',
        'aggregation_type': 'aggregationType',
        'is_filter': 'isFilter',
        'is_trainable': 'isTrainable',
        'is_explainable': 'isExplainable',
        'is_categorical': 'isCategorical',
        'category_values': 'categoryValues',
        'type': 'type'
    }

    def __init__(self, column_name=None, column_alias=None, display_name=None, feature_sub_category_id=None, aggregation_type=None, is_filter=None, is_trainable=None, is_explainable=None, is_categorical=None, category_values=None, type=None):  # noqa: E501
        """UpdateFeatureDto - a model defined in Swagger"""  # noqa: E501
        self._column_name = None
        self._column_alias = None
        self._display_name = None
        self._feature_sub_category_id = None
        self._aggregation_type = None
        self._is_filter = None
        self._is_trainable = None
        self._is_explainable = None
        self._is_categorical = None
        self._category_values = None
        self._type = None
        self.discriminator = None
        if column_name is not None:
            self.column_name = column_name
        if column_alias is not None:
            self.column_alias = column_alias
        if display_name is not None:
            self.display_name = display_name
        if feature_sub_category_id is not None:
            self.feature_sub_category_id = feature_sub_category_id
        if aggregation_type is not None:
            self.aggregation_type = aggregation_type
        if is_filter is not None:
            self.is_filter = is_filter
        if is_trainable is not None:
            self.is_trainable = is_trainable
        if is_explainable is not None:
            self.is_explainable = is_explainable
        if is_categorical is not None:
            self.is_categorical = is_categorical
        if category_values is not None:
            self.category_values = category_values
        if type is not None:
            self.type = type

    @property
    def column_name(self):
        """Gets the column_name of this UpdateFeatureDto.  # noqa: E501


        :return: The column_name of this UpdateFeatureDto.  # noqa: E501
        :rtype: str
        """
        return self._column_name

    @column_name.setter
    def column_name(self, column_name):
        """Sets the column_name of this UpdateFeatureDto.


        :param column_name: The column_name of this UpdateFeatureDto.  # noqa: E501
        :type: str
        """

        self._column_name = column_name

    @property
    def column_alias(self):
        """Gets the column_alias of this UpdateFeatureDto.  # noqa: E501


        :return: The column_alias of this UpdateFeatureDto.  # noqa: E501
        :rtype: str
        """
        return self._column_alias

    @column_alias.setter
    def column_alias(self, column_alias):
        """Sets the column_alias of this UpdateFeatureDto.


        :param column_alias: The column_alias of this UpdateFeatureDto.  # noqa: E501
        :type: str
        """

        self._column_alias = column_alias

    @property
    def display_name(self):
        """Gets the display_name of this UpdateFeatureDto.  # noqa: E501


        :return: The display_name of this UpdateFeatureDto.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this UpdateFeatureDto.


        :param display_name: The display_name of this UpdateFeatureDto.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def feature_sub_category_id(self):
        """Gets the feature_sub_category_id of this UpdateFeatureDto.  # noqa: E501


        :return: The feature_sub_category_id of this UpdateFeatureDto.  # noqa: E501
        :rtype: str
        """
        return self._feature_sub_category_id

    @feature_sub_category_id.setter
    def feature_sub_category_id(self, feature_sub_category_id):
        """Sets the feature_sub_category_id of this UpdateFeatureDto.


        :param feature_sub_category_id: The feature_sub_category_id of this UpdateFeatureDto.  # noqa: E501
        :type: str
        """

        self._feature_sub_category_id = feature_sub_category_id

    @property
    def aggregation_type(self):
        """Gets the aggregation_type of this UpdateFeatureDto.  # noqa: E501


        :return: The aggregation_type of this UpdateFeatureDto.  # noqa: E501
        :rtype: str
        """
        return self._aggregation_type

    @aggregation_type.setter
    def aggregation_type(self, aggregation_type):
        """Sets the aggregation_type of this UpdateFeatureDto.


        :param aggregation_type: The aggregation_type of this UpdateFeatureDto.  # noqa: E501
        :type: str
        """
        allowed_values = ["avg", "sum"]  # noqa: E501
        if aggregation_type not in allowed_values:
            raise ValueError(
                "Invalid value for `aggregation_type` ({0}), must be one of {1}"  # noqa: E501
                .format(aggregation_type, allowed_values)
            )

        self._aggregation_type = aggregation_type

    @property
    def is_filter(self):
        """Gets the is_filter of this UpdateFeatureDto.  # noqa: E501


        :return: The is_filter of this UpdateFeatureDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_filter

    @is_filter.setter
    def is_filter(self, is_filter):
        """Sets the is_filter of this UpdateFeatureDto.


        :param is_filter: The is_filter of this UpdateFeatureDto.  # noqa: E501
        :type: bool
        """

        self._is_filter = is_filter

    @property
    def is_trainable(self):
        """Gets the is_trainable of this UpdateFeatureDto.  # noqa: E501


        :return: The is_trainable of this UpdateFeatureDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_trainable

    @is_trainable.setter
    def is_trainable(self, is_trainable):
        """Sets the is_trainable of this UpdateFeatureDto.


        :param is_trainable: The is_trainable of this UpdateFeatureDto.  # noqa: E501
        :type: bool
        """

        self._is_trainable = is_trainable

    @property
    def is_explainable(self):
        """Gets the is_explainable of this UpdateFeatureDto.  # noqa: E501


        :return: The is_explainable of this UpdateFeatureDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_explainable

    @is_explainable.setter
    def is_explainable(self, is_explainable):
        """Sets the is_explainable of this UpdateFeatureDto.


        :param is_explainable: The is_explainable of this UpdateFeatureDto.  # noqa: E501
        :type: bool
        """

        self._is_explainable = is_explainable

    @property
    def is_categorical(self):
        """Gets the is_categorical of this UpdateFeatureDto.  # noqa: E501


        :return: The is_categorical of this UpdateFeatureDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_categorical

    @is_categorical.setter
    def is_categorical(self, is_categorical):
        """Sets the is_categorical of this UpdateFeatureDto.


        :param is_categorical: The is_categorical of this UpdateFeatureDto.  # noqa: E501
        :type: bool
        """

        self._is_categorical = is_categorical

    @property
    def category_values(self):
        """Gets the category_values of this UpdateFeatureDto.  # noqa: E501


        :return: The category_values of this UpdateFeatureDto.  # noqa: E501
        :rtype: object
        """
        return self._category_values

    @category_values.setter
    def category_values(self, category_values):
        """Sets the category_values of this UpdateFeatureDto.


        :param category_values: The category_values of this UpdateFeatureDto.  # noqa: E501
        :type: object
        """

        self._category_values = category_values

    @property
    def type(self):
        """Gets the type of this UpdateFeatureDto.  # noqa: E501


        :return: The type of this UpdateFeatureDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UpdateFeatureDto.


        :param type: The type of this UpdateFeatureDto.  # noqa: E501
        :type: str
        """
        allowed_values = ["string", "numeric"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(UpdateFeatureDto, dict):
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
        if not isinstance(other, UpdateFeatureDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
