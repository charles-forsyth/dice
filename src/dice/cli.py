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
    advantage: bool = typer.Option(
        False, "--advantage", "-adv", help="Roll twice and take the higher result"
    ),
    disadvantage: bool = typer.Option(
        False, "--disadvantage", "-dis", help="Roll twice and take the lower result"
    ),
) -> None:
    """Roll dice with flair!"""
    try:
        count, sides, modifier = parse_dice_string(notation)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)

    result = roll_dice(count, sides, modifier, advantage, disadvantage)

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

    # Adjust title for method
    if result.method == "advantage":
        title += " (Advantage)"
    elif result.method == "disadvantage":
        title += " (Disadvantage)"

    table = Table(show_header=False, border_style=color)
    table.add_column("Die", justify="right")
    table.add_column("Result")

    # Main rolls
    for i, r in enumerate(result.rolls):
        table.add_row(f"Die {i + 1} (d{r.sides})", f"[bold]{r.result}[/bold]")

    # Dropped rolls visualization
    if result.dropped_rolls:
        table.add_row("---", "---")
        dropped_sum = sum(r.result for r in result.dropped_rolls)
        for i, r in enumerate(result.dropped_rolls):
            table.add_row(
                f"[dim]Dropped {i + 1} (d{r.sides})[/dim]", f"[dim]{r.result}[/dim]"
            )
        table.add_row("[dim]Dropped Total[/dim]", f"[dim]{dropped_sum}[/dim]")

    if modifier != 0:
        summary = f"\nTotal: {result.total} {'+' if modifier > 0 else ''}{modifier} = [bold cyan]{result.grand_total}[/bold cyan]"
    else:
        summary = f"\nTotal: [bold cyan]{result.total}[/bold cyan]"

    console.print(
        Panel(table, title=title, subtitle=summary, border_style=color, expand=False)
    )


if __name__ == "__main__":
    app()
