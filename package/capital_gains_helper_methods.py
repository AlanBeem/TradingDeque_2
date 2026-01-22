from package.stock_ledger import StockLedger
from random import SystemRandom


def display_interpret_string_as_ledger(
    input_str: str, display: bool = False
) -> StockLedger:  # O(N)
    sl = StockLedger()
    input_lines = input_str.split("\n")
    for each_line in input_lines:  # O(N=len(input_lines))
        each_split_line = each_line.split()  # splits on spaces
        # print(each_line)
        if each_line.count("Display") == 0:
            price_string = each_split_line[-1].strip(".$")
        if each_split_line[0] == "Buy":
            sl.buy(
                each_split_line[4], int(each_split_line[1]), float(price_string)
            )
        elif each_split_line[0] == "Sell":
            sl.sell(
                each_split_line[4], int(each_split_line[1]), float(price_string)
            )
        elif display:
            sl.display_ledger()
    return sl


def interpret_string_as_ledger(input_str: str) -> StockLedger:  # O(N)
    return display_interpret_string_as_ledger(input_str)


def get_buy_sell_line(
    stock_symbol: str, buy_sell_str: str, quantity: int, price: float
) -> str:  # O(1)
    # ex: "Buy 20 shares of AAPL at $45."
    return str(
        f"{buy_sell_str} {quantity} shares of {stock_symbol} at ${price}."
    )


def generate_buy_sell_lines_string(
    stock_symbols: list[str],
    number_of_transactions: int,
    minimum_quantity: int = 1,
    maximum_quantity: int = 100,
) -> tuple[str, list[int]]:  # O(N)
    """This assumes some market conditions:
    NVDA goes up.
    As a counter gets above 200, Microsoft starts to go up (before that, it goes down).
    No price is greater than 400."""
    # returned list is in order of stock_symbols, which comes from client code
    # (for example, likely will not match order in a StockLedger)
    gbss_shares_quantity_list = [0 for gbss_i in range(len(stock_symbols))]
    gbss_line_list = []
    # for nt_i in range(number_of_transactions):  # actually, could use this
    # definite loop
    counter = 0
    while (
        len(gbss_line_list) < number_of_transactions
    ):  # O(N=number_of_transactions)
        counter += 1
        a_symbol = SystemRandom().choice(stock_symbols)
        a_quantity = SystemRandom().randrange(
            minimum_quantity, maximum_quantity + 1
        )
        if a_symbol == "NVDA":
            a_price = round(
                (100 + counter)
                * (SystemRandom().random() + SystemRandom().random()),
                2,
            )
        elif a_symbol == "MSFT":
            a_price = round(
                SystemRandom().random() * 200 * (abs(200 - counter) / 200), 2
            )
        else:
            a_price = SystemRandom().randrange(150, 351)
        a_price = min(a_price, 400)
        # if a quantity is more than currently held, make it a buy
        if (
            a_quantity
            > gbss_shares_quantity_list[stock_symbols.index(a_symbol)]
        ):
            a_buy_or_sell = "Buy"
        else:  # otherwise, choose pseudorandomly
            a_buy_or_sell = SystemRandom().choice(
                ["Buy", "Sell"]
            )  # could weight this choice with more 'Sell' items, or use a
            # cutoff for a pseudorandom number
        if a_buy_or_sell == "Buy":
            gbss_shares_quantity_list[
                stock_symbols.index(a_symbol)
            ] += a_quantity
        # else:  # == 'Sell'
        if a_buy_or_sell == "Sell":
            gbss_shares_quantity_list[
                stock_symbols.index(a_symbol)
            ] -= a_quantity
        gbss_line_list.append(
            get_buy_sell_line(a_symbol, a_buy_or_sell, a_quantity, a_price)
        )
    return "\n".join(gbss_line_list), gbss_shares_quantity_list


# For testing, the total shares of each ledger entry resulting from returned str
# should match returned list[int]
