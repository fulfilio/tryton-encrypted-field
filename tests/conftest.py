# -*- coding: utf-8 -*-
"""
    tests/conftest.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
import os

import pytest
from trytond.model import fields, ModelSQL
from trytond.config import config
from cryptography.fernet import Fernet
from trytond_encrypted_field import EncryptedField


class EncryptedCharField(ModelSQL):
    "Test Model with char EncryptedField"
    __name__ = "encrypted_char_field"

    name = fields.Char('Name')
    char = EncryptedField(fields.Char('Char'))


class EncryptedTextField(ModelSQL):
    "Test Model with text EncryptedField"
    __name__ = "encrypted_text_field"

    name = fields.Char('Name')
    text = EncryptedField(fields.Text('Text'))


class EncryptedSelectionField(ModelSQL):
    "Test Model with selection EncryptedField"
    __name__ = "encrypted_selection_field"

    name = fields.Char('Name')
    selection = EncryptedField(
        fields.Selection([
            ('value1', 'Value 1'),
            ('value2', 'Value 2'),
        ], 'Selection')
    )


@pytest.fixture(scope='session', autouse=True)
def install_module(request):
    """Install tryton module in specified database.
    """
    os.environ['TRYTOND_DATABASE_URI'] = "postgresql://"
    os.environ['DB_NAME'] = 'test_enc_field'
    config.set('database', 'uri', os.environ['TRYTOND_DATABASE_URI'])
    os.environ['TRYTOND_ENCRYPTED_FIELD__SECRET_KEY'] = (
        Fernet.generate_key().decode('utf-8')
    )
    from trytond.tests import test_tryton
    from trytond.pool import Pool

    Pool.register(
        EncryptedCharField,
        EncryptedTextField,
        EncryptedSelectionField,
        module='tests', type_='model'
    )
    test_tryton.activate_module('tests')


@pytest.yield_fixture()
def transaction(request):
    """Yields transaction with installed module.
    """
    from trytond.transaction import Transaction
    from trytond.tests.test_tryton import USER, CONTEXT, DB_NAME, Pool

    # Inject helper functions in instance on which test function was collected.
    request.instance.POOL = Pool(DB_NAME)
    request.instance.USER = USER
    request.instance.CONTEXT = CONTEXT
    request.instance.DB_NAME = DB_NAME

    with Transaction().start(DB_NAME, USER, context=CONTEXT) as transaction:
        yield transaction

        transaction.rollback()
