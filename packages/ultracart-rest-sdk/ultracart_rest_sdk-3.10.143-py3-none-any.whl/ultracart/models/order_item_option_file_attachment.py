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


class OrderItemOptionFileAttachment(object):
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
        'expiration_dts': 'str',
        'file_name': 'str',
        'mime_type': 'str',
        'size': 'int'
    }

    attribute_map = {
        'expiration_dts': 'expiration_dts',
        'file_name': 'file_name',
        'mime_type': 'mime_type',
        'size': 'size'
    }

    def __init__(self, expiration_dts=None, file_name=None, mime_type=None, size=None):  # noqa: E501
        """OrderItemOptionFileAttachment - a model defined in Swagger"""  # noqa: E501

        self._expiration_dts = None
        self._file_name = None
        self._mime_type = None
        self._size = None
        self.discriminator = None

        if expiration_dts is not None:
            self.expiration_dts = expiration_dts
        if file_name is not None:
            self.file_name = file_name
        if mime_type is not None:
            self.mime_type = mime_type
        if size is not None:
            self.size = size

    @property
    def expiration_dts(self):
        """Gets the expiration_dts of this OrderItemOptionFileAttachment.  # noqa: E501

        Expiration date/time  # noqa: E501

        :return: The expiration_dts of this OrderItemOptionFileAttachment.  # noqa: E501
        :rtype: str
        """
        return self._expiration_dts

    @expiration_dts.setter
    def expiration_dts(self, expiration_dts):
        """Sets the expiration_dts of this OrderItemOptionFileAttachment.

        Expiration date/time  # noqa: E501

        :param expiration_dts: The expiration_dts of this OrderItemOptionFileAttachment.  # noqa: E501
        :type: str
        """

        self._expiration_dts = expiration_dts

    @property
    def file_name(self):
        """Gets the file_name of this OrderItemOptionFileAttachment.  # noqa: E501

        File name  # noqa: E501

        :return: The file_name of this OrderItemOptionFileAttachment.  # noqa: E501
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """Sets the file_name of this OrderItemOptionFileAttachment.

        File name  # noqa: E501

        :param file_name: The file_name of this OrderItemOptionFileAttachment.  # noqa: E501
        :type: str
        """

        self._file_name = file_name

    @property
    def mime_type(self):
        """Gets the mime_type of this OrderItemOptionFileAttachment.  # noqa: E501

        Mime type  # noqa: E501

        :return: The mime_type of this OrderItemOptionFileAttachment.  # noqa: E501
        :rtype: str
        """
        return self._mime_type

    @mime_type.setter
    def mime_type(self, mime_type):
        """Sets the mime_type of this OrderItemOptionFileAttachment.

        Mime type  # noqa: E501

        :param mime_type: The mime_type of this OrderItemOptionFileAttachment.  # noqa: E501
        :type: str
        """

        self._mime_type = mime_type

    @property
    def size(self):
        """Gets the size of this OrderItemOptionFileAttachment.  # noqa: E501

        Size  # noqa: E501

        :return: The size of this OrderItemOptionFileAttachment.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this OrderItemOptionFileAttachment.

        Size  # noqa: E501

        :param size: The size of this OrderItemOptionFileAttachment.  # noqa: E501
        :type: int
        """

        self._size = size

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
        if issubclass(OrderItemOptionFileAttachment, dict):
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
        if not isinstance(other, OrderItemOptionFileAttachment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
