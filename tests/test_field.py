# -*- coding: utf-8 -*-
"""
    tests/test_field.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
import pytest
from trytond.transaction import Transaction


class TestField:

    def test_encrypted_char_field(self, transaction):
        EncryptedCharField = self.POOL.get('encrypted_char_field')

        char = "this is secret char"
        record = EncryptedCharField()
        record.char = char
        record.save()

        cursor = Transaction().connection.cursor()
        sql_table = EncryptedCharField.__table__()
        cursor.execute(*sql_table.select(sql_table.id, sql_table.char))
        row, = cursor.fetchall()

        assert row[0] == record.id
        assert row[1] != char
        assert record.char == char

    def test_encrypted_text_field(self, transaction):
        EncryptedTextField = self.POOL.get('encrypted_text_field')

        text = """
        Lorem Ipsum is simply dummy text of the printing and typesetting
        industry. Lorem Ipsum has been the industry's standard dummy text
        ever since the 1500s, when an unknown printer took a galley of type
        and scrambled it to make a type specimen book.
        """
        record = EncryptedTextField()
        record.text = text
        record.save()

        cursor = Transaction().connection.cursor()
        sql_table = EncryptedTextField.__table__()
        cursor.execute(*sql_table.select(sql_table.id, sql_table.text))
        row, = cursor.fetchall()

        assert row[0] == record.id
        assert row[1] != text
        assert record.text == text

    def test_encrypted_selection_field(self, transaction):
        EncryptedSelectionField = self.POOL.get('encrypted_selection_field')

        selection = "value1"
        record = EncryptedSelectionField()
        record.selection = selection
        record.save()

        cursor = Transaction().connection.cursor()
        sql_table = EncryptedSelectionField.__table__()
        cursor.execute(*sql_table.select(sql_table.id, sql_table.selection))
        row, = cursor.fetchall()

        assert row[0] == record.id
        assert row[1] != selection
        assert record.selection == selection

    def test_encrypted_field_search(self, transaction):
        EncryptedCharField = self.POOL.get('encrypted_char_field')

        rec1 = EncryptedCharField()
        rec1.name = 'name1'
        rec1.char = 'secret1'
        rec1.save()

        rec2 = EncryptedCharField()
        rec2.name = 'name2'
        rec2.char = 'secret2'
        rec2.save()

        rec3 = EncryptedCharField()
        rec3.name = 'name1'
        rec3.save()

        assert EncryptedCharField.search([('char', '=', None)], count=True) == 1  # noqa
        assert EncryptedCharField.search([('char', '!=', None)], count=True) == 2  # noqa

        with pytest.raises(AssertionError):
            EncryptedCharField.search([('char', '=', 'secret1')])
