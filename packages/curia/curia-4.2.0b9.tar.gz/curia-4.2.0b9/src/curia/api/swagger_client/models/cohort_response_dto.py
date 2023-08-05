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

class CohortResponseDto(object):
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
        'model_jobs': 'CohortJoinedModelJobResponseDto',
        'train_cohort': 'CohortJoinedCohortResponseDto',
        'prediction_cohorts': 'CohortJoinedCohortResponseDto',
        'id': 'str',
        'name': 'str',
        'model_id': 'str',
        'train_cohort_id': 'str',
        'cohort_windows': 'list[CohortWindow]',
        'organization_id': 'str',
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'revised_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'model_jobs': 'modelJobs',
        'train_cohort': 'trainCohort',
        'prediction_cohorts': 'predictionCohorts',
        'id': 'id',
        'name': 'name',
        'model_id': 'modelId',
        'train_cohort_id': 'trainCohortId',
        'cohort_windows': 'cohortWindows',
        'organization_id': 'organizationId',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'revised_at': 'revisedAt',
        'version': 'version'
    }

    def __init__(self, model_jobs=None, train_cohort=None, prediction_cohorts=None, id=None, name=None, model_id=None, train_cohort_id=None, cohort_windows=None, organization_id=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, revised_at=None, version=None):  # noqa: E501
        """CohortResponseDto - a model defined in Swagger"""  # noqa: E501
        self._model_jobs = None
        self._train_cohort = None
        self._prediction_cohorts = None
        self._id = None
        self._name = None
        self._model_id = None
        self._train_cohort_id = None
        self._cohort_windows = None
        self._organization_id = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._revised_at = None
        self._version = None
        self.discriminator = None
        if model_jobs is not None:
            self.model_jobs = model_jobs
        if train_cohort is not None:
            self.train_cohort = train_cohort
        if prediction_cohorts is not None:
            self.prediction_cohorts = prediction_cohorts
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if model_id is not None:
            self.model_id = model_id
        if train_cohort_id is not None:
            self.train_cohort_id = train_cohort_id
        self.cohort_windows = cohort_windows
        self.organization_id = organization_id
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
        if revised_at is not None:
            self.revised_at = revised_at
        if version is not None:
            self.version = version

    @property
    def model_jobs(self):
        """Gets the model_jobs of this CohortResponseDto.  # noqa: E501


        :return: The model_jobs of this CohortResponseDto.  # noqa: E501
        :rtype: CohortJoinedModelJobResponseDto
        """
        return self._model_jobs

    @model_jobs.setter
    def model_jobs(self, model_jobs):
        """Sets the model_jobs of this CohortResponseDto.


        :param model_jobs: The model_jobs of this CohortResponseDto.  # noqa: E501
        :type: CohortJoinedModelJobResponseDto
        """

        self._model_jobs = model_jobs

    @property
    def train_cohort(self):
        """Gets the train_cohort of this CohortResponseDto.  # noqa: E501


        :return: The train_cohort of this CohortResponseDto.  # noqa: E501
        :rtype: CohortJoinedCohortResponseDto
        """
        return self._train_cohort

    @train_cohort.setter
    def train_cohort(self, train_cohort):
        """Sets the train_cohort of this CohortResponseDto.


        :param train_cohort: The train_cohort of this CohortResponseDto.  # noqa: E501
        :type: CohortJoinedCohortResponseDto
        """

        self._train_cohort = train_cohort

    @property
    def prediction_cohorts(self):
        """Gets the prediction_cohorts of this CohortResponseDto.  # noqa: E501


        :return: The prediction_cohorts of this CohortResponseDto.  # noqa: E501
        :rtype: CohortJoinedCohortResponseDto
        """
        return self._prediction_cohorts

    @prediction_cohorts.setter
    def prediction_cohorts(self, prediction_cohorts):
        """Sets the prediction_cohorts of this CohortResponseDto.


        :param prediction_cohorts: The prediction_cohorts of this CohortResponseDto.  # noqa: E501
        :type: CohortJoinedCohortResponseDto
        """

        self._prediction_cohorts = prediction_cohorts

    @property
    def id(self):
        """Gets the id of this CohortResponseDto.  # noqa: E501


        :return: The id of this CohortResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CohortResponseDto.


        :param id: The id of this CohortResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this CohortResponseDto.  # noqa: E501


        :return: The name of this CohortResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CohortResponseDto.


        :param name: The name of this CohortResponseDto.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def model_id(self):
        """Gets the model_id of this CohortResponseDto.  # noqa: E501


        :return: The model_id of this CohortResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this CohortResponseDto.


        :param model_id: The model_id of this CohortResponseDto.  # noqa: E501
        :type: str
        """

        self._model_id = model_id

    @property
    def train_cohort_id(self):
        """Gets the train_cohort_id of this CohortResponseDto.  # noqa: E501


        :return: The train_cohort_id of this CohortResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._train_cohort_id

    @train_cohort_id.setter
    def train_cohort_id(self, train_cohort_id):
        """Sets the train_cohort_id of this CohortResponseDto.


        :param train_cohort_id: The train_cohort_id of this CohortResponseDto.  # noqa: E501
        :type: str
        """

        self._train_cohort_id = train_cohort_id

    @property
    def cohort_windows(self):
        """Gets the cohort_windows of this CohortResponseDto.  # noqa: E501


        :return: The cohort_windows of this CohortResponseDto.  # noqa: E501
        :rtype: list[CohortWindow]
        """
        return self._cohort_windows

    @cohort_windows.setter
    def cohort_windows(self, cohort_windows):
        """Sets the cohort_windows of this CohortResponseDto.


        :param cohort_windows: The cohort_windows of this CohortResponseDto.  # noqa: E501
        :type: list[CohortWindow]
        """
        if cohort_windows is None:
            raise ValueError("Invalid value for `cohort_windows`, must not be `None`")  # noqa: E501

        self._cohort_windows = cohort_windows

    @property
    def organization_id(self):
        """Gets the organization_id of this CohortResponseDto.  # noqa: E501


        :return: The organization_id of this CohortResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this CohortResponseDto.


        :param organization_id: The organization_id of this CohortResponseDto.  # noqa: E501
        :type: str
        """
        if organization_id is None:
            raise ValueError("Invalid value for `organization_id`, must not be `None`")  # noqa: E501

        self._organization_id = organization_id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this CohortResponseDto.  # noqa: E501


        :return: The last_updated_by of this CohortResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this CohortResponseDto.


        :param last_updated_by: The last_updated_by of this CohortResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this CohortResponseDto.  # noqa: E501


        :return: The created_by of this CohortResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this CohortResponseDto.


        :param created_by: The created_by of this CohortResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this CohortResponseDto.  # noqa: E501


        :return: The created_at of this CohortResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this CohortResponseDto.


        :param created_at: The created_at of this CohortResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this CohortResponseDto.  # noqa: E501


        :return: The updated_at of this CohortResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this CohortResponseDto.


        :param updated_at: The updated_at of this CohortResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this CohortResponseDto.  # noqa: E501


        :return: The archived_at of this CohortResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this CohortResponseDto.


        :param archived_at: The archived_at of this CohortResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def revised_at(self):
        """Gets the revised_at of this CohortResponseDto.  # noqa: E501


        :return: The revised_at of this CohortResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._revised_at

    @revised_at.setter
    def revised_at(self, revised_at):
        """Sets the revised_at of this CohortResponseDto.


        :param revised_at: The revised_at of this CohortResponseDto.  # noqa: E501
        :type: datetime
        """

        self._revised_at = revised_at

    @property
    def version(self):
        """Gets the version of this CohortResponseDto.  # noqa: E501


        :return: The version of this CohortResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this CohortResponseDto.


        :param version: The version of this CohortResponseDto.  # noqa: E501
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
        if issubclass(CohortResponseDto, dict):
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
        if not isinstance(other, CohortResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
