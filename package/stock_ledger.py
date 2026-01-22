from package.ledger_entry import LedgerEntry
from package.stock_sale import StockSale, StockPurchase
from random import SystemRandom


class StockLedger:
    def __init__(self) -> None:  # required
        self.ledger_entries = []

    def __len__(self):
        return len(self.ledger_entries)

    def __getitem__(self, index) -> LedgerEntry:
        return self.ledger_entries[index]

    def __str__(self) -> str:  # O(N=total shares)
        out_string = "Total shares:"
        for each_entry in self.ledger_entries:
            out_string += (
                f"\n{each_entry.symbol}:"
                f" {self.number_of_shares(each_entry.symbol)} shares"
            )
        return out_string

    def equals(self, other) -> bool:
        self_in_other_bool = True  # use any, and all
        other_in_self_bool = True
        self_string = str(self)
        other_string = str(other)
        for each in self_string.split("\n"):
            if not each in other_string.split("\n"):
                self_in_other_bool = False
        for each in other_string.split("\n"):
            if not each in self_string.split("\n"):
                other_in_self_bool = False
        # return str(self) == str(other)  # This takes into account abstraction
        # of instance fields for equivalence, but, as-is, it ignores a lot ('is'
        # might be a better comparison)
        return self_in_other_bool and other_in_self_bool

    def open_entry(self, stock_symbol: str) -> LedgerEntry:  # O(1)
        if not self.contains(stock_symbol):
            self.ledger_entries.append(LedgerEntry(stock_symbol))
            entry = self.ledger_entries[-1]
        else:
            entry = self.get_entry(stock_symbol)
        return entry

    def open_sale(
        self, stock_symbol: str, quantity: int, price: float
    ) -> tuple[StockSale | None, LedgerEntry | None]:  # O(number of shares)
        sale = StockSale(stock_symbol, quantity, price)
        sell_entry = self.get_entry(stock_symbol)  # O(number of entries)
        if sell_entry is None:
            print(
                f"Stock symbol not found for {quantity} shares of"
                f" {stock_symbol}"
            )  # maybe instead of these, have client code making sense of
            # returned values including some error code
            sale = None
        elif quantity > len(sell_entry):  # O(len(sell_entry))
            print(
                f"Cannot fill quantity of sale: {quantity} shares of"
                f" {stock_symbol}. len(sell_entry) == {len(sell_entry)}"
            )
            sale = None
        return sale, sell_entry

    def buy(
        self, stock_symbol: str, shares_bought: int, cost_per_share: float
    ) -> None:  # required  # O(shares_bought)
        buy_entry = self.open_entry(stock_symbol)
        for share in range(shares_bought):
            buy_entry.add_purchase(StockPurchase(stock_symbol, cost_per_share))

    def buyRandom(
        self, stock_symbol: str, shares_bought: int, cost_per_share: float
    ) -> None:  # O(N) = O(N) * O(quantity)
        buy_entry = self.open_entry(stock_symbol)
        for s_i in range(shares_bought):  # O(shares_to_buy) * O(len(buy_entry))
            for s_j in range(
                SystemRandom().randint(0, len(buy_entry) - s_i)
            ):  # O(N)
                buy_entry.increment_entry()
            if SystemRandom().random() >= 0.5:
                buy_entry.add_purchase(
                    StockPurchase(stock_symbol, cost_per_share)
                )
            else:
                buy_entry.add_purchase_front(
                    StockPurchase(stock_symbol, cost_per_share)
                )

    def buyOptimal_1(
        self, stock_symbol: str, shares_bought: int, cost_per_share: float
    ) -> None:  # O(N)
        """buyOptimal_1 uses a method of LedgerEntry to position the data_portions such that addition places data in ascending order, then after use of an additional method of LedgerEntry that positions the deque such that the front is less than or equal to back, the deque is ascending order."""
        buy_entry = self.open_entry(stock_symbol)
        buy_entry.position_entry_add_between(cost_per_share)
        for share in range(shares_bought):
            buy_entry.add_purchase(
                StockPurchase(stock_symbol, cost_per_share)
            )  # COULD DO: centralize all add_purchase buys to a single buy
            # method
        buy_entry.align_head_tail()

    def buyOptimal_2(
        self, stock_symbol: str, shares_bought: int, cost_per_share: float
    ) -> None:  # O(N^2)
        """buyOptimal_2 uses a method of LedgerEntry to get the median data_portion, and adds lower cost shares to the front, and equal or greater cost shares to the back."""
        buy_entry = self.open_entry(stock_symbol)
        if len(buy_entry) == 0:
            for share in range(shares_bought):
                buy_entry.add_purchase(
                    StockPurchase(stock_symbol, cost_per_share)
                )
        else:
            if (
                cost_per_share >= buy_entry.median()
            ):  # idea: interesting design problem, chain together one or more
                # pairs of buy and sell methods (do by instance field assigned
                # None or object) but not all of them
                for share in range(shares_bought):
                    buy_entry.add_purchase(
                        StockPurchase(stock_symbol, cost_per_share)
                    )
            else:
                for share in range(shares_bought):
                    buy_entry.add_purchase_front(
                        StockPurchase(stock_symbol, cost_per_share)
                    )

    def buyOptimal_3(
        self, stock_symbol: str, shares_bought: int, cost_per_share: float
    ) -> None:  # O(1) = O(shares bought)
        """buyOptimal_3 makes an O(1) comparison to the back of the deque, adding to the front if the cost_per_share is less than the back cost."""
        buy_entry = self.open_entry(stock_symbol)
        if len(buy_entry) == 0:
            for share in range(shares_bought):
                buy_entry.add_purchase(
                    StockPurchase(stock_symbol, cost_per_share)
                )
        else:
            if cost_per_share >= buy_entry.peek_back().cost:
                for share in range(shares_bought):
                    buy_entry.add_purchase(
                        StockPurchase(stock_symbol, cost_per_share)
                    )
            else:
                for share in range(shares_bought):
                    buy_entry.add_purchase_front(
                        StockPurchase(stock_symbol, cost_per_share)
                    )

    def sell(
        self, stock_symbol: str, quantity: int, price: float
    ) -> StockSale:  # required  # O(1) = O(1) * O(quantity)
        """sell uses remove_purchase() to get a StockPurchase"""
        sale, sell_entry = self.open_sale(stock_symbol, quantity, price)
        if sale is not None:
            for s_i in range(quantity):  # O(quantity)
                sale.add_sale(sell_entry.remove_purchase())  # O(1)
        return sale

    def sellRandom(
        self, stock_symbol: str, quantity: int, price: float
    ) -> StockSale:  # O(N)
        """sellRandom increments the LedgerEntry"""
        sale, sell_entry = self.open_sale(stock_symbol, quantity, price)
        if sale is not None:
            # O(N)
            sell_entry_length = len(sell_entry)  # O(N)
            for s_i in range(quantity):  # O(quantity)
                for s_j in range(
                    SystemRandom().randrange(1, sell_entry_length * 2)
                ):  # O(N) = O(2N)
                    sell_entry.increment_entry()
                sale.add_sale(
                    sell_entry.remove_purchase()
                )  # removes from front  # O(1)
        return sale

    def sellOptimal_1(
        self, stock_symbol: str, quantity: int, price: float
    ) -> None:  # O(N)
        """sellOptimal_1 sells the lowest cost shares first"""
        sale, sell_entry = self.open_sale(stock_symbol, quantity, price)
        while not sale.is_filled():  # O(N) = O(N) * quantity  # fill the sale
            if sale.quantity - len(sale) == self.number_of_shares(
                stock_symbol
            ):  # O(N)
                for s_i in range(sale.quantity - len(sale)):
                    sale.add_sale(sell_entry.remove_purchase())
                    # if the currently required quantity is equal to the number
                    # of shares, all must be sold
            else:
                lowest_cost_share = (
                    sell_entry.peek()
                )  # O(1), gets a StockPurchase, in this case
                index_from_front = 0  # this value will be overwritten at some
                # point, unless the code below cannot run  ### used to decide
                # which direction to go
                entry_length = len(sell_entry)
                # locate a lowest cost share  ### alternative: position deque
                # such that front is less than sale price (but this method
                # doesn't know the price)
                for so_i in range(
                    entry_length
                ):  # O(len(sell_entry)) setup, O(N)
                    sell_entry.increment_entry()
                    if sell_entry.peek() < lowest_cost_share:
                        lowest_cost_share = sell_entry.peek()
                        index_from_front = so_i  # switching the order of these
                        # causes indefinite while loop
                # position the Deque according to index_from_front
                if (
                    index_from_front + 1
                    <= len(sell_entry) - index_from_front - 1
                ):
                    for so_j in range(
                        index_from_front + 1
                    ):  # O(N) = O(N/2) = O(index_from_front)
                        sell_entry.increment_entry()
                else:
                    for so_k in range(
                        len(sell_entry) - index_from_front - 1
                    ):  # O(N) = O(N/2)
                        sell_entry.decrement_entry()
                # add sales of current lowest cost
                while (
                    not sale.is_filled()
                    and sell_entry.peek().cost == lowest_cost_share.cost
                ):
                    sale.add_sale(sell_entry.remove_purchase())
        return sale

    def sellOptimal_2(
        self, stock_symbol: str, quantity: int, price: float
    ) -> None:  # O(N)
        """sellOptimal_2 sells any shares up to the "median" cost (per iteration, calculated as (maximum - minimum) / 2 + minimum)"""
        sale, sell_entry = self.open_sale(
            stock_symbol, quantity, price
        )  # number of shares >= quantity
        if sale is not None:
            while (
                not sale.is_filled()
            ):  # this loop will not run indefinitely
                # (number of shares >= quantity)
                current_median = sell_entry.median_2()  # O(N)
                for t_j in range(
                    len(sell_entry)
                ):  # must visit up to each data_portion
                    if sale.is_filled():  # order is filled
                        break
                    if (
                        sell_entry.peek().cost <= current_median
                    ):  # examine a purchase
                        sale.add_sale(
                            sell_entry.remove_purchase()
                        )  # add to sale, remove from front
                    else:
                        sell_entry.increment_entry()  # or add to back of deque
        return sale

    def sellOptimal_3(
        self, stock_symbol: str, quantity: int, price: float
    ) -> None:  # O(1)
        """sellOptimal_3 sells the lower cost share from the front or back"""
        sale, sell_entry = self.open_sale(
            stock_symbol, quantity, price
        )  # number of shares >= quantity
        if sale is not None:
            while (
                not sale.is_filled()
            ):  # this loop will not run indefinitely
                # (number of shares >= quantity)
                if (
                    sell_entry.peek() > sell_entry.peek_back()
                ):  # StockPurchase has __lt__ method
                    sell_entry.decrement_entry()
                sale.add_sale(sell_entry.remove_purchase())
        return sale

    def display_ledger(self) -> None:  # required  # O(number of shares)
        print("----  Stock Ledger  ----")
        for each_entry in self:  # calls iter which calls .__getitem__(index)
            each_entry.display_entry()

    def display_total_shares(self) -> None:
        print(self)

    def contains(
        self, stock_symbol: str
    ) -> bool:  # required  # O(number of entries)
        for each_entry in self.ledger_entries:
            if each_entry.symbol == stock_symbol:
                return True
        return False

    def get_entry(
        self, stock_symbol: str
    ) -> LedgerEntry:  # required  # O(number of entries)
        for each_entry in self.ledger_entries:
            if each_entry.symbol == stock_symbol:
                return each_entry
        return None

    def number_of_shares(self, stock_symbol: str) -> None | int:  # O(N)
        num_shares = 0
        if self.contains(stock_symbol):
            num_shares = len(
                self.get_entry(stock_symbol)
            )  # returns None for non-present stock_symbols
        return num_shares  # same behavior for stock symbols not found in ledger
    # and for those of empty ledger entries
