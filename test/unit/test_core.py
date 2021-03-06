import pytest

import core

from boto3.exceptions import botocore
from botocore.exceptions import ClientError

def test_list_function_versions(mocker):
    mocker.patch.object(core.LAMBDA_CLIENT, 'list_versions_by_function')
    core.list_function_versions()
    core.LAMBDA_CLIENT.list_versions_by_function.assert_called_with(FunctionName='test function', MaxItems=100)


def test_list_function_versions_return_none(mocker):
    mocker.patch.object(core.LAMBDA_CLIENT, 'list_versions_by_function')
    core.LAMBDA_CLIENT.list_versions_by_function.side_effect = ClientError({'Error': {'Code': 'ResourceNotFoundException'}}, 'list_versions_by_function')
    assert core.list_function_versions() == None


def test_versions_to_delete_none(mocker):
    versions_response = {
        'Versions': [
            { 'Version': '$LATEST', 'LastModified': 100},
            { 'Version': 2, 'LastModified': 99}
        ]
    }

    assert core.versions_to_delete(versions_response) == None


def test_versions_to_delete_less_than_10(mocker):
    versions_response = {
        'Versions': [
            { 'Version': '$LATEST', 'LastModified': 100},
            { 'Version': 2, 'LastModified': 99},
            { 'Version': 3, 'LastModified': 98},
            { 'Version': 4, 'LastModified': 97},
            { 'Version': 5, 'LastModified': 96},
            { 'Version': 6, 'LastModified': 95},
            { 'Version': 7, 'LastModified': 94},
            { 'Version': 8, 'LastModified': 93},
            { 'Version': 9, 'LastModified': 92},
            { 'Version': 10, 'LastModified':91},
            { 'Version': 11, 'LastModified': 90},
            { 'Version': 12, 'LastModified': 89},
            { 'Version': 13, 'LastModified': 88},
            { 'Version': 14, 'LastModified': 87},
            { 'Version': 15, 'LastModified': 86}
        ]
    }
    assert core.versions_to_delete(versions_response) == [15, 14, 13, 12, 11 ]


def test_versions_to_delete_not_latest(mocker):
    versions_response = {
        'Versions': [
            { 'Version': 1, 'LastModified': 100},
            { 'Version': 2, 'LastModified': 99},
            { 'Version': 3, 'LastModified': 98},
            { 'Version': 4, 'LastModified': 97},
            { 'Version': 5, 'LastModified': 96},
            { 'Version': 6, 'LastModified': 95},
            { 'Version': 7, 'LastModified': 94},
            { 'Version': 8, 'LastModified': 93},
            { 'Version': 9, 'LastModified': 92},
            { 'Version': 10, 'LastModified':91},
            { 'Version': 11, 'LastModified': 90},
            { 'Version': 12, 'LastModified': 89},
            { 'Version': 13, 'LastModified': 88},
            { 'Version': 14, 'LastModified': 87},
            { 'Version': '$LATEST', 'LastModified': 86}
        ]
    }
    assert core.versions_to_delete(versions_response) == [14, 13, 12, 11, 10]


def test_delete_function_versions(mocker):
    mocker.patch.object(core.LAMBDA_CLIENT, 'delete_function')
    core.delete_function_version(100)
    core.LAMBDA_CLIENT.delete_function.assert_called_with(FunctionName='test function', Qualifier=100)