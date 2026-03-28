import os
import argparse
from dotenv import load_dotenv

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from bot.client import BinanceTestnetClient
from bot.orders import place_order

load_dotenv()

console = Console()

def create_parser():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--symbol", type=str, required=True)
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], required=True)
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT", "STOP_MARKET"], required=True)
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--price", type=float)
    parser.add_argument("--stop-price", type=float)
    
    return parser

def display_response(response: dict):
    if "orderId" in response:
        console.print(Panel(f"[bold green]Order Placed Successfully![/bold green]", expand=False))
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Order ID")
        table.add_column("Symbol")
        table.add_column("Side")
        table.add_column("Type")
        table.add_column("Status")
        table.add_column("Executed Qty")
        table.add_column("Price / AvgPrice")
        
        avg_price = response.get("avgPrice", "0")
        price = response.get("price", "0")
        display_price = price if avg_price == "0" or avg_price == "0.00000" else avg_price

        table.add_row(
            str(response.get("orderId")),
            str(response.get("symbol")),
            str(response.get("side")),
            str(response.get("type")),
            str(response.get("status")),
            str(response.get("executedQty", "0")),
            str(display_price)
        )
        console.print(table)
    else:
        console.print(Panel(f"[bold yellow]Response Received:[/bold yellow]\n{response}", expand=False))

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        console.print("[bold red]Error:[/bold red] API keys not found.")
        return

    try:
        client = BinanceTestnetClient(api_key, api_secret)
        
        console.print(f"Attempting to place [bold cyan]{args.type}[/bold cyan] order for [bold cyan]{args.qty} {args.symbol}[/bold cyan] on side [bold cyan]{args.side}[/bold cyan]...")
        
        response = place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            qty=args.qty,
            price=args.price,
            stop_price=args.stop_price
        )
        display_response(response)
        
    except ValueError as ve:
        console.print(f"[bold red]Validation Error:[/bold red] {str(ve)}")
    except Exception as e:
        console.print(f"[bold red]Execution Error:[/bold red] {str(e)}")
        console.print("[dim]Check bot.log for full details.[/dim]")

if __name__ == "__main__":
    main()
