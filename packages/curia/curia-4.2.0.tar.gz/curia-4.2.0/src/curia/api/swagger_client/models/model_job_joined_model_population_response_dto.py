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

class ModelJobJoinedModelPopulationResponseDto(object):
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
        'cohorts': 'ModelJobJoinedModelPopulationJoinedCohortDefinitionResponseDto',
        'outcome': 'ModelJobJoinedModelPopulationJoinedOutcomeDefinitionResponseDto',
        'intervention': 'ModelJobJoinedModelPopulationJoinedInterventionDefinitionResponseDto',
        'data_query': 'ModelJobJoinedModelPopulationJoinedDataQueryResponseDto',
        'id': 'str',
        'name': 'str',
        'query_count_status': 'str',
        'query_count_error': 'str',
        'query_list_status': 'str',
        'query_list_error': 'str',
        'query_all_status': 'str',
        'query_all_error': 'str',
        'query_count_started_at': 'datetime',
        'query_count_ended_at': 'datetime',
        'query_list_started_at': 'datetime',
        'query_list_ended_at': 'datetime',
        'query_all_started_at': 'datetime',
        'query_all_ended_at': 'datetime',
        'organization_id': 'str',
        'population_id': 'str',
        'data_query_id': 'str',
        'outcome_distribution_histogram_query_id': 'str',
        'created_at': 'datetime',
        'created_by': 'str',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'last_updated_by': 'str',
        'version': 'float'
    }

    attribute_map = {
        'cohorts': 'cohorts',
        'outcome': 'outcome',
        'intervention': 'intervention',
        'data_query': 'dataQuery',
        'id': 'id',
        'name': 'name',
        'query_count_status': 'queryCountStatus',
        'query_count_error': 'queryCountError',
        'query_list_status': 'queryListStatus',
        'query_list_error': 'queryListError',
        'query_all_status': 'queryAllStatus',
        'query_all_error': 'queryAllError',
        'query_count_started_at': 'queryCountStartedAt',
        'query_count_ended_at': 'queryCountEndedAt',
        'query_list_started_at': 'queryListStartedAt',
        'query_list_ended_at': 'queryListEndedAt',
        'query_all_started_at': 'queryAllStartedAt',
        'query_all_ended_at': 'queryAllEndedAt',
        'organization_id': 'organizationId',
        'population_id': 'populationId',
        'data_query_id': 'dataQueryId',
        'outcome_distribution_histogram_query_id': 'outcomeDistributionHistogramQueryId',
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'last_updated_by': 'lastUpdatedBy',
        'version': 'version'
    }

    def __init__(self, cohorts=None, outcome=None, intervention=None, data_query=None, id=None, name=None, query_count_status=None, query_count_error=None, query_list_status=None, query_list_error=None, query_all_status=None, query_all_error=None, query_count_started_at=None, query_count_ended_at=None, query_list_started_at=None, query_list_ended_at=None, query_all_started_at=None, query_all_ended_at=None, organization_id=None, population_id=None, data_query_id=None, outcome_distribution_histogram_query_id=None, created_at=None, created_by=None, updated_at=None, archived_at=None, last_updated_by=None, version=None):  # noqa: E501
        """ModelJobJoinedModelPopulationResponseDto - a model defined in Swagger"""  # noqa: E501
        self._cohorts = None
        self._outcome = None
        self._intervention = None
        self._data_query = None
        self._id = None
        self._name = None
        self._query_count_status = None
        self._query_count_error = None
        self._query_list_status = None
        self._query_list_error = None
        self._query_all_status = None
        self._query_all_error = None
        self._query_count_started_at = None
        self._query_count_ended_at = None
        self._query_list_started_at = None
        self._query_list_ended_at = None
        self._query_all_started_at = None
        self._query_all_ended_at = None
        self._organization_id = None
        self._population_id = None
        self._data_query_id = None
        self._outcome_distribution_histogram_query_id = None
        self._created_at = None
        self._created_by = None
        self._updated_at = None
        self._archived_at = None
        self._last_updated_by = None
        self._version = None
        self.discriminator = None
        if cohorts is not None:
            self.cohorts = cohorts
        if outcome is not None:
            self.outcome = outcome
        if intervention is not None:
            self.intervention = intervention
        if data_query is not None:
            self.data_query = data_query
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if query_count_status is not None:
            self.query_count_status = query_count_status
        if query_count_error is not None:
            self.query_count_error = query_count_error
        if query_list_status is not None:
            self.query_list_status = query_list_status
        if query_list_error is not None:
            self.query_list_error = query_list_error
        if query_all_status is not None:
            self.query_all_status = query_all_status
        if query_all_error is not None:
            self.query_all_error = query_all_error
        if query_count_started_at is not None:
            self.query_count_started_at = query_count_started_at
        if query_count_ended_at is not None:
            self.query_count_ended_at = query_count_ended_at
        if query_list_started_at is not None:
            self.query_list_started_at = query_list_started_at
        if query_list_ended_at is not None:
            self.query_list_ended_at = query_list_ended_at
        if query_all_started_at is not None:
            self.query_all_started_at = query_all_started_at
        if query_all_ended_at is not None:
            self.query_all_ended_at = query_all_ended_at
        if organization_id is not None:
            self.organization_id = organization_id
        if population_id is not None:
            self.population_id = population_id
        if data_query_id is not None:
            self.data_query_id = data_query_id
        if outcome_distribution_histogram_query_id is not None:
            self.outcome_distribution_histogram_query_id = outcome_distribution_histogram_query_id
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if updated_at is not None:
            self.updated_at = updated_at
        if archived_at is not None:
            self.archived_at = archived_at
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if version is not None:
            self.version = version

    @property
    def cohorts(self):
        """Gets the cohorts of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The cohorts of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: ModelJobJoinedModelPopulationJoinedCohortDefinitionResponseDto
        """
        return self._cohorts

    @cohorts.setter
    def cohorts(self, cohorts):
        """Sets the cohorts of this ModelJobJoinedModelPopulationResponseDto.


        :param cohorts: The cohorts of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: ModelJobJoinedModelPopulationJoinedCohortDefinitionResponseDto
        """

        self._cohorts = cohorts

    @property
    def outcome(self):
        """Gets the outcome of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The outcome of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: ModelJobJoinedModelPopulationJoinedOutcomeDefinitionResponseDto
        """
        return self._outcome

    @outcome.setter
    def outcome(self, outcome):
        """Sets the outcome of this ModelJobJoinedModelPopulationResponseDto.


        :param outcome: The outcome of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: ModelJobJoinedModelPopulationJoinedOutcomeDefinitionResponseDto
        """

        self._outcome = outcome

    @property
    def intervention(self):
        """Gets the intervention of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The intervention of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: ModelJobJoinedModelPopulationJoinedInterventionDefinitionResponseDto
        """
        return self._intervention

    @intervention.setter
    def intervention(self, intervention):
        """Sets the intervention of this ModelJobJoinedModelPopulationResponseDto.


        :param intervention: The intervention of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: ModelJobJoinedModelPopulationJoinedInterventionDefinitionResponseDto
        """

        self._intervention = intervention

    @property
    def data_query(self):
        """Gets the data_query of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The data_query of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: ModelJobJoinedModelPopulationJoinedDataQueryResponseDto
        """
        return self._data_query

    @data_query.setter
    def data_query(self, data_query):
        """Sets the data_query of this ModelJobJoinedModelPopulationResponseDto.


        :param data_query: The data_query of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: ModelJobJoinedModelPopulationJoinedDataQueryResponseDto
        """

        self._data_query = data_query

    @property
    def id(self):
        """Gets the id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelJobJoinedModelPopulationResponseDto.


        :param id: The id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The name of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ModelJobJoinedModelPopulationResponseDto.


        :param name: The name of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def query_count_status(self):
        """Gets the query_count_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_count_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._query_count_status

    @query_count_status.setter
    def query_count_status(self, query_count_status):
        """Sets the query_count_status of this ModelJobJoinedModelPopulationResponseDto.


        :param query_count_status: The query_count_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._query_count_status = query_count_status

    @property
    def query_count_error(self):
        """Gets the query_count_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_count_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._query_count_error

    @query_count_error.setter
    def query_count_error(self, query_count_error):
        """Sets the query_count_error of this ModelJobJoinedModelPopulationResponseDto.


        :param query_count_error: The query_count_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._query_count_error = query_count_error

    @property
    def query_list_status(self):
        """Gets the query_list_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_list_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._query_list_status

    @query_list_status.setter
    def query_list_status(self, query_list_status):
        """Sets the query_list_status of this ModelJobJoinedModelPopulationResponseDto.


        :param query_list_status: The query_list_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._query_list_status = query_list_status

    @property
    def query_list_error(self):
        """Gets the query_list_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_list_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._query_list_error

    @query_list_error.setter
    def query_list_error(self, query_list_error):
        """Sets the query_list_error of this ModelJobJoinedModelPopulationResponseDto.


        :param query_list_error: The query_list_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._query_list_error = query_list_error

    @property
    def query_all_status(self):
        """Gets the query_all_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_all_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._query_all_status

    @query_all_status.setter
    def query_all_status(self, query_all_status):
        """Sets the query_all_status of this ModelJobJoinedModelPopulationResponseDto.


        :param query_all_status: The query_all_status of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._query_all_status = query_all_status

    @property
    def query_all_error(self):
        """Gets the query_all_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_all_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._query_all_error

    @query_all_error.setter
    def query_all_error(self, query_all_error):
        """Sets the query_all_error of this ModelJobJoinedModelPopulationResponseDto.


        :param query_all_error: The query_all_error of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._query_all_error = query_all_error

    @property
    def query_count_started_at(self):
        """Gets the query_count_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_count_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._query_count_started_at

    @query_count_started_at.setter
    def query_count_started_at(self, query_count_started_at):
        """Sets the query_count_started_at of this ModelJobJoinedModelPopulationResponseDto.


        :param query_count_started_at: The query_count_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._query_count_started_at = query_count_started_at

    @property
    def query_count_ended_at(self):
        """Gets the query_count_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_count_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._query_count_ended_at

    @query_count_ended_at.setter
    def query_count_ended_at(self, query_count_ended_at):
        """Sets the query_count_ended_at of this ModelJobJoinedModelPopulationResponseDto.


        :param query_count_ended_at: The query_count_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._query_count_ended_at = query_count_ended_at

    @property
    def query_list_started_at(self):
        """Gets the query_list_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_list_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._query_list_started_at

    @query_list_started_at.setter
    def query_list_started_at(self, query_list_started_at):
        """Sets the query_list_started_at of this ModelJobJoinedModelPopulationResponseDto.


        :param query_list_started_at: The query_list_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._query_list_started_at = query_list_started_at

    @property
    def query_list_ended_at(self):
        """Gets the query_list_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_list_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._query_list_ended_at

    @query_list_ended_at.setter
    def query_list_ended_at(self, query_list_ended_at):
        """Sets the query_list_ended_at of this ModelJobJoinedModelPopulationResponseDto.


        :param query_list_ended_at: The query_list_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._query_list_ended_at = query_list_ended_at

    @property
    def query_all_started_at(self):
        """Gets the query_all_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_all_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._query_all_started_at

    @query_all_started_at.setter
    def query_all_started_at(self, query_all_started_at):
        """Sets the query_all_started_at of this ModelJobJoinedModelPopulationResponseDto.


        :param query_all_started_at: The query_all_started_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._query_all_started_at = query_all_started_at

    @property
    def query_all_ended_at(self):
        """Gets the query_all_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The query_all_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._query_all_ended_at

    @query_all_ended_at.setter
    def query_all_ended_at(self, query_all_ended_at):
        """Sets the query_all_ended_at of this ModelJobJoinedModelPopulationResponseDto.


        :param query_all_ended_at: The query_all_ended_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._query_all_ended_at = query_all_ended_at

    @property
    def organization_id(self):
        """Gets the organization_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The organization_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this ModelJobJoinedModelPopulationResponseDto.


        :param organization_id: The organization_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._organization_id = organization_id

    @property
    def population_id(self):
        """Gets the population_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The population_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._population_id

    @population_id.setter
    def population_id(self, population_id):
        """Sets the population_id of this ModelJobJoinedModelPopulationResponseDto.


        :param population_id: The population_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._population_id = population_id

    @property
    def data_query_id(self):
        """Gets the data_query_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The data_query_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._data_query_id

    @data_query_id.setter
    def data_query_id(self, data_query_id):
        """Sets the data_query_id of this ModelJobJoinedModelPopulationResponseDto.


        :param data_query_id: The data_query_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._data_query_id = data_query_id

    @property
    def outcome_distribution_histogram_query_id(self):
        """Gets the outcome_distribution_histogram_query_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The outcome_distribution_histogram_query_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._outcome_distribution_histogram_query_id

    @outcome_distribution_histogram_query_id.setter
    def outcome_distribution_histogram_query_id(self, outcome_distribution_histogram_query_id):
        """Sets the outcome_distribution_histogram_query_id of this ModelJobJoinedModelPopulationResponseDto.


        :param outcome_distribution_histogram_query_id: The outcome_distribution_histogram_query_id of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._outcome_distribution_histogram_query_id = outcome_distribution_histogram_query_id

    @property
    def created_at(self):
        """Gets the created_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The created_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelJobJoinedModelPopulationResponseDto.


        :param created_at: The created_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The created_by of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ModelJobJoinedModelPopulationResponseDto.


        :param created_by: The created_by of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The updated_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelJobJoinedModelPopulationResponseDto.


        :param updated_at: The updated_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The archived_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this ModelJobJoinedModelPopulationResponseDto.


        :param archived_at: The archived_at of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The last_updated_by of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ModelJobJoinedModelPopulationResponseDto.


        :param last_updated_by: The last_updated_by of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def version(self):
        """Gets the version of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501


        :return: The version of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelJobJoinedModelPopulationResponseDto.


        :param version: The version of this ModelJobJoinedModelPopulationResponseDto.  # noqa: E501
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
        if issubclass(ModelJobJoinedModelPopulationResponseDto, dict):
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
        if not isinstance(other, ModelJobJoinedModelPopulationResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
