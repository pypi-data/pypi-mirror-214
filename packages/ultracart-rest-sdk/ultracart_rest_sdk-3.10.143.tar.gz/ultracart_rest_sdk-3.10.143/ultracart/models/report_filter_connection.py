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


class ReportFilterConnection(object):
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
        'column': 'str',
        'data_source_name': 'str'
    }

    attribute_map = {
        'column': 'column',
        'data_source_name': 'data_source_name'
    }

    def __init__(self, column=None, data_source_name=None):  # noqa: E501
        """ReportFilterConnection - a model defined in Swagger"""  # noqa: E501

        self._column = None
        self._data_source_name = None
        self.discriminator = None

        if column is not None:
            self.column = column
        if data_source_name is not None:
            self.data_source_name = data_source_name

    @property
    def column(self):
        """Gets the column of this ReportFilterConnection.  # noqa: E501


        :return: The column of this ReportFilterConnection.  # noqa: E501
        :rtype: str
        """
        return self._column

    @column.setter
    def column(self, column):
        """Sets the column of this ReportFilterConnection.


        :param column: The column of this ReportFilterConnection.  # noqa: E501
        :type: str
        """

        self._column = column

    @property
    def data_source_name(self):
        """Gets the data_source_name of this ReportFilterConnection.  # noqa: E501


        :return: The data_source_name of this ReportFilterConnection.  # noqa: E501
        :rtype: str
        """
        return self._data_source_name

    @data_source_name.setter
    def data_source_name(self, data_source_name):
        """Sets the data_source_name of this ReportFilterConnection.


        :param data_source_name: The data_source_name of this ReportFilterConnection.  # noqa: E501
        :type: str
        """

        self._data_source_name = data_source_name

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
        if issubclass(ReportFilterConnection, dict):
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
        if not isinstance(other, ReportFilterConnection):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
