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

class ModelResponseDto(object):
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
        'project': 'ModelJoinedProjectResponseDto',
        'model_jobs': 'ModelJoinedModelJobResponseDto',
        'cohorts': 'ModelJoinedCohortResponseDto',
        'user_favorites': 'ModelJoinedUserFavoriteResponseDto',
        'model_output_details': 'ModelJoinedModelOutputDetailsResponseDto',
        'id': 'str',
        'name': 'str',
        'type': 'str',
        'outcome_type': 'str',
        'feature_store': 'str',
        'description': 'str',
        'status': 'str',
        'project_id': 'str',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float',
        'children_last_updated_at': 'datetime',
        'children_last_updated_by': 'str'
    }

    attribute_map = {
        'project': 'project',
        'model_jobs': 'modelJobs',
        'cohorts': 'cohorts',
        'user_favorites': 'userFavorites',
        'model_output_details': 'modelOutputDetails',
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'outcome_type': 'outcomeType',
        'feature_store': 'featureStore',
        'description': 'description',
        'status': 'status',
        'project_id': 'projectId',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version',
        'children_last_updated_at': 'childrenLastUpdatedAt',
        'children_last_updated_by': 'childrenLastUpdatedBy'
    }

    def __init__(self, project=None, model_jobs=None, cohorts=None, user_favorites=None, model_output_details=None, id=None, name=None, type=None, outcome_type=None, feature_store=None, description=None, status=None, project_id=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None, children_last_updated_at=None, children_last_updated_by=None):  # noqa: E501
        """ModelResponseDto - a model defined in Swagger"""  # noqa: E501
        self._project = None
        self._model_jobs = None
        self._cohorts = None
        self._user_favorites = None
        self._model_output_details = None
        self._id = None
        self._name = None
        self._type = None
        self._outcome_type = None
        self._feature_store = None
        self._description = None
        self._status = None
        self._project_id = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self._children_last_updated_at = None
        self._children_last_updated_by = None
        self.discriminator = None
        if project is not None:
            self.project = project
        if model_jobs is not None:
            self.model_jobs = model_jobs
        if cohorts is not None:
            self.cohorts = cohorts
        if user_favorites is not None:
            self.user_favorites = user_favorites
        if model_output_details is not None:
            self.model_output_details = model_output_details
        if id is not None:
            self.id = id
        self.name = name
        self.type = type
        if outcome_type is not None:
            self.outcome_type = outcome_type
        self.feature_store = feature_store
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
        self.project_id = project_id
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
        if children_last_updated_at is not None:
            self.children_last_updated_at = children_last_updated_at
        if children_last_updated_by is not None:
            self.children_last_updated_by = children_last_updated_by

    @property
    def project(self):
        """Gets the project of this ModelResponseDto.  # noqa: E501


        :return: The project of this ModelResponseDto.  # noqa: E501
        :rtype: ModelJoinedProjectResponseDto
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ModelResponseDto.


        :param project: The project of this ModelResponseDto.  # noqa: E501
        :type: ModelJoinedProjectResponseDto
        """

        self._project = project

    @property
    def model_jobs(self):
        """Gets the model_jobs of this ModelResponseDto.  # noqa: E501


        :return: The model_jobs of this ModelResponseDto.  # noqa: E501
        :rtype: ModelJoinedModelJobResponseDto
        """
        return self._model_jobs

    @model_jobs.setter
    def model_jobs(self, model_jobs):
        """Sets the model_jobs of this ModelResponseDto.


        :param model_jobs: The model_jobs of this ModelResponseDto.  # noqa: E501
        :type: ModelJoinedModelJobResponseDto
        """

        self._model_jobs = model_jobs

    @property
    def cohorts(self):
        """Gets the cohorts of this ModelResponseDto.  # noqa: E501


        :return: The cohorts of this ModelResponseDto.  # noqa: E501
        :rtype: ModelJoinedCohortResponseDto
        """
        return self._cohorts

    @cohorts.setter
    def cohorts(self, cohorts):
        """Sets the cohorts of this ModelResponseDto.


        :param cohorts: The cohorts of this ModelResponseDto.  # noqa: E501
        :type: ModelJoinedCohortResponseDto
        """

        self._cohorts = cohorts

    @property
    def user_favorites(self):
        """Gets the user_favorites of this ModelResponseDto.  # noqa: E501


        :return: The user_favorites of this ModelResponseDto.  # noqa: E501
        :rtype: ModelJoinedUserFavoriteResponseDto
        """
        return self._user_favorites

    @user_favorites.setter
    def user_favorites(self, user_favorites):
        """Sets the user_favorites of this ModelResponseDto.


        :param user_favorites: The user_favorites of this ModelResponseDto.  # noqa: E501
        :type: ModelJoinedUserFavoriteResponseDto
        """

        self._user_favorites = user_favorites

    @property
    def model_output_details(self):
        """Gets the model_output_details of this ModelResponseDto.  # noqa: E501


        :return: The model_output_details of this ModelResponseDto.  # noqa: E501
        :rtype: ModelJoinedModelOutputDetailsResponseDto
        """
        return self._model_output_details

    @model_output_details.setter
    def model_output_details(self, model_output_details):
        """Sets the model_output_details of this ModelResponseDto.


        :param model_output_details: The model_output_details of this ModelResponseDto.  # noqa: E501
        :type: ModelJoinedModelOutputDetailsResponseDto
        """

        self._model_output_details = model_output_details

    @property
    def id(self):
        """Gets the id of this ModelResponseDto.  # noqa: E501


        :return: The id of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelResponseDto.


        :param id: The id of this ModelResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ModelResponseDto.  # noqa: E501


        :return: The name of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ModelResponseDto.


        :param name: The name of this ModelResponseDto.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def type(self):
        """Gets the type of this ModelResponseDto.  # noqa: E501


        :return: The type of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ModelResponseDto.


        :param type: The type of this ModelResponseDto.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["risk", "impactability"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def outcome_type(self):
        """Gets the outcome_type of this ModelResponseDto.  # noqa: E501


        :return: The outcome_type of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._outcome_type

    @outcome_type.setter
    def outcome_type(self, outcome_type):
        """Sets the outcome_type of this ModelResponseDto.


        :param outcome_type: The outcome_type of this ModelResponseDto.  # noqa: E501
        :type: str
        """
        allowed_values = ["regression", "occurrence"]  # noqa: E501
        if outcome_type not in allowed_values:
            raise ValueError(
                "Invalid value for `outcome_type` ({0}), must be one of {1}"  # noqa: E501
                .format(outcome_type, allowed_values)
            )

        self._outcome_type = outcome_type

    @property
    def feature_store(self):
        """Gets the feature_store of this ModelResponseDto.  # noqa: E501


        :return: The feature_store of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._feature_store

    @feature_store.setter
    def feature_store(self, feature_store):
        """Sets the feature_store of this ModelResponseDto.


        :param feature_store: The feature_store of this ModelResponseDto.  # noqa: E501
        :type: str
        """
        if feature_store is None:
            raise ValueError("Invalid value for `feature_store`, must not be `None`")  # noqa: E501
        allowed_values = ["curia_data_lake", "byod"]  # noqa: E501
        if feature_store not in allowed_values:
            raise ValueError(
                "Invalid value for `feature_store` ({0}), must be one of {1}"  # noqa: E501
                .format(feature_store, allowed_values)
            )

        self._feature_store = feature_store

    @property
    def description(self):
        """Gets the description of this ModelResponseDto.  # noqa: E501


        :return: The description of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ModelResponseDto.


        :param description: The description of this ModelResponseDto.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def status(self):
        """Gets the status of this ModelResponseDto.  # noqa: E501


        :return: The status of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ModelResponseDto.


        :param status: The status of this ModelResponseDto.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def project_id(self):
        """Gets the project_id of this ModelResponseDto.  # noqa: E501


        :return: The project_id of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ModelResponseDto.


        :param project_id: The project_id of this ModelResponseDto.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ModelResponseDto.  # noqa: E501


        :return: The last_updated_by of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ModelResponseDto.


        :param last_updated_by: The last_updated_by of this ModelResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this ModelResponseDto.  # noqa: E501


        :return: The created_by of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ModelResponseDto.


        :param created_by: The created_by of this ModelResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this ModelResponseDto.  # noqa: E501


        :return: The created_at of this ModelResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelResponseDto.


        :param created_at: The created_at of this ModelResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelResponseDto.  # noqa: E501


        :return: The updated_at of this ModelResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelResponseDto.


        :param updated_at: The updated_at of this ModelResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this ModelResponseDto.  # noqa: E501


        :return: The archived_at of this ModelResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this ModelResponseDto.


        :param archived_at: The archived_at of this ModelResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this ModelResponseDto.  # noqa: E501


        :return: The version of this ModelResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelResponseDto.


        :param version: The version of this ModelResponseDto.  # noqa: E501
        :type: float
        """

        self._version = version

    @property
    def children_last_updated_at(self):
        """Gets the children_last_updated_at of this ModelResponseDto.  # noqa: E501


        :return: The children_last_updated_at of this ModelResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._children_last_updated_at

    @children_last_updated_at.setter
    def children_last_updated_at(self, children_last_updated_at):
        """Sets the children_last_updated_at of this ModelResponseDto.


        :param children_last_updated_at: The children_last_updated_at of this ModelResponseDto.  # noqa: E501
        :type: datetime
        """

        self._children_last_updated_at = children_last_updated_at

    @property
    def children_last_updated_by(self):
        """Gets the children_last_updated_by of this ModelResponseDto.  # noqa: E501


        :return: The children_last_updated_by of this ModelResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._children_last_updated_by

    @children_last_updated_by.setter
    def children_last_updated_by(self, children_last_updated_by):
        """Sets the children_last_updated_by of this ModelResponseDto.


        :param children_last_updated_by: The children_last_updated_by of this ModelResponseDto.  # noqa: E501
        :type: str
        """

        self._children_last_updated_by = children_last_updated_by

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
        if issubclass(ModelResponseDto, dict):
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
        if not isinstance(other, ModelResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
