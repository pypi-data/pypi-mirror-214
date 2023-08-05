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

class ModelJoinedModelJobResponseDto(object):
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
        'feature_sub_categories': 'ModelJoinedModelJobJoinedFeatureSubCategoryResponseDto',
        'dataset': 'ModelJoinedModelJobJoinedDatasetResponseDto',
        'cohort': 'ModelJoinedModelJobJoinedCohortResponseDto',
        'id': 'str',
        'type': 'str',
        'outcome_type': 'str',
        'config': 'ModelJobConfig',
        'execution_id': 'str',
        'status': 'str',
        'project_id': 'str',
        'model_id': 'str',
        'cohort_id': 'str',
        'dataset_id': 'str',
        'model_population_id': 'str',
        'outcome_distribution_histogram_query_id': 'str',
        'last_updated_by': 'str',
        'created_by': 'str',
        'started_at': 'datetime',
        'ended_at': 'datetime',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float'
    }

    attribute_map = {
        'feature_sub_categories': 'featureSubCategories',
        'dataset': 'dataset',
        'cohort': 'cohort',
        'id': 'id',
        'type': 'type',
        'outcome_type': 'outcomeType',
        'config': 'config',
        'execution_id': 'executionId',
        'status': 'status',
        'project_id': 'projectId',
        'model_id': 'modelId',
        'cohort_id': 'cohortId',
        'dataset_id': 'datasetId',
        'model_population_id': 'modelPopulationId',
        'outcome_distribution_histogram_query_id': 'outcomeDistributionHistogramQueryId',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'started_at': 'startedAt',
        'ended_at': 'endedAt',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version'
    }

    def __init__(self, feature_sub_categories=None, dataset=None, cohort=None, id=None, type=None, outcome_type=None, config=None, execution_id=None, status=None, project_id=None, model_id=None, cohort_id=None, dataset_id=None, model_population_id=None, outcome_distribution_histogram_query_id=None, last_updated_by=None, created_by=None, started_at=None, ended_at=None, created_at=None, updated_at=None, archived_at=None, version=None):  # noqa: E501
        """ModelJoinedModelJobResponseDto - a model defined in Swagger"""  # noqa: E501
        self._feature_sub_categories = None
        self._dataset = None
        self._cohort = None
        self._id = None
        self._type = None
        self._outcome_type = None
        self._config = None
        self._execution_id = None
        self._status = None
        self._project_id = None
        self._model_id = None
        self._cohort_id = None
        self._dataset_id = None
        self._model_population_id = None
        self._outcome_distribution_histogram_query_id = None
        self._last_updated_by = None
        self._created_by = None
        self._started_at = None
        self._ended_at = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self.discriminator = None
        if feature_sub_categories is not None:
            self.feature_sub_categories = feature_sub_categories
        if dataset is not None:
            self.dataset = dataset
        if cohort is not None:
            self.cohort = cohort
        if id is not None:
            self.id = id
        self.type = type
        if outcome_type is not None:
            self.outcome_type = outcome_type
        if config is not None:
            self.config = config
        if execution_id is not None:
            self.execution_id = execution_id
        if status is not None:
            self.status = status
        self.project_id = project_id
        self.model_id = model_id
        if cohort_id is not None:
            self.cohort_id = cohort_id
        if dataset_id is not None:
            self.dataset_id = dataset_id
        if model_population_id is not None:
            self.model_population_id = model_population_id
        if outcome_distribution_histogram_query_id is not None:
            self.outcome_distribution_histogram_query_id = outcome_distribution_histogram_query_id
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_by is not None:
            self.created_by = created_by
        if started_at is not None:
            self.started_at = started_at
        if ended_at is not None:
            self.ended_at = ended_at
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if archived_at is not None:
            self.archived_at = archived_at
        if version is not None:
            self.version = version

    @property
    def feature_sub_categories(self):
        """Gets the feature_sub_categories of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The feature_sub_categories of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: ModelJoinedModelJobJoinedFeatureSubCategoryResponseDto
        """
        return self._feature_sub_categories

    @feature_sub_categories.setter
    def feature_sub_categories(self, feature_sub_categories):
        """Sets the feature_sub_categories of this ModelJoinedModelJobResponseDto.


        :param feature_sub_categories: The feature_sub_categories of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: ModelJoinedModelJobJoinedFeatureSubCategoryResponseDto
        """

        self._feature_sub_categories = feature_sub_categories

    @property
    def dataset(self):
        """Gets the dataset of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The dataset of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: ModelJoinedModelJobJoinedDatasetResponseDto
        """
        return self._dataset

    @dataset.setter
    def dataset(self, dataset):
        """Sets the dataset of this ModelJoinedModelJobResponseDto.


        :param dataset: The dataset of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: ModelJoinedModelJobJoinedDatasetResponseDto
        """

        self._dataset = dataset

    @property
    def cohort(self):
        """Gets the cohort of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The cohort of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: ModelJoinedModelJobJoinedCohortResponseDto
        """
        return self._cohort

    @cohort.setter
    def cohort(self, cohort):
        """Sets the cohort of this ModelJoinedModelJobResponseDto.


        :param cohort: The cohort of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: ModelJoinedModelJobJoinedCohortResponseDto
        """

        self._cohort = cohort

    @property
    def id(self):
        """Gets the id of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelJoinedModelJobResponseDto.


        :param id: The id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def type(self):
        """Gets the type of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The type of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ModelJoinedModelJobResponseDto.


        :param type: The type of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["train", "predict"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def outcome_type(self):
        """Gets the outcome_type of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The outcome_type of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._outcome_type

    @outcome_type.setter
    def outcome_type(self, outcome_type):
        """Sets the outcome_type of this ModelJoinedModelJobResponseDto.


        :param outcome_type: The outcome_type of this ModelJoinedModelJobResponseDto.  # noqa: E501
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
    def config(self):
        """Gets the config of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The config of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: ModelJobConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this ModelJoinedModelJobResponseDto.


        :param config: The config of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: ModelJobConfig
        """

        self._config = config

    @property
    def execution_id(self):
        """Gets the execution_id of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The execution_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this ModelJoinedModelJobResponseDto.


        :param execution_id: The execution_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._execution_id = execution_id

    @property
    def status(self):
        """Gets the status of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The status of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ModelJoinedModelJobResponseDto.


        :param status: The status of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def project_id(self):
        """Gets the project_id of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The project_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ModelJoinedModelJobResponseDto.


        :param project_id: The project_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def model_id(self):
        """Gets the model_id of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The model_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this ModelJoinedModelJobResponseDto.


        :param model_id: The model_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """
        if model_id is None:
            raise ValueError("Invalid value for `model_id`, must not be `None`")  # noqa: E501

        self._model_id = model_id

    @property
    def cohort_id(self):
        """Gets the cohort_id of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The cohort_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._cohort_id

    @cohort_id.setter
    def cohort_id(self, cohort_id):
        """Sets the cohort_id of this ModelJoinedModelJobResponseDto.


        :param cohort_id: The cohort_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._cohort_id = cohort_id

    @property
    def dataset_id(self):
        """Gets the dataset_id of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The dataset_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        """Sets the dataset_id of this ModelJoinedModelJobResponseDto.


        :param dataset_id: The dataset_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._dataset_id = dataset_id

    @property
    def model_population_id(self):
        """Gets the model_population_id of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The model_population_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._model_population_id

    @model_population_id.setter
    def model_population_id(self, model_population_id):
        """Sets the model_population_id of this ModelJoinedModelJobResponseDto.


        :param model_population_id: The model_population_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._model_population_id = model_population_id

    @property
    def outcome_distribution_histogram_query_id(self):
        """Gets the outcome_distribution_histogram_query_id of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The outcome_distribution_histogram_query_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._outcome_distribution_histogram_query_id

    @outcome_distribution_histogram_query_id.setter
    def outcome_distribution_histogram_query_id(self, outcome_distribution_histogram_query_id):
        """Sets the outcome_distribution_histogram_query_id of this ModelJoinedModelJobResponseDto.


        :param outcome_distribution_histogram_query_id: The outcome_distribution_histogram_query_id of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._outcome_distribution_histogram_query_id = outcome_distribution_histogram_query_id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The last_updated_by of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ModelJoinedModelJobResponseDto.


        :param last_updated_by: The last_updated_by of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The created_by of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ModelJoinedModelJobResponseDto.


        :param created_by: The created_by of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def started_at(self):
        """Gets the started_at of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The started_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this ModelJoinedModelJobResponseDto.


        :param started_at: The started_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: datetime
        """

        self._started_at = started_at

    @property
    def ended_at(self):
        """Gets the ended_at of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The ended_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._ended_at

    @ended_at.setter
    def ended_at(self, ended_at):
        """Sets the ended_at of this ModelJoinedModelJobResponseDto.


        :param ended_at: The ended_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: datetime
        """

        self._ended_at = ended_at

    @property
    def created_at(self):
        """Gets the created_at of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The created_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelJoinedModelJobResponseDto.


        :param created_at: The created_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The updated_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelJoinedModelJobResponseDto.


        :param updated_at: The updated_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The archived_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this ModelJoinedModelJobResponseDto.


        :param archived_at: The archived_at of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this ModelJoinedModelJobResponseDto.  # noqa: E501


        :return: The version of this ModelJoinedModelJobResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelJoinedModelJobResponseDto.


        :param version: The version of this ModelJoinedModelJobResponseDto.  # noqa: E501
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
        if issubclass(ModelJoinedModelJobResponseDto, dict):
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
        if not isinstance(other, ModelJoinedModelJobResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
