import random
import uuid

from dcicutils.misc_utils import utc_now_str
from jsonschema_serialize_fork import NO_DEFAULT
from pyramid.path import DottedNameResolver
from pyramid.threadlocal import get_current_request
from snovault.schema_utils import server_default
from .interfaces import COLLECTIONS  # , ROOT
from string import digits  # , ascii_uppercase
from .project_app import app_project
from .server_defaults_user import _userid, get_userid, get_user_resource


ACCESSION_FACTORY = __name__ + ':accession_factory'
ACCESSION_PREFIX = app_project().ACCESSION_PREFIX
ACCESSION_TEST_PREFIX = 'TST'


def includeme(config):
    accession_factory = config.registry.settings.get('accession_factory')
    if accession_factory:
        factory = DottedNameResolver().resolve(accession_factory)
    else:
        factory = enc_accession
    config.registry[ACCESSION_FACTORY] = factory


# XXX: This stuff is all added based on the serverDefault identifier in the schemas
# removing it altogether will totally break our code


@server_default
def userid(instance, subschema):  # args required by jsonschema-serialize-fork
    return _userid()


@server_default
def now(instance, subschema):  # args required by jsonschema-serialize-fork
    return utc_now_str()


@server_default
def uuid4(instance, subschema):
    return str(uuid.uuid4())


@server_default
def accession(instance, subschema):
    if 'external_accession' in instance:
        return NO_DEFAULT
    request = get_current_request()
    factory = request.registry[ACCESSION_FACTORY]
    # With 17 576 000 options
    ATTEMPTS = 10
    for attempt in range(ATTEMPTS):
        new_accession = factory(subschema['accessionType'])
        if new_accession in request.root:
            continue
        return new_accession
    raise AssertionError("Free accession not found in %d attempts" % ATTEMPTS)


def get_now():
    """ Wrapper for the server_default 'now' above so it is not called through SERVER_DEFAULTS in our code """
    return utc_now_str()


def add_last_modified(properties, **kwargs):
    """
        Uses the above two functions to add the last_modified information to the item
        May have no effect
        Allow someone to override the request userid (none in this case) by passing in a different uuid
        CONSIDER: `last_modified` (and `last_text_edited`) are not really 'server defaults' but rather system-managed fields.
    """

    userid = kwargs.get("userid", None)
    field_name_portion = kwargs.get("field_name_portion", "modified")

    last_field_name = "last_" + field_name_portion  # => last_modified
    by_field_name = field_name_portion + "_by"      # => modified_by
    date_field_name = "date_" + field_name_portion  # => date_modified

    try:
        last_modified = {
            by_field_name: get_userid(),
            date_field_name: get_now(),
        }
    except AttributeError:  # no request in scope ie: we are outside the core application.
        if userid:
            last_modified = {
                by_field_name: userid,
                date_field_name: get_now(),
            }
            properties[last_field_name] = last_modified
    else:
        # get_userid returns NO_DEFAULT if no userid
        if last_modified[by_field_name] != NO_DEFAULT:
            properties[last_field_name] = last_modified


#FDN_ACCESSION_FORMAT = (digits, digits, digits, ascii_uppercase, ascii_uppercase, ascii_uppercase)
FDN_ACCESSION_FORMAT = ['ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789']*7

def enc_accession(accession_type):
    random_part = ''.join(random.choice(s) for s in FDN_ACCESSION_FORMAT)
    return ACCESSION_PREFIX + accession_type + random_part


TEST_ACCESSION_FORMAT = (digits, ) * 7


def test_accession(accession_type):
    """ Test accessions are generated on test.encodedcc.org
    """
    random_part = ''.join(random.choice(s) for s in TEST_ACCESSION_FORMAT)
    return 'TST' + accession_type + random_part
