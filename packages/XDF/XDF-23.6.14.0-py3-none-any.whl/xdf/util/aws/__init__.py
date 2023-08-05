"""AWS utilities."""


import configparser
import os
from typing import Optional
import warnings

import botocore
import boto3


__all__ = 'key_pair', 'client'


CREDS_FILE_PATH = os.path.expanduser('~/.aws/credentials')

if os.path.isfile(CREDS_FILE_PATH):
    CREDS = configparser.ConfigParser()

    with open(file=CREDS_FILE_PATH,
              mode='rt',
              buffering=-1,
              encoding='utf-8') as f:
        CREDS.read_file(f)

else:
    CREDS = None


_CLIENTS = {}


def key_pair(profile: str = 'default') -> tuple[Optional[str], Optional[str]]:
    """Get AWS key pair."""
    if CREDS:
        if profile in CREDS:
            return (CREDS[profile]['aws_access_key_id'],
                    CREDS[profile]['aws_secret_access_key'])

        if (profile != 'default') and ('default' in CREDS):
            warnings.warn(
                message=(f'*** "{profile}" PROFILE DOES NOT EXIST IN '
                         f'"{CREDS_FILE_PATH}"; USING DEFAULT PROFILE ***'))

            return (CREDS['default']['aws_access_key_id'],
                    CREDS['default']['aws_secret_access_key'])

        warnings.warn(
            message=(f'*** NEITHER "{profile}" NOR "default" PROFILE EXISTS '
                     f'IN "{CREDS_FILE_PATH}"; USING EC2 INSTANCE PROFILE ***')
        )

        return None, None

    warnings.warn(
        message=(f'*** "{CREDS_FILE_PATH}" DOES NOT EXIST; '
                 'FALLING BACK TO EC2 INSTANCE PROFILE ***'))

    return None, None


def client(service_name: str, /,
           access_key_id: Optional[str] = None,
           secret_access_key: Optional[str] = None):
    """Get AWS service client."""
    global _CLIENTS   # pylint: disable=global-variable-not-assigned

    tup = service_name, access_key_id, secret_access_key

    if tup not in _CLIENTS:
        _CLIENTS[tup] = boto3.client(service_name,
                                     aws_access_key_id=access_key_id,
                                     aws_secret_access_key=secret_access_key,
                                     config=botocore.client.Config(
                                         connect_timeout=9,
                                         read_timeout=9))

    return _CLIENTS[tup]
