# -*- coding: utf-8 -*-
"""
    tests/conftest.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
import os
import time

import pytest
from trytond.model import fields, ModelSQL
from cryptography.fernet import Fernet
from tryton_encrypted_field import EncryptedField


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


def pytest_addoption(parser):
    parser.addoption(
        "--db", action="store", default="sqlite",
        help="Run on database: sqlite or postgres"
    )


@pytest.fixture(scope='session', autouse=True)
def install_module(request):
    """Install tryton module in specified database.
    """
    if request.config.getoption("--db") == 'sqlite':
        os.environ['TRYTOND_DATABASE_URI'] = "sqlite://"
        os.environ['DB_NAME'] = ':memory:'

    elif request.config.getoption("--db") == 'postgres':
        os.environ['TRYTOND_DATABASE_URI'] = "postgresql://"
        os.environ['DB_NAME'] = 'test_' + str(int(time.time()))

    os.environ['TRYTOND_ENCRYPTED_FIELD__SECRET_KEY'] = Fernet.generate_key()
    from trytond.tests import test_tryton
    from trytond.pool import Pool

    Pool.register(
        EncryptedCharField,
        EncryptedTextField,
        EncryptedSelectionField,
        module='tests', type_='model'
    )
    test_tryton.install_module('tests')


@pytest.yield_fixture()
def transaction(request):
    """Yields transaction with installed module.
    """
    from trytond.transaction import Transaction
    from trytond.tests.test_tryton import USER, CONTEXT, DB_NAME, POOL

    # Inject helper functions in instance on which test function was collected.
    request.instance.POOL = POOL
    request.instance.USER = USER
    request.instance.CONTEXT = CONTEXT
    request.instance.DB_NAME = DB_NAME

    with Transaction().start(DB_NAME, USER, context=CONTEXT) as transaction:
        yield transaction

        transaction.cursor.rollback()
