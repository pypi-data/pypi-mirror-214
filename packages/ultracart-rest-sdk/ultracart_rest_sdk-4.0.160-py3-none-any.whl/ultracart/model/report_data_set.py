"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from ultracart.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from ultracart.exceptions import ApiAttributeError


def lazy_import():
    from ultracart.model.report_data_set_page import ReportDataSetPage
    from ultracart.model.report_data_set_schema import ReportDataSetSchema
    globals()['ReportDataSetPage'] = ReportDataSetPage
    globals()['ReportDataSetSchema'] = ReportDataSetSchema


class ReportDataSet(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
        ('for_object_type',): {
            'SCHEMA': "schema",
            'FILTER': "filter",
            'VISUALIZATION': "visualization",
        },
    }

    validations = {
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'data_set_query_uuid': (str,),  # noqa: E501
            'data_set_uuid': (str,),  # noqa: E501
            'destination_table_id': (str,),  # noqa: E501
            'error_message': (str,),  # noqa: E501
            'executed_sql': (str,),  # noqa: E501
            'for_object_id': (str,),  # noqa: E501
            'for_object_type': (str,),  # noqa: E501
            'initial_pages': ([ReportDataSetPage],),  # noqa: E501
            'max_results': (int,),  # noqa: E501
            'merchant_id': (str,),  # noqa: E501
            'page_count': (int,),  # noqa: E501
            'page_size': (int,),  # noqa: E501
            'request_dts': (str,),  # noqa: E501
            'schema': ([ReportDataSetSchema],),  # noqa: E501
            'security_level': (str,),  # noqa: E501
            'timezone': (str,),  # noqa: E501
            'user_data': (str,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'data_set_query_uuid': 'data_set_query_uuid',  # noqa: E501
        'data_set_uuid': 'data_set_uuid',  # noqa: E501
        'destination_table_id': 'destination_table_id',  # noqa: E501
        'error_message': 'error_message',  # noqa: E501
        'executed_sql': 'executed_sql',  # noqa: E501
        'for_object_id': 'for_object_id',  # noqa: E501
        'for_object_type': 'for_object_type',  # noqa: E501
        'initial_pages': 'initial_pages',  # noqa: E501
        'max_results': 'max_results',  # noqa: E501
        'merchant_id': 'merchant_id',  # noqa: E501
        'page_count': 'page_count',  # noqa: E501
        'page_size': 'page_size',  # noqa: E501
        'request_dts': 'request_dts',  # noqa: E501
        'schema': 'schema',  # noqa: E501
        'security_level': 'security_level',  # noqa: E501
        'timezone': 'timezone',  # noqa: E501
        'user_data': 'user_data',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """ReportDataSet - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            data_set_query_uuid (str): A unique identifier assigned to the data set query that is returned.. [optional]  # noqa: E501
            data_set_uuid (str): A unique identifier assigned to the data set that is returned.. [optional]  # noqa: E501
            destination_table_id (str): The BigQuery destination table id that contains the result.. [optional]  # noqa: E501
            error_message (str): Error message if the query failed.. [optional]  # noqa: E501
            executed_sql (str): [optional]  # noqa: E501
            for_object_id (str): An identifier that can be used to help match up the returned data set. [optional]  # noqa: E501
            for_object_type (str): The type of object this data set is for. [optional]  # noqa: E501
            initial_pages ([ReportDataSetPage]): Initial pages returned in the dataset. [optional]  # noqa: E501
            max_results (int): The total number of results. [optional]  # noqa: E501
            merchant_id (str): Merchant that owns this data set. [optional]  # noqa: E501
            page_count (int): The total number of pages in the result set. [optional]  # noqa: E501
            page_size (int): The size of the pages. [optional]  # noqa: E501
            request_dts (str): Date/Time of the client submitted the request.  Can be used to resolve out of order query completion results. [optional]  # noqa: E501
            schema ([ReportDataSetSchema]): The schema associated with the data set.. [optional]  # noqa: E501
            security_level (str): Security level this dataset was read from.. [optional]  # noqa: E501
            timezone (str): [optional]  # noqa: E501
            user_data (str): Any other data that needs to be returned with the response to help the UI. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """ReportDataSet - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            data_set_query_uuid (str): A unique identifier assigned to the data set query that is returned.. [optional]  # noqa: E501
            data_set_uuid (str): A unique identifier assigned to the data set that is returned.. [optional]  # noqa: E501
            destination_table_id (str): The BigQuery destination table id that contains the result.. [optional]  # noqa: E501
            error_message (str): Error message if the query failed.. [optional]  # noqa: E501
            executed_sql (str): [optional]  # noqa: E501
            for_object_id (str): An identifier that can be used to help match up the returned data set. [optional]  # noqa: E501
            for_object_type (str): The type of object this data set is for. [optional]  # noqa: E501
            initial_pages ([ReportDataSetPage]): Initial pages returned in the dataset. [optional]  # noqa: E501
            max_results (int): The total number of results. [optional]  # noqa: E501
            merchant_id (str): Merchant that owns this data set. [optional]  # noqa: E501
            page_count (int): The total number of pages in the result set. [optional]  # noqa: E501
            page_size (int): The size of the pages. [optional]  # noqa: E501
            request_dts (str): Date/Time of the client submitted the request.  Can be used to resolve out of order query completion results. [optional]  # noqa: E501
            schema ([ReportDataSetSchema]): The schema associated with the data set.. [optional]  # noqa: E501
            security_level (str): Security level this dataset was read from.. [optional]  # noqa: E501
            timezone (str): [optional]  # noqa: E501
            user_data (str): Any other data that needs to be returned with the response to help the UI. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
