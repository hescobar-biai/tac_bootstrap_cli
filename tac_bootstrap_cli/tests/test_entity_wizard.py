"""Tests for entity field wizard."""

from unittest.mock import MagicMock, patch

import pytest

from tac_bootstrap.domain.entity_config import FieldType
from tac_bootstrap.interfaces.entity_wizard import run_entity_field_wizard


class TestEntityFieldWizard:
    """Test run_entity_field_wizard function."""

    @patch("tac_bootstrap.interfaces.entity_wizard.Prompt.ask")
    @patch("tac_bootstrap.interfaces.entity_wizard.Confirm.ask")
    def test_single_field(self, mock_confirm, mock_prompt):
        """Test wizard with a single field."""
        # Mock user input: one field, then stop
        mock_prompt.side_effect = [
            "product_name",  # field name
            "1",  # field type (str)
        ]
        mock_confirm.side_effect = [
            True,  # is required
            False,  # add another field? No
        ]

        fields = run_entity_field_wizard()

        assert len(fields) == 1
        assert fields[0].name == "product_name"
        assert fields[0].field_type == FieldType.STRING
        assert fields[0].required is True

    @patch("tac_bootstrap.interfaces.entity_wizard.Prompt.ask")
    @patch("tac_bootstrap.interfaces.entity_wizard.Confirm.ask")
    def test_multiple_fields(self, mock_confirm, mock_prompt):
        """Test wizard with multiple fields."""
        # Mock user input: three fields
        mock_prompt.side_effect = [
            "name",  # field 1 name
            "1",  # field 1 type (str)
            "price",  # field 2 name
            "3",  # field 2 type (float)
            "is_active",  # field 3 name
            "4",  # field 3 type (bool)
        ]
        mock_confirm.side_effect = [
            True,  # field 1 is required
            True,  # add another field? Yes
            True,  # field 2 is required
            True,  # add another field? Yes
            False,  # field 3 is not required
            False,  # add another field? No
        ]

        fields = run_entity_field_wizard()

        assert len(fields) == 3
        assert fields[0].name == "name"
        assert fields[0].field_type == FieldType.STRING
        assert fields[0].required is True

        assert fields[1].name == "price"
        assert fields[1].field_type == FieldType.FLOAT
        assert fields[1].required is True

        assert fields[2].name == "is_active"
        assert fields[2].field_type == FieldType.BOOLEAN
        assert fields[2].required is False

    @patch("tac_bootstrap.interfaces.entity_wizard.Prompt.ask")
    @patch("tac_bootstrap.interfaces.entity_wizard.Confirm.ask")
    def test_field_type_selection(self, mock_confirm, mock_prompt):
        """Test different field type selections."""
        # Mock user input for different types
        mock_prompt.side_effect = [
            "uuid_field",
            "6",  # UUID type
            "text_field",
            "7",  # TEXT type
            "json_field",
            "9",  # JSON type
        ]
        mock_confirm.side_effect = [
            True,  # required
            True,  # add another
            False,  # not required
            True,  # add another
            True,  # required
            False,  # stop
        ]

        fields = run_entity_field_wizard()

        assert len(fields) == 3
        assert fields[0].field_type == FieldType.UUID
        assert fields[1].field_type == FieldType.TEXT
        assert fields[2].field_type == FieldType.JSON

    @patch("tac_bootstrap.interfaces.entity_wizard.Prompt.ask")
    def test_keyboard_interrupt(self, mock_prompt):
        """Test wizard handles Ctrl+C gracefully."""
        # Mock KeyboardInterrupt during field name input
        mock_prompt.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit):
            run_entity_field_wizard()

    @patch("tac_bootstrap.interfaces.entity_wizard.Prompt.ask")
    @patch("tac_bootstrap.interfaces.entity_wizard.Confirm.ask")
    def test_invalid_field_name_retry(self, mock_confirm, mock_prompt):
        """Test wizard retries on invalid field name."""
        # Mock user input: invalid name first, then valid
        # When validation fails, the wizard continues the loop and asks for field name again
        mock_prompt.side_effect = [
            "class",  # Python keyword (will fail validation)
            "1",  # field type (will fail because validation happens after type selection)
            "product_class",  # valid name (retry)
            "1",  # field type
        ]
        mock_confirm.side_effect = [
            True,  # is required (first attempt)
            True,  # is required (second attempt)
            False,  # add another field? No
        ]

        fields = run_entity_field_wizard()

        # Should succeed with the valid field name
        assert len(fields) == 1
        assert fields[0].name == "product_class"

    @patch("tac_bootstrap.interfaces.entity_wizard.Prompt.ask")
    @patch("tac_bootstrap.interfaces.entity_wizard.Confirm.ask")
    def test_empty_field_name_with_existing_fields(self, mock_confirm, mock_prompt):
        """Test empty field name finishes wizard if fields exist."""
        # Mock user input: one field, then add another field, but provide empty name
        mock_prompt.side_effect = [
            "name",  # field name
            "1",  # field type
            "",  # empty name to finish (after "add another" prompt)
        ]
        mock_confirm.side_effect = [
            True,  # is required
            True,  # add another field? Yes
            # After empty name, wizard breaks loop
        ]

        fields = run_entity_field_wizard()

        assert len(fields) == 1
        assert fields[0].name == "name"
