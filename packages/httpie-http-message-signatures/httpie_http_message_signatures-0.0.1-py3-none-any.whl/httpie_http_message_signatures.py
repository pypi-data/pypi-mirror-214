from __future__ import annotations

import fnmatch
import hashlib
import os.path
from base64 import b64decode
from configparser import ConfigParser
from typing import Sequence, NamedTuple, Optional
from urllib.parse import urlsplit, parse_qs

from http_message_signatures import HTTPSignatureKeyResolver, HTTPMessageSigner, algorithms
from http_sfv import Item, Dictionary
from httpie.plugins import AuthPlugin
from requests import PreparedRequest
from requests.auth import AuthBase

DEFAULT_COVERED_COMPONENT_IDS = ('@method', '@authority', '@target-uri')


class HostConfiguration(NamedTuple):
    host: str
    key_id: str
    key: bytes
    covered_component_ids: Sequence[str]


class HttpSignatureAuthPlugin(AuthPlugin):
    auth_type = 'message-signature'
    auth_require = False
    auth_parse = False

    def parse_raw_auth(self) -> Optional[ConfigParser]:
        if not self.raw_auth:
            return None

        try:
            key_id, key, *components = self.raw_auth.split(':')
        except ValueError as e:
            raise ValueError('Bad argument passed to -a/--auth parameter: use format "key_id:key[:components]"') from e

        config = {'key_id': key_id, 'key': key}

        if components:
            config['covered_component_ids'] = components[0]

        return ConfigParser(config)

    @staticmethod
    def parse_rc_file() -> ConfigParser:
        config = ConfigParser()
        config.read(os.path.expanduser('~/.httpmessagesignaturesrc'))
        return config

    def get_auth(self, *_) -> HttpSignatureAuth:
        config = self.parse_raw_auth()

        if not config:
            config = self.parse_rc_file()

        return HttpSignatureAuth(config)


def add_digest(configuration: HostConfiguration, request: PreparedRequest):
    if 'content-digest' in configuration.covered_component_ids and request.body:
        request.headers['Content-Digest'] = str(Dictionary({'sha-256': hashlib.sha256(request.body).digest()}))


def resolve_covered_component_ids(components: Sequence[str], request: PreparedRequest) -> Sequence[str]:
    resolved_components = []

    for component in components:
        if component == '@query-params':
            for param in parse_qs(urlsplit(request.url).query):
                item = Item('@query-params')
                item.params['name'] = param
                resolved_components.append(str(item))
        elif component != 'content-digest' or request.body:
            resolved_components.append(component)

    return resolved_components


def sign(configuration: HostConfiguration, request: PreparedRequest):
    key_resolver = SingleHttpSignatureKeyResolver(configuration.key_id, configuration.key)
    components = resolve_covered_component_ids(configuration.covered_component_ids, request)
    signer = HTTPMessageSigner(signature_algorithm=algorithms.HMAC_SHA256, key_resolver=key_resolver)
    signer.sign(request, key_id=configuration.key_id, covered_component_ids=components)


class SingleHttpSignatureKeyResolver(HTTPSignatureKeyResolver):
    def __init__(self, key_id: str, key: bytes):
        self.key_id = key_id
        self.key = key

    def resolve_private_key(self, key_id: str):
        assert self.key_id == key_id
        return self.key


class HttpSignatureAuth(AuthBase):
    def __init__(self, configurations: ConfigParser):
        self.configurations = configurations

    def configuration_for(self, host: str) -> HostConfiguration:
        defaults = self.configurations.defaults()

        for host_pattern, values in self.configurations.items():
            if fnmatch.fnmatch(host, host_pattern):
                values = {**defaults, **values}
                break
        else:
            values = defaults

        components = values.get('covered_component_ids', ','.join(DEFAULT_COVERED_COMPONENT_IDS)).split(',')
        components = list(map(str.strip, map(str.lower, components)))

        try:
            return HostConfiguration(host, values['key_id'], b64decode(values['key']), components)
        except KeyError as e:
            raise LookupError(f'No {e.args[0]} parameter found for host {host}') from e

    def __call__(self, r: PreparedRequest):
        host = urlsplit(r.url).netloc
        configuration = self.configuration_for(host)
        add_digest(configuration, r)
        sign(configuration, r)
        return r
