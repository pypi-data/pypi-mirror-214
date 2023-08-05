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

class ModelPopulationJoinedFeatureResponseDto(object):
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
        'id': 'str',
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
        'type': 'str',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
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
        'type': 'type',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version'
    }

    def __init__(self, id=None, column_name=None, column_alias=None, display_name=None, feature_sub_category_id=None, aggregation_type=None, is_filter=None, is_trainable=None, is_explainable=None, is_categorical=None, category_values=None, type=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None):  # noqa: E501
        """ModelPopulationJoinedFeatureResponseDto - a model defined in Swagger"""  # noqa: E501
        self._id = None
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
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.column_name = column_name
        self.column_alias = column_alias
        self.display_name = display_name
        self.feature_sub_category_id = feature_sub_category_id
        self.aggregation_type = aggregation_type
        self.is_filter = is_filter
        self.is_trainable = is_trainable
        self.is_explainable = is_explainable
        self.is_categorical = is_categorical
        if category_values is not None:
            self.category_values = category_values
        self.type = type
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_by is not None:
            self.created_by = created_by
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if archived_at is not None:
            self.archived_at = archived_at
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The id of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelPopulationJoinedFeatureResponseDto.


        :param id: The id of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def column_name(self):
        """Gets the column_name of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The column_name of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._column_name

    @column_name.setter
    def column_name(self, column_name):
        """Sets the column_name of this ModelPopulationJoinedFeatureResponseDto.


        :param column_name: The column_name of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """
        if column_name is None:
            raise ValueError("Invalid value for `column_name`, must not be `None`")  # noqa: E501

        self._column_name = column_name

    @property
    def column_alias(self):
        """Gets the column_alias of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The column_alias of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._column_alias

    @column_alias.setter
    def column_alias(self, column_alias):
        """Sets the column_alias of this ModelPopulationJoinedFeatureResponseDto.


        :param column_alias: The column_alias of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """
        if column_alias is None:
            raise ValueError("Invalid value for `column_alias`, must not be `None`")  # noqa: E501

        self._column_alias = column_alias

    @property
    def display_name(self):
        """Gets the display_name of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The display_name of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this ModelPopulationJoinedFeatureResponseDto.


        :param display_name: The display_name of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """
        if display_name is None:
            raise ValueError("Invalid value for `display_name`, must not be `None`")  # noqa: E501

        self._display_name = display_name

    @property
    def feature_sub_category_id(self):
        """Gets the feature_sub_category_id of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The feature_sub_category_id of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._feature_sub_category_id

    @feature_sub_category_id.setter
    def feature_sub_category_id(self, feature_sub_category_id):
        """Sets the feature_sub_category_id of this ModelPopulationJoinedFeatureResponseDto.


        :param feature_sub_category_id: The feature_sub_category_id of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """
        if feature_sub_category_id is None:
            raise ValueError("Invalid value for `feature_sub_category_id`, must not be `None`")  # noqa: E501

        self._feature_sub_category_id = feature_sub_category_id

    @property
    def aggregation_type(self):
        """Gets the aggregation_type of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The aggregation_type of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._aggregation_type

    @aggregation_type.setter
    def aggregation_type(self, aggregation_type):
        """Sets the aggregation_type of this ModelPopulationJoinedFeatureResponseDto.


        :param aggregation_type: The aggregation_type of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """
        if aggregation_type is None:
            raise ValueError("Invalid value for `aggregation_type`, must not be `None`")  # noqa: E501
        allowed_values = ["avg", "sum"]  # noqa: E501
        if aggregation_type not in allowed_values:
            raise ValueError(
                "Invalid value for `aggregation_type` ({0}), must be one of {1}"  # noqa: E501
                .format(aggregation_type, allowed_values)
            )

        self._aggregation_type = aggregation_type

    @property
    def is_filter(self):
        """Gets the is_filter of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The is_filter of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_filter

    @is_filter.setter
    def is_filter(self, is_filter):
        """Sets the is_filter of this ModelPopulationJoinedFeatureResponseDto.


        :param is_filter: The is_filter of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: bool
        """
        if is_filter is None:
            raise ValueError("Invalid value for `is_filter`, must not be `None`")  # noqa: E501

        self._is_filter = is_filter

    @property
    def is_trainable(self):
        """Gets the is_trainable of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The is_trainable of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_trainable

    @is_trainable.setter
    def is_trainable(self, is_trainable):
        """Sets the is_trainable of this ModelPopulationJoinedFeatureResponseDto.


        :param is_trainable: The is_trainable of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: bool
        """
        if is_trainable is None:
            raise ValueError("Invalid value for `is_trainable`, must not be `None`")  # noqa: E501

        self._is_trainable = is_trainable

    @property
    def is_explainable(self):
        """Gets the is_explainable of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The is_explainable of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_explainable

    @is_explainable.setter
    def is_explainable(self, is_explainable):
        """Sets the is_explainable of this ModelPopulationJoinedFeatureResponseDto.


        :param is_explainable: The is_explainable of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: bool
        """
        if is_explainable is None:
            raise ValueError("Invalid value for `is_explainable`, must not be `None`")  # noqa: E501

        self._is_explainable = is_explainable

    @property
    def is_categorical(self):
        """Gets the is_categorical of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The is_categorical of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: bool
        """
        return self._is_categorical

    @is_categorical.setter
    def is_categorical(self, is_categorical):
        """Sets the is_categorical of this ModelPopulationJoinedFeatureResponseDto.


        :param is_categorical: The is_categorical of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: bool
        """
        if is_categorical is None:
            raise ValueError("Invalid value for `is_categorical`, must not be `None`")  # noqa: E501

        self._is_categorical = is_categorical

    @property
    def category_values(self):
        """Gets the category_values of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The category_values of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: object
        """
        return self._category_values

    @category_values.setter
    def category_values(self, category_values):
        """Sets the category_values of this ModelPopulationJoinedFeatureResponseDto.


        :param category_values: The category_values of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: object
        """

        self._category_values = category_values

    @property
    def type(self):
        """Gets the type of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The type of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ModelPopulationJoinedFeatureResponseDto.


        :param type: The type of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["string", "numeric"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The last_updated_by of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ModelPopulationJoinedFeatureResponseDto.


        :param last_updated_by: The last_updated_by of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The created_by of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ModelPopulationJoinedFeatureResponseDto.


        :param created_by: The created_by of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The created_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelPopulationJoinedFeatureResponseDto.


        :param created_at: The created_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The updated_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelPopulationJoinedFeatureResponseDto.


        :param updated_at: The updated_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The archived_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this ModelPopulationJoinedFeatureResponseDto.


        :param archived_at: The archived_at of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501


        :return: The version of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelPopulationJoinedFeatureResponseDto.


        :param version: The version of this ModelPopulationJoinedFeatureResponseDto.  # noqa: E501
        :type: float
        """

        self._version = version

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
        if issubclass(ModelPopulationJoinedFeatureResponseDto, dict):
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
        if not isinstance(other, ModelPopulationJoinedFeatureResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
