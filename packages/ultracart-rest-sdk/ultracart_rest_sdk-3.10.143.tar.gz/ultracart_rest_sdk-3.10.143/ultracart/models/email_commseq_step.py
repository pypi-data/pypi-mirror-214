# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class EmailCommseqStep(object):
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
        'alt_child_email_communication_sequence_steps': 'list[EmailCommseqStep]',
        'child_email_communication_sequence_steps': 'list[EmailCommseqStep]',
        'email_communication_sequence_step_uuid': 'str',
        'email_pending_review': 'bool',
        'email_rejected': 'bool',
        'email_requires_review': 'bool',
        'filter_profile_equation_json': 'str',
        'merchant_notes': 'str',
        'step_config_json': 'str',
        'type': 'str'
    }

    attribute_map = {
        'alt_child_email_communication_sequence_steps': 'alt_child_email_communication_sequence_steps',
        'child_email_communication_sequence_steps': 'child_email_communication_sequence_steps',
        'email_communication_sequence_step_uuid': 'email_communication_sequence_step_uuid',
        'email_pending_review': 'email_pending_review',
        'email_rejected': 'email_rejected',
        'email_requires_review': 'email_requires_review',
        'filter_profile_equation_json': 'filter_profile_equation_json',
        'merchant_notes': 'merchant_notes',
        'step_config_json': 'step_config_json',
        'type': 'type'
    }

    def __init__(self, alt_child_email_communication_sequence_steps=None, child_email_communication_sequence_steps=None, email_communication_sequence_step_uuid=None, email_pending_review=None, email_rejected=None, email_requires_review=None, filter_profile_equation_json=None, merchant_notes=None, step_config_json=None, type=None):  # noqa: E501
        """EmailCommseqStep - a model defined in Swagger"""  # noqa: E501

        self._alt_child_email_communication_sequence_steps = None
        self._child_email_communication_sequence_steps = None
        self._email_communication_sequence_step_uuid = None
        self._email_pending_review = None
        self._email_rejected = None
        self._email_requires_review = None
        self._filter_profile_equation_json = None
        self._merchant_notes = None
        self._step_config_json = None
        self._type = None
        self.discriminator = None

        if alt_child_email_communication_sequence_steps is not None:
            self.alt_child_email_communication_sequence_steps = alt_child_email_communication_sequence_steps
        if child_email_communication_sequence_steps is not None:
            self.child_email_communication_sequence_steps = child_email_communication_sequence_steps
        if email_communication_sequence_step_uuid is not None:
            self.email_communication_sequence_step_uuid = email_communication_sequence_step_uuid
        if email_pending_review is not None:
            self.email_pending_review = email_pending_review
        if email_rejected is not None:
            self.email_rejected = email_rejected
        if email_requires_review is not None:
            self.email_requires_review = email_requires_review
        if filter_profile_equation_json is not None:
            self.filter_profile_equation_json = filter_profile_equation_json
        if merchant_notes is not None:
            self.merchant_notes = merchant_notes
        if step_config_json is not None:
            self.step_config_json = step_config_json
        if type is not None:
            self.type = type

    @property
    def alt_child_email_communication_sequence_steps(self):
        """Gets the alt_child_email_communication_sequence_steps of this EmailCommseqStep.  # noqa: E501

        Array of child steps for the alternate path  # noqa: E501

        :return: The alt_child_email_communication_sequence_steps of this EmailCommseqStep.  # noqa: E501
        :rtype: list[EmailCommseqStep]
        """
        return self._alt_child_email_communication_sequence_steps

    @alt_child_email_communication_sequence_steps.setter
    def alt_child_email_communication_sequence_steps(self, alt_child_email_communication_sequence_steps):
        """Sets the alt_child_email_communication_sequence_steps of this EmailCommseqStep.

        Array of child steps for the alternate path  # noqa: E501

        :param alt_child_email_communication_sequence_steps: The alt_child_email_communication_sequence_steps of this EmailCommseqStep.  # noqa: E501
        :type: list[EmailCommseqStep]
        """

        self._alt_child_email_communication_sequence_steps = alt_child_email_communication_sequence_steps

    @property
    def child_email_communication_sequence_steps(self):
        """Gets the child_email_communication_sequence_steps of this EmailCommseqStep.  # noqa: E501

        Array of child steps  # noqa: E501

        :return: The child_email_communication_sequence_steps of this EmailCommseqStep.  # noqa: E501
        :rtype: list[EmailCommseqStep]
        """
        return self._child_email_communication_sequence_steps

    @child_email_communication_sequence_steps.setter
    def child_email_communication_sequence_steps(self, child_email_communication_sequence_steps):
        """Sets the child_email_communication_sequence_steps of this EmailCommseqStep.

        Array of child steps  # noqa: E501

        :param child_email_communication_sequence_steps: The child_email_communication_sequence_steps of this EmailCommseqStep.  # noqa: E501
        :type: list[EmailCommseqStep]
        """

        self._child_email_communication_sequence_steps = child_email_communication_sequence_steps

    @property
    def email_communication_sequence_step_uuid(self):
        """Gets the email_communication_sequence_step_uuid of this EmailCommseqStep.  # noqa: E501

        Email commseq step UUID  # noqa: E501

        :return: The email_communication_sequence_step_uuid of this EmailCommseqStep.  # noqa: E501
        :rtype: str
        """
        return self._email_communication_sequence_step_uuid

    @email_communication_sequence_step_uuid.setter
    def email_communication_sequence_step_uuid(self, email_communication_sequence_step_uuid):
        """Sets the email_communication_sequence_step_uuid of this EmailCommseqStep.

        Email commseq step UUID  # noqa: E501

        :param email_communication_sequence_step_uuid: The email_communication_sequence_step_uuid of this EmailCommseqStep.  # noqa: E501
        :type: str
        """

        self._email_communication_sequence_step_uuid = email_communication_sequence_step_uuid

    @property
    def email_pending_review(self):
        """Gets the email_pending_review of this EmailCommseqStep.  # noqa: E501

        True if the content of the email associated with this step is pending review by UltraCart  # noqa: E501

        :return: The email_pending_review of this EmailCommseqStep.  # noqa: E501
        :rtype: bool
        """
        return self._email_pending_review

    @email_pending_review.setter
    def email_pending_review(self, email_pending_review):
        """Sets the email_pending_review of this EmailCommseqStep.

        True if the content of the email associated with this step is pending review by UltraCart  # noqa: E501

        :param email_pending_review: The email_pending_review of this EmailCommseqStep.  # noqa: E501
        :type: bool
        """

        self._email_pending_review = email_pending_review

    @property
    def email_rejected(self):
        """Gets the email_rejected of this EmailCommseqStep.  # noqa: E501

        True if the content of the email associated with this step was rejected during review by UltraCart  # noqa: E501

        :return: The email_rejected of this EmailCommseqStep.  # noqa: E501
        :rtype: bool
        """
        return self._email_rejected

    @email_rejected.setter
    def email_rejected(self, email_rejected):
        """Sets the email_rejected of this EmailCommseqStep.

        True if the content of the email associated with this step was rejected during review by UltraCart  # noqa: E501

        :param email_rejected: The email_rejected of this EmailCommseqStep.  # noqa: E501
        :type: bool
        """

        self._email_rejected = email_rejected

    @property
    def email_requires_review(self):
        """Gets the email_requires_review of this EmailCommseqStep.  # noqa: E501

        True if the content of the email associated with this step requires review by UltraCart  # noqa: E501

        :return: The email_requires_review of this EmailCommseqStep.  # noqa: E501
        :rtype: bool
        """
        return self._email_requires_review

    @email_requires_review.setter
    def email_requires_review(self, email_requires_review):
        """Sets the email_requires_review of this EmailCommseqStep.

        True if the content of the email associated with this step requires review by UltraCart  # noqa: E501

        :param email_requires_review: The email_requires_review of this EmailCommseqStep.  # noqa: E501
        :type: bool
        """

        self._email_requires_review = email_requires_review

    @property
    def filter_profile_equation_json(self):
        """Gets the filter_profile_equation_json of this EmailCommseqStep.  # noqa: E501

        Filter profile equation JSON  # noqa: E501

        :return: The filter_profile_equation_json of this EmailCommseqStep.  # noqa: E501
        :rtype: str
        """
        return self._filter_profile_equation_json

    @filter_profile_equation_json.setter
    def filter_profile_equation_json(self, filter_profile_equation_json):
        """Sets the filter_profile_equation_json of this EmailCommseqStep.

        Filter profile equation JSON  # noqa: E501

        :param filter_profile_equation_json: The filter_profile_equation_json of this EmailCommseqStep.  # noqa: E501
        :type: str
        """

        self._filter_profile_equation_json = filter_profile_equation_json

    @property
    def merchant_notes(self):
        """Gets the merchant_notes of this EmailCommseqStep.  # noqa: E501

        Internal merchant notes  # noqa: E501

        :return: The merchant_notes of this EmailCommseqStep.  # noqa: E501
        :rtype: str
        """
        return self._merchant_notes

    @merchant_notes.setter
    def merchant_notes(self, merchant_notes):
        """Sets the merchant_notes of this EmailCommseqStep.

        Internal merchant notes  # noqa: E501

        :param merchant_notes: The merchant_notes of this EmailCommseqStep.  # noqa: E501
        :type: str
        """

        self._merchant_notes = merchant_notes

    @property
    def step_config_json(self):
        """Gets the step_config_json of this EmailCommseqStep.  # noqa: E501

        Arbitrary Configuration for a step  # noqa: E501

        :return: The step_config_json of this EmailCommseqStep.  # noqa: E501
        :rtype: str
        """
        return self._step_config_json

    @step_config_json.setter
    def step_config_json(self, step_config_json):
        """Sets the step_config_json of this EmailCommseqStep.

        Arbitrary Configuration for a step  # noqa: E501

        :param step_config_json: The step_config_json of this EmailCommseqStep.  # noqa: E501
        :type: str
        """

        self._step_config_json = step_config_json

    @property
    def type(self):
        """Gets the type of this EmailCommseqStep.  # noqa: E501

        Type of step  # noqa: E501

        :return: The type of this EmailCommseqStep.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this EmailCommseqStep.

        Type of step  # noqa: E501

        :param type: The type of this EmailCommseqStep.  # noqa: E501
        :type: str
        """
        allowed_values = ["begin", "wait", "email", "merge", "condition", "end"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(EmailCommseqStep, dict):
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
        if not isinstance(other, EmailCommseqStep):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
