# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.0.256
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class SidesDefinitionRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'side': 'str',
        'side_request': 'SideDefinitionRequest'
    }

    attribute_map = {
        'side': 'side',
        'side_request': 'sideRequest'
    }

    required_map = {
        'side': 'required',
        'side_request': 'required'
    }

    def __init__(self, side=None, side_request=None, local_vars_configuration=None):  # noqa: E501
        """SidesDefinitionRequest - a model defined in OpenAPI"
        
        :param side:  A unique label identifying the side definition. (required)
        :type side: str
        :param side_request:  (required)
        :type side_request: lusid.SideDefinitionRequest

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._side = None
        self._side_request = None
        self.discriminator = None

        self.side = side
        self.side_request = side_request

    @property
    def side(self):
        """Gets the side of this SidesDefinitionRequest.  # noqa: E501

        A unique label identifying the side definition.  # noqa: E501

        :return: The side of this SidesDefinitionRequest.  # noqa: E501
        :rtype: str
        """
        return self._side

    @side.setter
    def side(self, side):
        """Sets the side of this SidesDefinitionRequest.

        A unique label identifying the side definition.  # noqa: E501

        :param side: The side of this SidesDefinitionRequest.  # noqa: E501
        :type side: str
        """
        if self.local_vars_configuration.client_side_validation and side is None:  # noqa: E501
            raise ValueError("Invalid value for `side`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                side is not None and len(side) > 64):
            raise ValueError("Invalid value for `side`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                side is not None and len(side) < 1):
            raise ValueError("Invalid value for `side`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                side is not None and not re.search(r'^[a-zA-Z0-9\-_]+$', side)):  # noqa: E501
            raise ValueError(r"Invalid value for `side`, must be a follow pattern or equal to `/^[a-zA-Z0-9\-_]+$/`")  # noqa: E501

        self._side = side

    @property
    def side_request(self):
        """Gets the side_request of this SidesDefinitionRequest.  # noqa: E501


        :return: The side_request of this SidesDefinitionRequest.  # noqa: E501
        :rtype: lusid.SideDefinitionRequest
        """
        return self._side_request

    @side_request.setter
    def side_request(self, side_request):
        """Sets the side_request of this SidesDefinitionRequest.


        :param side_request: The side_request of this SidesDefinitionRequest.  # noqa: E501
        :type side_request: lusid.SideDefinitionRequest
        """
        if self.local_vars_configuration.client_side_validation and side_request is None:  # noqa: E501
            raise ValueError("Invalid value for `side_request`, must not be `None`")  # noqa: E501

        self._side_request = side_request

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SidesDefinitionRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SidesDefinitionRequest):
            return True

        return self.to_dict() != other.to_dict()
