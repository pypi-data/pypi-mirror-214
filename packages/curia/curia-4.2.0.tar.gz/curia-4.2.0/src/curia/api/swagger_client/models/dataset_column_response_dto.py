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

class DatasetColumnResponseDto(object):
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
        'dataset': 'DatasetColumnJoinedDatasetResponseDto',
        'id': 'str',
        'name': 'str',
        'type': 'str',
        'metadata': 'str',
        'dataset_id': 'str',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'dataset': 'dataset',
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'metadata': 'metadata',
        'dataset_id': 'datasetId',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version'
    }

    def __init__(self, dataset=None, id=None, name=None, type=None, metadata=None, dataset_id=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None):  # noqa: E501
        """DatasetColumnResponseDto - a model defined in Swagger"""  # noqa: E501
        self._dataset = None
        self._id = None
        self._name = None
        self._type = None
        self._metadata = None
        self._dataset_id = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self.discriminator = None
        if dataset is not None:
            self.dataset = dataset
        if id is not None:
            self.id = id
        self.name = name
        self.type = type
        if metadata is not None:
            self.metadata = metadata
        self.dataset_id = dataset_id
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
    def dataset(self):
        """Gets the dataset of this DatasetColumnResponseDto.  # noqa: E501


        :return: The dataset of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: DatasetColumnJoinedDatasetResponseDto
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this DatasetColumnResponseDto.


        :param dataset: The dataset of this DatasetColumnResponseDto.  # noqa: E501
        :type: DatasetColumnJoinedDatasetResponseDto
        """

        self._dataset = dataset

    @property
    def id(self):
        """Gets the id of this DatasetColumnResponseDto.  # noqa: E501


        :return: The id of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this DatasetColumnResponseDto.


        :param id: The id of this DatasetColumnResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this DatasetColumnResponseDto.  # noqa: E501


        :return: The name of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DatasetColumnResponseDto.


        :param name: The name of this DatasetColumnResponseDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this DatasetColumnResponseDto.  # noqa: E501


        :return: The type of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DatasetColumnResponseDto.


        :param type: The type of this DatasetColumnResponseDto.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def metadata(self):
        """Gets the metadata of this DatasetColumnResponseDto.  # noqa: E501


        :return: The metadata of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this DatasetColumnResponseDto.


        :param metadata: The metadata of this DatasetColumnResponseDto.  # noqa: E501
        :type: str
        """

        self._metadata = metadata

    @property
    def dataset_id(self):
        """Gets the dataset_id of this DatasetColumnResponseDto.  # noqa: E501


        :return: The dataset_id of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """Sets the dataset_id of this DatasetColumnResponseDto.


        :param dataset_id: The dataset_id of this DatasetColumnResponseDto.  # noqa: E501
        :type: str
        """
        if dataset_id is None:
            raise ValueError("Invalid value for `dataset_id`, must not be `None`")  # noqa: E501

        self._dataset_id = dataset_id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this DatasetColumnResponseDto.  # noqa: E501


        :return: The last_updated_by of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this DatasetColumnResponseDto.


        :param last_updated_by: The last_updated_by of this DatasetColumnResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this DatasetColumnResponseDto.  # noqa: E501


        :return: The created_by of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this DatasetColumnResponseDto.


        :param created_by: The created_by of this DatasetColumnResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this DatasetColumnResponseDto.  # noqa: E501


        :return: The created_at of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this DatasetColumnResponseDto.


        :param created_at: The created_at of this DatasetColumnResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this DatasetColumnResponseDto.  # noqa: E501


        :return: The updated_at of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this DatasetColumnResponseDto.


        :param updated_at: The updated_at of this DatasetColumnResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this DatasetColumnResponseDto.  # noqa: E501


        :return: The archived_at of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this DatasetColumnResponseDto.


        :param archived_at: The archived_at of this DatasetColumnResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this DatasetColumnResponseDto.  # noqa: E501


        :return: The version of this DatasetColumnResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DatasetColumnResponseDto.


        :param version: The version of this DatasetColumnResponseDto.  # noqa: E501
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
        if issubclass(DatasetColumnResponseDto, dict):
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
        if not isinstance(other, DatasetColumnResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
