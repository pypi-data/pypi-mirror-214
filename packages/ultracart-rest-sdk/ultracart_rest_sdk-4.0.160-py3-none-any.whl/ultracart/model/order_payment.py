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
    from ultracart.model.currency import Currency
    from ultracart.model.order_payment_check import OrderPaymentCheck
    from ultracart.model.order_payment_credit_card import OrderPaymentCreditCard
    from ultracart.model.order_payment_e_check import OrderPaymentECheck
    from ultracart.model.order_payment_insurance import OrderPaymentInsurance
    from ultracart.model.order_payment_purchase_order import OrderPaymentPurchaseOrder
    from ultracart.model.order_payment_transaction import OrderPaymentTransaction
    globals()['Currency'] = Currency
    globals()['OrderPaymentCheck'] = OrderPaymentCheck
    globals()['OrderPaymentCreditCard'] = OrderPaymentCreditCard
    globals()['OrderPaymentECheck'] = OrderPaymentECheck
    globals()['OrderPaymentInsurance'] = OrderPaymentInsurance
    globals()['OrderPaymentPurchaseOrder'] = OrderPaymentPurchaseOrder
    globals()['OrderPaymentTransaction'] = OrderPaymentTransaction


class OrderPayment(ModelNormal):
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
        ('payment_method',): {
            'AFFIRM': "Affirm",
            'AMAZON': "Amazon",
            'AMAZON_SC': "Amazon SC",
            'CASH': "Cash",
            'CHECK': "Check",
            'COD': "COD",
            'CREDIT_CARD': "Credit Card",
            'EBAY': "eBay",
            'ECHECK': "eCheck",
            'GOOGLE_SHOPPING': "Google Shopping",
            'INSURANCE': "Insurance",
            'LOANHERO': "LoanHero",
            'MONEY_ORDER': "Money Order",
            'PAYPAL': "PayPal",
            'PURCHASE_ORDER': "Purchase Order",
            'QUOTE_REQUEST': "Quote Request",
            'UNKNOWN': "Unknown",
            'WIRE_TRANSFER': "Wire Transfer",
            'WALMART': "Walmart",
            'SHOP.COM': "Shop.com",
            'SEZZLE': "Sezzle",
            'VENMO': "Venmo",
        },
        ('payment_status',): {
            'UNPROCESSED': "Unprocessed",
            'AUTHORIZED': "Authorized",
            'CAPTURE_FAILED': "Capture Failed",
            'PROCESSED': "Processed",
            'DECLINED': "Declined",
            'VOIDED': "Voided",
            'REFUNDED': "Refunded",
            'SKIPPED': "Skipped",
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
            'check': (OrderPaymentCheck,),  # noqa: E501
            'credit_card': (OrderPaymentCreditCard,),  # noqa: E501
            'echeck': (OrderPaymentECheck,),  # noqa: E501
            'hold_for_fraud_review': (bool,),  # noqa: E501
            'insurance': (OrderPaymentInsurance,),  # noqa: E501
            'payment_dts': (str,),  # noqa: E501
            'payment_method': (str,),  # noqa: E501
            'payment_method_accounting_code': (str,),  # noqa: E501
            'payment_method_deposit_to_account': (str,),  # noqa: E501
            'payment_status': (str,),  # noqa: E501
            'purchase_order': (OrderPaymentPurchaseOrder,),  # noqa: E501
            'rotating_transaction_gateway_code': (str,),  # noqa: E501
            'surcharge': (Currency,),  # noqa: E501
            'surcharge_accounting_code': (str,),  # noqa: E501
            'surcharge_transaction_fee': (float,),  # noqa: E501
            'surcharge_transaction_percentage': (float,),  # noqa: E501
            'test_order': (bool,),  # noqa: E501
            'transactions': ([OrderPaymentTransaction],),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'check': 'check',  # noqa: E501
        'credit_card': 'credit_card',  # noqa: E501
        'echeck': 'echeck',  # noqa: E501
        'hold_for_fraud_review': 'hold_for_fraud_review',  # noqa: E501
        'insurance': 'insurance',  # noqa: E501
        'payment_dts': 'payment_dts',  # noqa: E501
        'payment_method': 'payment_method',  # noqa: E501
        'payment_method_accounting_code': 'payment_method_accounting_code',  # noqa: E501
        'payment_method_deposit_to_account': 'payment_method_deposit_to_account',  # noqa: E501
        'payment_status': 'payment_status',  # noqa: E501
        'purchase_order': 'purchase_order',  # noqa: E501
        'rotating_transaction_gateway_code': 'rotating_transaction_gateway_code',  # noqa: E501
        'surcharge': 'surcharge',  # noqa: E501
        'surcharge_accounting_code': 'surcharge_accounting_code',  # noqa: E501
        'surcharge_transaction_fee': 'surcharge_transaction_fee',  # noqa: E501
        'surcharge_transaction_percentage': 'surcharge_transaction_percentage',  # noqa: E501
        'test_order': 'test_order',  # noqa: E501
        'transactions': 'transactions',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """OrderPayment - a model defined in OpenAPI

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
            check (OrderPaymentCheck): [optional]  # noqa: E501
            credit_card (OrderPaymentCreditCard): [optional]  # noqa: E501
            echeck (OrderPaymentECheck): [optional]  # noqa: E501
            hold_for_fraud_review (bool): True if order has been held for fraud review. [optional]  # noqa: E501
            insurance (OrderPaymentInsurance): [optional]  # noqa: E501
            payment_dts (str): Date/time that the payment was successfully processed, for new orders, this field is only considered if channel_partner.skip_payment_processing is true. [optional]  # noqa: E501
            payment_method (str): Payment method. [optional]  # noqa: E501
            payment_method_accounting_code (str): Payment method QuickBooks code. [optional]  # noqa: E501
            payment_method_deposit_to_account (str): Payment method QuickBooks deposit account. [optional]  # noqa: E501
            payment_status (str): Payment status. [optional]  # noqa: E501
            purchase_order (OrderPaymentPurchaseOrder): [optional]  # noqa: E501
            rotating_transaction_gateway_code (str): Rotating transaction gateway code used to process this order. [optional]  # noqa: E501
            surcharge (Currency): [optional]  # noqa: E501
            surcharge_accounting_code (str): Surcharge accounting code. [optional]  # noqa: E501
            surcharge_transaction_fee (float): Surcharge transaction fee. [optional]  # noqa: E501
            surcharge_transaction_percentage (float): Surcharge transaction percentage. [optional]  # noqa: E501
            test_order (bool): True if this is a test order. [optional]  # noqa: E501
            transactions ([OrderPaymentTransaction]): Transactions associated with processing this payment. [optional]  # noqa: E501
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
        """OrderPayment - a model defined in OpenAPI

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
            check (OrderPaymentCheck): [optional]  # noqa: E501
            credit_card (OrderPaymentCreditCard): [optional]  # noqa: E501
            echeck (OrderPaymentECheck): [optional]  # noqa: E501
            hold_for_fraud_review (bool): True if order has been held for fraud review. [optional]  # noqa: E501
            insurance (OrderPaymentInsurance): [optional]  # noqa: E501
            payment_dts (str): Date/time that the payment was successfully processed, for new orders, this field is only considered if channel_partner.skip_payment_processing is true. [optional]  # noqa: E501
            payment_method (str): Payment method. [optional]  # noqa: E501
            payment_method_accounting_code (str): Payment method QuickBooks code. [optional]  # noqa: E501
            payment_method_deposit_to_account (str): Payment method QuickBooks deposit account. [optional]  # noqa: E501
            payment_status (str): Payment status. [optional]  # noqa: E501
            purchase_order (OrderPaymentPurchaseOrder): [optional]  # noqa: E501
            rotating_transaction_gateway_code (str): Rotating transaction gateway code used to process this order. [optional]  # noqa: E501
            surcharge (Currency): [optional]  # noqa: E501
            surcharge_accounting_code (str): Surcharge accounting code. [optional]  # noqa: E501
            surcharge_transaction_fee (float): Surcharge transaction fee. [optional]  # noqa: E501
            surcharge_transaction_percentage (float): Surcharge transaction percentage. [optional]  # noqa: E501
            test_order (bool): True if this is a test order. [optional]  # noqa: E501
            transactions ([OrderPaymentTransaction]): Transactions associated with processing this payment. [optional]  # noqa: E501
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
