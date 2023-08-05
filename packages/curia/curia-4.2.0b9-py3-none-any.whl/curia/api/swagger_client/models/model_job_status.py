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

class ModelJobStatus(object):
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
        'model_job': 'ModelJob',
        'model_job_id': 'str',
        'project': 'Project',
        'project_id': 'str',
        'source': 'str',
        'step': 'str',
        'message': 'str',
        'type': 'str',
        'order': 'float',
        'created_at': 'datetime',
        'updated_at': 'datetime',
        'archived_at': 'datetime',
        'last_updated_by': 'str',
        'created_by': 'str',
        'progress': 'float',
        'metadata': 'object',
        'version': 'float'
    }

    attribute_map = {
        'id': 'id',
        'model_job': 'modelJob',
        'model_job_id': 'modelJobId',
        'project': 'project',
        'project_id': 'projectId',
        'source': 'source',
        'step': 'step',
        'message': 'message',
        'type': 'type',
        'order': 'order',
        'created_at': 'createdAt',
        'updated_at': 'updatedAt',
        'archived_at': 'archivedAt',
        'last_updated_by': 'lastUpdatedBy',
        'created_by': 'createdBy',
        'progress': 'progress',
        'metadata': 'metadata',
        'version': 'version'
    }

    def __init__(self, id=None, model_job=None, model_job_id=None, project=None, project_id=None, source=None, step=None, message=None, type=None, order=None, created_at=None, updated_at=None, archived_at=None, last_updated_by=None, created_by=None, progress=None, metadata=None, version=None):  # noqa: E501
        """ModelJobStatus - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._model_job = None
        self._model_job_id = None
        self._project = None
        self._project_id = None
        self._source = None
        self._step = None
        self._message = None
        self._type = None
        self._order = None
        self._created_at = None
        self._updated_at = None
        self._archived_at = None
        self._last_updated_by = None
        self._created_by = None
        self._progress = None
        self._metadata = None
        self._version = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if model_job is not None:
            self.model_job = model_job
        self.model_job_id = model_job_id
        if project is not None:
            self.project = project
        self.project_id = project_id
        if source is not None:
            self.source = source
        self.step = step
        if message is not None:
            self.message = message
        if type is not None:
            self.type = type
        if order is not None:
            self.order = order
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        if archived_at is not None:
            self.archived_at = archived_at
        if last_updated_by is not None:
            self.last_updated_by = last_updated_by
        if created_by is not None:
            self.created_by = created_by
        if progress is not None:
            self.progress = progress
        if metadata is not None:
            self.metadata = metadata
        if version is not None:
            self.version = version

    @property
    def id(self):
        """Gets the id of this ModelJobStatus.  # noqa: E501


        :return: The id of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ModelJobStatus.


        :param id: The id of this ModelJobStatus.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def model_job(self):
        """Gets the model_job of this ModelJobStatus.  # noqa: E501


        :return: The model_job of this ModelJobStatus.  # noqa: E501
        :rtype: ModelJob
        """
        return self._model_job

    @model_job.setter
    def model_job(self, model_job):
        """Sets the model_job of this ModelJobStatus.


        :param model_job: The model_job of this ModelJobStatus.  # noqa: E501
        :type: ModelJob
        """

        self._model_job = model_job

    @property
    def model_job_id(self):
        """Gets the model_job_id of this ModelJobStatus.  # noqa: E501


        :return: The model_job_id of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._model_job_id

    @model_job_id.setter
    def model_job_id(self, model_job_id):
        """Sets the model_job_id of this ModelJobStatus.


        :param model_job_id: The model_job_id of this ModelJobStatus.  # noqa: E501
        :type: str
        """
        if model_job_id is None:
            raise ValueError("Invalid value for `model_job_id`, must not be `None`")  # noqa: E501

        self._model_job_id = model_job_id

    @property
    def project(self):
        """Gets the project of this ModelJobStatus.  # noqa: E501


        :return: The project of this ModelJobStatus.  # noqa: E501
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ModelJobStatus.


        :param project: The project of this ModelJobStatus.  # noqa: E501
        :type: Project
        """

        self._project = project

    @property
    def project_id(self):
        """Gets the project_id of this ModelJobStatus.  # noqa: E501


        :return: The project_id of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ModelJobStatus.


        :param project_id: The project_id of this ModelJobStatus.  # noqa: E501
        :type: str
        """
        if project_id is None:
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def source(self):
        """Gets the source of this ModelJobStatus.  # noqa: E501


        :return: The source of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this ModelJobStatus.


        :param source: The source of this ModelJobStatus.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def step(self):
        """Gets the step of this ModelJobStatus.  # noqa: E501


        :return: The step of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._step

    @step.setter
    def step(self, step):
        """Sets the step of this ModelJobStatus.


        :param step: The step of this ModelJobStatus.  # noqa: E501
        :type: str
        """
        if step is None:
            raise ValueError("Invalid value for `step`, must not be `None`")  # noqa: E501

        self._step = step

    @property
    def message(self):
        """Gets the message of this ModelJobStatus.  # noqa: E501


        :return: The message of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this ModelJobStatus.


        :param message: The message of this ModelJobStatus.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def type(self):
        """Gets the type of this ModelJobStatus.  # noqa: E501


        :return: The type of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ModelJobStatus.


        :param type: The type of this ModelJobStatus.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def order(self):
        """Gets the order of this ModelJobStatus.  # noqa: E501


        :return: The order of this ModelJobStatus.  # noqa: E501
        :rtype: float
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this ModelJobStatus.


        :param order: The order of this ModelJobStatus.  # noqa: E501
        :type: float
        """

        self._order = order

    @property
    def created_at(self):
        """Gets the created_at of this ModelJobStatus.  # noqa: E501


        :return: The created_at of this ModelJobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this ModelJobStatus.


        :param created_at: The created_at of this ModelJobStatus.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this ModelJobStatus.  # noqa: E501


        :return: The updated_at of this ModelJobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this ModelJobStatus.


        :param updated_at: The updated_at of this ModelJobStatus.  # noqa: E501
        :type: datetime
        """

        self._updated_at = updated_at

    @property
    def archived_at(self):
        """Gets the archived_at of this ModelJobStatus.  # noqa: E501


        :return: The archived_at of this ModelJobStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this ModelJobStatus.


        :param archived_at: The archived_at of this ModelJobStatus.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def last_updated_by(self):
        """Gets the last_updated_by of this ModelJobStatus.  # noqa: E501


        :return: The last_updated_by of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._last_updated_by

    @last_updated_by.setter
    def last_updated_by(self, last_updated_by):
        """Sets the last_updated_by of this ModelJobStatus.


        :param last_updated_by: The last_updated_by of this ModelJobStatus.  # noqa: E501
        :type: str
        """

        self._last_updated_by = last_updated_by

    @property
    def created_by(self):
        """Gets the created_by of this ModelJobStatus.  # noqa: E501


        :return: The created_by of this ModelJobStatus.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this ModelJobStatus.


        :param created_by: The created_by of this ModelJobStatus.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def progress(self):
        """Gets the progress of this ModelJobStatus.  # noqa: E501


        :return: The progress of this ModelJobStatus.  # noqa: E501
        :rtype: float
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this ModelJobStatus.


        :param progress: The progress of this ModelJobStatus.  # noqa: E501
        :type: float
        """

        self._progress = progress

    @property
    def metadata(self):
        """Gets the metadata of this ModelJobStatus.  # noqa: E501


        :return: The metadata of this ModelJobStatus.  # noqa: E501
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this ModelJobStatus.


        :param metadata: The metadata of this ModelJobStatus.  # noqa: E501
        :type: object
        """

        self._metadata = metadata

    @property
    def version(self):
        """Gets the version of this ModelJobStatus.  # noqa: E501


        :return: The version of this ModelJobStatus.  # noqa: E501
        :rtype: float
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ModelJobStatus.


        :param version: The version of this ModelJobStatus.  # noqa: E501
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
        if issubclass(ModelJobStatus, dict):
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
        if not isinstance(other, ModelJobStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
