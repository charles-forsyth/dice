import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dice.engine import roll_dice, parse_dice_string

app = typer.Typer(
    help="⚔️ Skywalker Dice - Precision rolling for the modern adventurer."
)
console = Console()


@app.command()
def roll(
    notation: str = typer.Argument(
        "1d20", help="Dice notation (e.g., '2d6+2', '1d20')"
    ),
    theme: str = typer.Option(
        "default",
        "--theme",
        "-t",
        help="Theme to use (default, dd-fighter, dd-wizard, catan)",
    ),
) -> None:
    """Roll dice with flair!"""
    try:
        count, sides, modifier = parse_dice_string(notation)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

    result = roll_dice(count, sides, modifier)

    # Theme processing
    color = "white"
    title = "Dice Roll"

    if theme == "dd-fighter":
        color = "red"
        title = "⚔️ Fighter's Might"
    elif theme == "dd-wizard":
        color = "purple"
        title = "🪄 Wizard's Arcana"
    elif theme == "catan":
        color = "yellow"
        title = "🏘️ Catan Roll"
        if sides != 6:
            console.print("[yellow]Warning:[/yellow] Catan usually uses d6!")

    table = Table(show_header=False, border_style=color)
    table.add_column("Die", justify="right")
    table.add_column("Result")

    for i, r in enumerate(result.rolls):
        table.add_row(f"Die {i + 1} (d{r.sides})", f"[bold]{r.result}[/bold]")

    if modifier != 0:
        summary = f"\nTotal: {result.total} {'+' if modifier > 0 else ''}{modifier} = [bold cyan]{result.grand_total}[/bold cyan]"
    else:
        summary = f"\nTotal: [bold cyan]{result.total}[/bold cyan]"

    console.print(
        Panel(table, title=title, subtitle=summary, border_style=color, expand=False)
    )


if __name__ == "__main__":
    app()
