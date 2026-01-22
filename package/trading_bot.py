from logging.config import stopListening
import time
from package.stock_ledger import StockLedger


def timing(func):
    def wrapper(*args):
        start = time.time()
        func(*args)
        return time.time() - start

    return wrapper


class TradingBot:
    # Later: TradingBot """Has methods to determine behavior as a function of
    # inputs, and these behaviors occur through execution of public methods.
    """TradingBot is for tabulation of a given sequence of buy and sell operations, and representation of combinations of buy and sell schema.\n\n
    \nbuy_setting:\n\n1: buy\n\n2: buyRandom\n\n3: buyOptimal_1\n\n4: buyOptimal_2\n\n5: buyOptimal_3\n\nsell_setting\n\n1: sell\n\n2: sellRandom\n\n3: sellOptimal_1\n\n4: sellOptimal_2\n\n5: sellOptimal_3
    """

    def __init__(
        self,
        initial_balance: float = 0,
        buy_setting: int = 1,
        sell_setting: int = 1,
    ) -> (
        None
    ):
        self.stock_ledger = StockLedger()
        self.stock_sales_list = []
        self.balance = initial_balance
        self.balance_over_transactions = [initial_balance]
        self.profit_per_sell = []
        self.buy_setting = buy_setting
        self.sell_setting = sell_setting
        self.sell_time = 0
        self.buy_time = 0

    @staticmethod
    def settings_string(buy_setting, sell_setting) -> str:
        return (
            f"{['buy', 'buyRandom', 'buyOptimal_1', 'buyOptimal_2', 'buyOptimal_3'][buy_setting - 1]},"
            f" {['sell', 'sellRandom', 'sellOptimal_1', 'sellOptimal_2', 'sellOptimal_3'][sell_setting - 1]}"
        )

    def __str__(self) -> str:
        return (
            "TradingBot:"
            f" {self.settings_string(self.buy_setting, self.sell_setting)}"
        )

    def string_to_trading_bot(
        self, input_str: str, display_bool: bool = False
    ) -> None:  # O(N) = O(len(input_str.split('\n')))
        input_lines = input_str.split("\n")
        for each_line in input_lines:  # O(N=len(input_lines))
            each_split_line = each_line.split()  # splits on spaces
            if each_line.count("Display") == 0:
                price_string = each_split_line[-1].strip(".$")
            else:
                if display_bool:
                    self.stock_ledger.display_ledger()
            if each_split_line[0] == "Buy":
                self.buy(
                    each_split_line[4],
                    int(each_split_line[1]),
                    float(price_string),
                )
            elif each_split_line[0] == "Sell":
                self.sell(
                    each_split_line[4],
                    int(each_split_line[1]),
                    float(price_string),
                )  # O(1) * O(num shares)

    # Refactored 01/19/2026:
    @timing
    def _match_buy(self, stock_symbol, quantity, price):
        if self.buy_setting == 1:  # O(1)
            self.stock_ledger.buy(stock_symbol, quantity, price)
        elif self.buy_setting == 2:  # O(N)
            self.stock_ledger.buyRandom(stock_symbol, quantity, price)
        elif self.buy_setting == 3:  # O(N)
            self.stock_ledger.buyOptimal_1(stock_symbol, quantity, price)
        elif self.buy_setting == 4:  # O(N^2)
            self.stock_ledger.buyOptimal_2(stock_symbol, quantity, price)
        elif self.buy_setting == 5:  # O(1)
            self.stock_ledger.buyOptimal_3(stock_symbol, quantity, price)


    def buy(
        self, stock_symbol: str, quantity: int, price: float
    ) -> None:  # O(f(N))
        self.buy_time += self._match_buy(stock_symbol, quantity, price)
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)

    @timing
    def _match_sell(self, stock_symbol, quantity, price):
        if self.sell_setting == 1:  # O(1)
            self.stock_sales_list.append(
                self.stock_ledger.sell(stock_symbol, quantity, price)
            )
        elif self.sell_setting == 2:  # O(N)
            self.stock_sales_list.append(
                self.stock_ledger.sellRandom(stock_symbol, quantity, price)
            )
        elif self.sell_setting == 3:  # O(N)
            self.stock_sales_list.append(
                self.stock_ledger.sellOptimal_1(stock_symbol, quantity, price)
            )
        elif self.sell_setting == 4:  # O(N^2)
            self.stock_sales_list.append(
                self.stock_ledger.sellOptimal_2(stock_symbol, quantity, price)
            )
        elif self.sell_setting == 5:  # O(1)
            self.stock_sales_list.append(
                self.stock_ledger.sellOptimal_3(stock_symbol, quantity, price)
            )

    def sell(
        self, stock_symbol: str, quantity: int, price: float
    ) -> None:  #                            # O(f(N))
        self.sell_time += self._match_sell(stock_symbol, quantity, price)
        if self.stock_sales_list[-1] is None:
            self.stock_sales_list.remove(None)
        else:
            self.balance += quantity * price
            self.profit_per_sell.append(self.last_profit())

    # end Refactored

    # $ report methods:

    def profit(self) -> float:  # O(num sold shares)
        return sum(
            [stock_sale.get_profit() for stock_sale in self.stock_sales_list]
        )

    def last_profit(self):  # O(num shares in last sale)
        if len(self.stock_sales_list) > 0:
            return self.stock_sales_list[-1].get_profit()
        else:
            return 0

    def accumulated_profit(self) -> list[float]:  # O(N)
        accumulated_profits = [0]
        for p_i in range(len(self.profit_per_sell)):
            accumulated_profits.append(sum(self.profit_per_sell[0 : p_i + 1]))
        return (
            accumulated_profits  # TODO Compare these as functions in a .ipynb
        )

    def revenue(self) -> float:  # O(N)
        return sum(
            [
                each_sale.quantity * len(each_sale.shares)
                for each_sale in self.stock_sales_list
            ]
        )

    def last_revenue(self) -> float:  # O(1)
        return (
            self.stock_sales_list[-1].quantity * self.stock_sales_list[-1].price
        )

    # elapsed time report method:

    def total_times(self) -> tuple[float, float]:  # buy time, sell time  # O(N)
        # return sum(self.buy_times), sum(self.sell_times)  # color-mix over
        # strategies (Cartesian) (try with .imshow)
        return self.buy_time, self.sell_time
