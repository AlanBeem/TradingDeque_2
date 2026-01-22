from package.stock_purchase import StockPurchase


class StockSale:
    """StockSale represents a to-be-filled sale of shares, and reports cost and profit for a filled sale."""

    def __init__(self, stock_symbol: str, quantity: int, price: float) -> None:
        self.symbol = stock_symbol
        self.quantity = quantity
        self.price = price
        self.shares = []

    def __len__(self) -> int:
        return len(self.shares)

    def __str__(self) -> str:
        out_string_list = [f"---- Stock Sale: {self.symbol} ----"]
        out_string_list.append("Cost        Price")
        for each_share in self.shares:
            out_string_list.append(f"${each_share.cost}         ${self.price}")
        out_string_list.append("- - - - - Total - - - - -")
        out_string_list.append("$" + str(self.get_profit()))
        return "\n".join(out_string_list)

    def add_sale(self, stock: StockPurchase) -> None:
        self.shares.append(stock)

    def total_cost(self) -> float:
        return sum([each_share.cost for each_share in self.shares])

    def get_profit(self) -> float:
        return self.quantity * self.price - self.total_cost()

    def is_filled(self) -> bool:
        return self.quantity == len(self)
