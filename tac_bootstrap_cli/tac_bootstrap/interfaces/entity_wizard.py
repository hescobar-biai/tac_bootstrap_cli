"""
Entity Field Wizard

Interactive wizard for defining entity fields during entity generation.
Prompts user for field specifications (name, type, required flag) in a loop
until all fields are defined.
"""

from typing import List

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from tac_bootstrap.domain.entity_config import FieldSpec, FieldType

# Supported field types for entity generation
SUPPORTED_TYPES = [
    ("str", "String (VARCHAR)", FieldType.STRING),
    ("int", "Integer", FieldType.INTEGER),
    ("float", "Floating point", FieldType.FLOAT),
    ("bool", "Boolean", FieldType.BOOLEAN),
    ("datetime", "Timestamp", FieldType.DATETIME),
    ("uuid", "UUID", FieldType.UUID),
    ("text", "Large text (TEXT)", FieldType.TEXT),
    ("decimal", "Fixed-precision decimal", FieldType.DECIMAL),
    ("json", "JSON data", FieldType.JSON),
]

console = Console()


def run_entity_field_wizard() -> List[FieldSpec]:
    """
    Run interactive wizard to collect entity field specifications.

    Prompts user in a loop to define fields with name, type, and required flag.
    Continues until user chooses to finish.

    Returns:
        List of FieldSpec objects

    Raises:
        SystemExit: If user cancels with Ctrl+C
        ValueError: If no fields are defined

    Example:
        >>> fields = run_entity_field_wizard()
        >>> for field in fields:
        ...     print(f"{field.name}: {field.field_type}")
    """
    console.print("\n[bold cyan]Define Entity Fields[/bold cyan]")
    console.print(
        "[dim]You'll be prompted to add fields one at a time. Press Ctrl+C to cancel.[/dim]\n"
    )

    fields: List[FieldSpec] = []

    try:
        while True:
            # Show current fields count
            if fields:
                console.print(
                    f"\n[dim]Current fields: {len(fields)}[/dim]"
                )

            # Prompt for field name
            field_name = Prompt.ask(
                "[bold]Field name[/bold] (snake_case)",
                default="" if not fields else None,
            )

            # Allow empty input to finish if at least one field exists
            if not field_name and fields:
                break

            if not field_name:
                console.print("[yellow]Field name cannot be empty. Please try again.[/yellow]")
                continue

            # Validate field name pattern (will be validated by FieldSpec Pydantic model)
            # Just give user a hint here
            if not field_name.islower() or " " in field_name:
                console.print(
                    "[yellow]Tip: Use snake_case (lowercase with underscores)[/yellow]"
                )

            # Show field types table
            table = Table(title="Available Field Types", show_header=True)
            table.add_column("Option", style="cyan", width=6)
            table.add_column("Type", style="green")
            table.add_column("Description", style="dim")

            for idx, (short_name, description, _) in enumerate(SUPPORTED_TYPES, 1):
                table.add_row(str(idx), short_name, description)

            console.print(table)

            # Prompt for field type
            while True:
                type_choice = Prompt.ask(
                    "[bold]Field type[/bold] (select number)",
                    default="1",
                )

                try:
                    type_idx = int(type_choice) - 1
                    if 0 <= type_idx < len(SUPPORTED_TYPES):
                        selected_type = SUPPORTED_TYPES[type_idx][2]
                        break
                    else:
                        max_num = len(SUPPORTED_TYPES)
                        console.print(
                            f"[yellow]Please enter a number between 1 and {max_num}[/yellow]"
                        )
                except ValueError:
                    console.print("[yellow]Please enter a valid number[/yellow]")

            # Prompt for required flag
            is_required = Confirm.ask(
                "[bold]Is this field required?[/bold]",
                default=True,
            )

            # Create FieldSpec (this will validate the field name)
            try:
                field_spec = FieldSpec(
                    name=field_name,
                    field_type=selected_type,
                    required=is_required,
                )
                fields.append(field_spec)
                req_status = 'required' if is_required else 'optional'
                console.print(
                    f"[green]✓[/green] Added field: [bold]{field_name}[/bold] "
                    f"({selected_type.value}, {req_status})"
                )

            except ValueError as e:
                console.print(f"[red]Invalid field:[/red] {e}")
                console.print("[yellow]Please try again with a different name.[/yellow]")
                continue

            # Ask if user wants to add another field
            add_another = Confirm.ask(
                "\n[bold]Add another field?[/bold]",
                default=True,
            )

            if not add_another:
                break

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Wizard cancelled by user[/yellow]")
        raise SystemExit(1)

    # Validate at least one field was added
    if not fields:
        console.print("[red]Error: Entity must have at least one field[/red]")
        raise ValueError("No fields defined")

    # Show summary
    console.print(f"\n[green]✓ Defined {len(fields)} field(s)[/green]")
    return fields
