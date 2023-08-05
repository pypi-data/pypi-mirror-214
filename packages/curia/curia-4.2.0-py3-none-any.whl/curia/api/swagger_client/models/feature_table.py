# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 2.4.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class FeatureTable(object):
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
        'table_name': 'str',
        'table_alias': 'str',
        'has_date': 'bool',
        'foreign_table_alias': 'str',
        'foreign_key': 'str',
        'join_where': 'str',
        'self_key': 'str',
        'last_updated_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'table_name': 'tableName',
        'table_alias': 'tableAlias',
        'has_date': 'hasDate',
        'foreign_table_alias': 'foreignTableAlias',
        'foreign_key': 'foreignKey',
        'join_where': 'joinWhere',
        'self_key': 'selfKey',
        'last_updated_by': 'lastUpdatedBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version'
    }

    def __init__(self, id=None, table_name=None, table_alias=None, has_date=None, foreign_table_alias=None, foreign_key=None, join_where=None, self_key=None, last_updated_by=None, created_at=None, updated_at=None, archived_at=None, version=None):  # noqa: E501
        """FeatureTable - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._table_name = None
        self._table_alias = None
        self._has_date = None
        self._foreign_table_alias = None
        self._foreign_key = None
        self._join_where = None
        self._self_key = None
        self._last_updated_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        self.table_name = table_name
        self.table_alias = table_alias
        self.has_date = has_date
        self.foreign_table_alias = foreign_table_alias
        self.foreign_key = foreign_key
        if join_where is not None:
            self.join_where = join_where
        self.self_key = self_key
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
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
        """Gets the id of this FeatureTable.  # noqa: E501


        :return: The id of this FeatureTable.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FeatureTable.


        :param id: The id of this FeatureTable.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def table_name(self):
        """Gets the table_name of this FeatureTable.  # noqa: E501


        :return: The table_name of this FeatureTable.  # noqa: E501
        :rtype: str
        """
        return self._table_name

    @table_name.setter
    def table_name(self, table_name):
        """Sets the table_name of this FeatureTable.


        :param table_name: The table_name of this FeatureTable.  # noqa: E501
        :type: str
        """
        if table_name is None:
            raise ValueError("Invalid value for `table_name`, must not be `None`")  # noqa: E501

        self._table_name = table_name

    @property
    def table_alias(self):
        """Gets the table_alias of this FeatureTable.  # noqa: E501


        :return: The table_alias of this FeatureTable.  # noqa: E501
        :rtype: str
        """
        return self._table_alias

    @table_alias.setter
    def table_alias(self, table_alias):
        """Sets the table_alias of this FeatureTable.


        :param table_alias: The table_alias of this FeatureTable.  # noqa: E501
        :type: str
        """
        if table_alias is None:
            raise ValueError("Invalid value for `table_alias`, must not be `None`")  # noqa: E501

        self._table_alias = table_alias

    @property
    def has_date(self):
        """Gets the has_date of this FeatureTable.  # noqa: E501


        :return: The has_date of this FeatureTable.  # noqa: E501
        :rtype: bool
        """
        return self._has_date

    @has_date.setter
    def has_date(self, has_date):
        """Sets the has_date of this FeatureTable.


        :param has_date: The has_date of this FeatureTable.  # noqa: E501
        :type: bool
        """
        if has_date is None:
            raise ValueError("Invalid value for `has_date`, must not be `None`")  # noqa: E501

        self._has_date = has_date

    @property
    def foreign_table_alias(self):
        """Gets the foreign_table_alias of this FeatureTable.  # noqa: E501


        :return: The foreign_table_alias of this FeatureTable.  # noqa: E501
        :rtype: str
        """
        return self._foreign_table_alias

    @foreign_table_alias.setter
    def foreign_table_alias(self, foreign_table_alias):
        """Sets the foreign_table_alias of this FeatureTable.


        :param foreign_table_alias: The foreign_table_alias of this FeatureTable.  # noqa: E501
        :type: str
        """
        if foreign_table_alias is None:
            raise ValueError("Invalid value for `foreign_table_alias`, must not be `None`")  # noqa: E501

        self._foreign_table_alias = foreign_table_alias

    @property
    def foreign_key(self):
        """Gets the foreign_key of this FeatureTable.  # noqa: E501


        :return: The foreign_key of this FeatureTable.  # noqa: E501
        :rtype: str
        """
        return self._foreign_key

    @foreign_key.setter
    def foreign_key(self, foreign_key):
        """Sets the foreign_key of this FeatureTable.


        :param foreign_key: The foreign_key of this FeatureTable.  # noqa: E501
        :type: str
        """
        if foreign_key is None:
            raise ValueError("Invalid value for `foreign_key`, must not be `None`")  # noqa: E501

        self._foreign_key = foreign_key

    @property
    def join_where(self):
        """Gets the join_where of this FeatureTable.  # noqa: E501


        :return: The join_where of this FeatureTable.  # noqa: E501
        :rtype: str
        """
        return self._join_where

    @join_where.setter
    def join_where(self, join_where):
        """Sets the join_where of this FeatureTable.


        :param join_where: The join_where of this FeatureTable.  # noqa: E501
        :type: str
        """

        self._join_where = join_where

    @property
    def self_key(self):
        """Gets the self_key of this FeatureTable.  # noqa: E501


        :return: The self_key of this FeatureTable.  # noqa: E501
        :rtype: str
        """
        return self._self_key

    @self_key.setter
    def self_key(self, self_key):
        """Sets the self_key of this FeatureTable.


        :param self_key: The self_key of this FeatureTable.  # noqa: E501
        :type: str
        """
        if self_key is None:
            raise ValueError("Invalid value for `self_key`, must not be `None`")  # noqa: E501

        self._self_key = self_key

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this FeatureTable.  # noqa: E501


        :return: The last_updated_by of this FeatureTable.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this FeatureTable.


        :param last_updated_by: The last_updated_by of this FeatureTable.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_at(self):
        """Gets the created_at of this FeatureTable.  # noqa: E501


        :return: The created_at of this FeatureTable.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this FeatureTable.


        :param created_at: The created_at of this FeatureTable.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this FeatureTable.  # noqa: E501


        :return: The updated_at of this FeatureTable.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this FeatureTable.


        :param updated_at: The updated_at of this FeatureTable.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this FeatureTable.  # noqa: E501


        :return: The archived_at of this FeatureTable.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this FeatureTable.


        :param archived_at: The archived_at of this FeatureTable.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this FeatureTable.  # noqa: E501


        :return: The version of this FeatureTable.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this FeatureTable.


        :param version: The version of this FeatureTable.  # noqa: E501
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
        if issubclass(FeatureTable, dict):
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
        if not isinstance(other, FeatureTable):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
