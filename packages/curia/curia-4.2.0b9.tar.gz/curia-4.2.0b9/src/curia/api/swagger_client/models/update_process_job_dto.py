# coding: utf-8

"""
    Curia Platform API

    These are the docs for the curia platform API. To test, generate an authorization token first.  # noqa: E501

    OpenAPI spec version: 3.2.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class UpdateProcessJobDto(object):
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
        'process_id': 'str',
        'project_id': 'str',
        'execution_id': 'str',
        'status': 'str',
        'config': 'object',
        'analysis_job_id': 'str',
        'started_at': 'datetime',
        'ended_at': 'datetime'
    }

    attribute_map = {
        'process_id': 'processId',
        'project_id': 'projectId',
        'execution_id': 'executionId',
        'status': 'status',
        'config': 'config',
        'analysis_job_id': 'analysisJobId',
        'started_at': 'startedAt',
        'ended_at': 'endedAt'
    }

    def __init__(self, process_id=None, project_id=None, execution_id=None, status=None, config=None, analysis_job_id=None, started_at=None, ended_at=None):  # noqa: E501
        """UpdateProcessJobDto - a model defined in Swagger"""  # noqa: E501
        self._process_id = None
        self._project_id = None
        self._execution_id = None
        self._status = None
        self._config = None
        self._analysis_job_id = None
        self._started_at = None
        self._ended_at = None
        self.discriminator = None
        if process_id is not None:
            self.process_id = process_id
        if project_id is not None:
            self.project_id = project_id
        if execution_id is not None:
            self.execution_id = execution_id
        if status is not None:
            self.status = status
        if config is not None:
            self.config = config
        if analysis_job_id is not None:
            self.analysis_job_id = analysis_job_id
        if started_at is not None:
            self.started_at = started_at
        if ended_at is not None:
            self.ended_at = ended_at

    @property
    def process_id(self):
        """Gets the process_id of this UpdateProcessJobDto.  # noqa: E501


        :return: The process_id of this UpdateProcessJobDto.  # noqa: E501
        :rtype: str
        """
        return self._process_id

    @process_id.setter
    def process_id(self, process_id):
        """Sets the process_id of this UpdateProcessJobDto.


        :param process_id: The process_id of this UpdateProcessJobDto.  # noqa: E501
        :type: str
        """

        self._process_id = process_id

    @property
    def project_id(self):
        """Gets the project_id of this UpdateProcessJobDto.  # noqa: E501


        :return: The project_id of this UpdateProcessJobDto.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this UpdateProcessJobDto.


        :param project_id: The project_id of this UpdateProcessJobDto.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def execution_id(self):
        """Gets the execution_id of this UpdateProcessJobDto.  # noqa: E501


        :return: The execution_id of this UpdateProcessJobDto.  # noqa: E501
        :rtype: str
        """
        return self._execution_id

    @execution_id.setter
    def execution_id(self, execution_id):
        """Sets the execution_id of this UpdateProcessJobDto.


        :param execution_id: The execution_id of this UpdateProcessJobDto.  # noqa: E501
        :type: str
        """

        self._execution_id = execution_id

    @property
    def status(self):
        """Gets the status of this UpdateProcessJobDto.  # noqa: E501


        :return: The status of this UpdateProcessJobDto.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this UpdateProcessJobDto.


        :param status: The status of this UpdateProcessJobDto.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def config(self):
        """Gets the config of this UpdateProcessJobDto.  # noqa: E501


        :return: The config of this UpdateProcessJobDto.  # noqa: E501
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this UpdateProcessJobDto.


        :param config: The config of this UpdateProcessJobDto.  # noqa: E501
        :type: object
        """

        self._config = config

    @property
    def analysis_job_id(self):
        """Gets the analysis_job_id of this UpdateProcessJobDto.  # noqa: E501


        :return: The analysis_job_id of this UpdateProcessJobDto.  # noqa: E501
        :rtype: str
        """
        return self._analysis_job_id

    @analysis_job_id.setter
    def analysis_job_id(self, analysis_job_id):
        """Sets the analysis_job_id of this UpdateProcessJobDto.


        :param analysis_job_id: The analysis_job_id of this UpdateProcessJobDto.  # noqa: E501
        :type: str
        """

        self._analysis_job_id = analysis_job_id

    @property
    def started_at(self):
        """Gets the started_at of this UpdateProcessJobDto.  # noqa: E501


        :return: The started_at of this UpdateProcessJobDto.  # noqa: E501
        :rtype: datetime
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this UpdateProcessJobDto.


        :param started_at: The started_at of this UpdateProcessJobDto.  # noqa: E501
        :type: datetime
        """

        self._started_at = started_at

    @property
    def ended_at(self):
        """Gets the ended_at of this UpdateProcessJobDto.  # noqa: E501


        :return: The ended_at of this UpdateProcessJobDto.  # noqa: E501
        :rtype: datetime
        """
        return self._ended_at

    @ended_at.setter
    def ended_at(self, ended_at):
        """Sets the ended_at of this UpdateProcessJobDto.


        :param ended_at: The ended_at of this UpdateProcessJobDto.  # noqa: E501
        :type: datetime
        """

        self._ended_at = ended_at

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
        if issubclass(UpdateProcessJobDto, dict):
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
        if not isinstance(other, UpdateProcessJobDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
