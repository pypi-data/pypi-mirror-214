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

class FeatureJoinedFeatureSubCategoryResponseDto(object):
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
        'feature_category': 'FeatureJoinedFeatureSubCategoryJoinedFeatureCategoryResponseDto',
        'id': 'str',
        'name': 'str',
        'feature_category_id': 'str',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'feature_category': 'featureCategory',
        'id': 'id',
        'name': 'name',
        'feature_category_id': 'featureCategoryId',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version'
    }

    def __init__(self, feature_category=None, id=None, name=None, feature_category_id=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None):  # noqa: E501
        """FeatureJoinedFeatureSubCategoryResponseDto - a model defined in Swagger"""  # noqa: E501
        self._feature_category = None
        self._id = None
        self._name = None
        self._feature_category_id = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self.discriminator = None
        if feature_category is not None:
            self.feature_category = feature_category
        if id is not None:
            self.id = id
        self.name = name
        self.feature_category_id = feature_category_id
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
    def feature_category(self):
        """Gets the feature_category of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The feature_category of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: FeatureJoinedFeatureSubCategoryJoinedFeatureCategoryResponseDto
        """
        return self._feature_category

    @feature_category.setter
    def feature_category(self, feature_category):
        """Sets the feature_category of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param feature_category: The feature_category of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: FeatureJoinedFeatureSubCategoryJoinedFeatureCategoryResponseDto
        """

        self._feature_category = feature_category

    @property
    def id(self):
        """Gets the id of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The id of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param id: The id of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The name of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param name: The name of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def feature_category_id(self):
        """Gets the feature_category_id of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The feature_category_id of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._feature_category_id

    @feature_category_id.setter
    def feature_category_id(self, feature_category_id):
        """Sets the feature_category_id of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param feature_category_id: The feature_category_id of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: str
        """
        if feature_category_id is None:
            raise ValueError("Invalid value for `feature_category_id`, must not be `None`")  # noqa: E501

        self._feature_category_id = feature_category_id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The last_updated_by of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param last_updated_by: The last_updated_by of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The created_by of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param created_by: The created_by of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The created_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param created_at: The created_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The updated_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param updated_at: The updated_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The archived_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param archived_at: The archived_at of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501


        :return: The version of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this FeatureJoinedFeatureSubCategoryResponseDto.


        :param version: The version of this FeatureJoinedFeatureSubCategoryResponseDto.  # noqa: E501
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
        if issubclass(FeatureJoinedFeatureSubCategoryResponseDto, dict):
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
        if not isinstance(other, FeatureJoinedFeatureSubCategoryResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
