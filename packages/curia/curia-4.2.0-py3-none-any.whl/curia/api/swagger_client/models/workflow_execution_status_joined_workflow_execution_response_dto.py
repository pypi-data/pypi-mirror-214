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

class WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto(object):
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
        'last_updated_by': 'str',
        'created_by': 'str',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'version': 'float',
        'organization_id': 'str',
        'workflow_id': 'str',
        'run_id': 'float',
        'status': 'object',
        'queued_at': 'datetime',
        'started_at': 'datetime',
        'ended_at': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'version': 'version',
        'organization_id': 'organizationId',
        'workflow_id': 'workflowId',
        'run_id': 'runId',
        'status': 'status',
        'queued_at': 'queuedAt',
        'started_at': 'startedAt',
        'ended_at': 'endedAt'
    }

    def __init__(self, id=None, last_updated_by=None, created_by=None, created_at=None, updated_at=None, archived_at=None, version=None, organization_id=None, workflow_id=None, run_id=None, status=None, queued_at=None, started_at=None, ended_at=None):  # noqa: E501
        """WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._last_updated_by = None
        self._created_by = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._version = None
        self._organization_id = None
        self._workflow_id = None
        self._run_id = None
        self._status = None
        self._queued_at = None
        self._started_at = None
        self._ended_at = None
        self.discriminator = None
        if id is not None:
            self.id = id
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
        self.organization_id = organization_id
        self.workflow_id = workflow_id
        if run_id is not None:
            self.run_id = run_id
        if status is not None:
            self.status = status
        if queued_at is not None:
            self.queued_at = queued_at
        if started_at is not None:
            self.started_at = started_at
        if ended_at is not None:
            self.ended_at = ended_at

    @property
    def id(self):
        """Gets the id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param id: The id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The last_updated_by of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param last_updated_by: The last_updated_by of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The created_by of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param created_by: The created_by of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def created_at(self):
        """Gets the created_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The created_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param created_at: The created_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The updated_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param updated_at: The updated_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The archived_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param archived_at: The archived_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def version(self):
        """Gets the version of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The version of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param version: The version of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: float
        """

        self._version = version

    @property
    def organization_id(self):
        """Gets the organization_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The organization_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param organization_id: The organization_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: str
        """
        if organization_id is None:
            raise ValueError("Invalid value for `organization_id`, must not be `None`")  # noqa: E501

        self._organization_id = organization_id

    @property
    def workflow_id(self):
        """Gets the workflow_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The workflow_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._workflow_id

    @workflow_id.setter
    def workflow_id(self, workflow_id):
        """Sets the workflow_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param workflow_id: The workflow_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: str
        """
        if workflow_id is None:
            raise ValueError("Invalid value for `workflow_id`, must not be `None`")  # noqa: E501

        self._workflow_id = workflow_id

    @property
    def run_id(self):
        """Gets the run_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The run_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: float
        """
        return self._run_id

    @run_id.setter
    def run_id(self, run_id):
        """Sets the run_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param run_id: The run_id of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: float
        """

        self._run_id = run_id

    @property
    def status(self):
        """Gets the status of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The status of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: object
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param status: The status of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: object
        """

        self._status = status

    @property
    def queued_at(self):
        """Gets the queued_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The queued_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._queued_at

    @queued_at.setter
    def queued_at(self, queued_at):
        """Sets the queued_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param queued_at: The queued_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: datetime
        """

        self._queued_at = queued_at

    @property
    def started_at(self):
        """Gets the started_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The started_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param started_at: The started_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :type: datetime
        """

        self._started_at = started_at

    @property
    def ended_at(self):
        """Gets the ended_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501


        :return: The ended_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._ended_at

    @ended_at.setter
    def ended_at(self, ended_at):
        """Sets the ended_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.


        :param ended_at: The ended_at of this WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto.  # noqa: E501
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
        if issubclass(WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto, dict):
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
        if not isinstance(other, WorkflowExecutionStatusJoinedWorkflowExecutionResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
