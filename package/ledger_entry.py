from package.linked_deque import LinkedDeque
from package.stock_purchase import StockPurchase


class LedgerEntry:
    def __init__(self, stock_symbol: str) -> None:  # required
        self._linked_deque = LinkedDeque()
        self.symbol = stock_symbol

    def __len__(self) -> int:  # O(N)
        return len(self._linked_deque)

    def add_purchase(
        self, new_purchase: StockPurchase
    ) -> None:  # required  # O(1)
        # add to the back
        if new_purchase.symbol == self.symbol:
            self._linked_deque.add_to_back(new_purchase)

    def add_purchase_front(self, new_purchase: StockPurchase) -> None:  # O(1)
        if (
            new_purchase.symbol == self.symbol
        ):  # this is twice as many primitive operations per call of this method
            # than without validation
            self._linked_deque.add_to_front(new_purchase)

    def peek(self) -> StockPurchase:  # O(1)
        return self._linked_deque.get_front()

    def peek_back(self) -> StockPurchase:  # O(1)
        return self._linked_deque.get_back()

    def increment_entry(self) -> None:  # O(1)
        self._linked_deque.front_to_back()

    def decrement_entry(self) -> None:  # O(1)
        self._linked_deque.back_to_front()

    def remove_purchase(self) -> StockPurchase:  # required  # O(1)
        # remove from the front
        return (
            self._linked_deque.remove_front()
        )  # .get_data_portion()  # DLNode is designed as a private inner class
    # of LedgerEntry, so this doesn't return DLNode objects, instead it returns
    # their data portion

    def __eq__(self, other) -> bool:  # O(N) = O(N) + O(N) + ... + O(N)
        equal_bool = False  # where N is the left operand of __eq__()
        if isinstance(other, self.__class__):
            equal_bool = self._linked_deque == other._linked_deque
        return equal_bool

    def equals(self, other) -> bool:  # required  # O(N^2)
        return self.symbol == other.symbol and len(self._linked_deque) == len(
            other._linked_deque
        )  # same symbol, same length: equal

    def display_entry(self) -> None:  # required
        if self._linked_deque.is_empty():
            print(f"{self.symbol}: None")
        else:
            price_list = []
            quantity_list = []
            # price_quantity_dict = dict()
            front_ledger_item = self._linked_deque.remove_front()
            self._linked_deque.add_to_back(front_ledger_item)
            price_list.append(front_ledger_item.cost)
            quantity_list.append(1)
            # price_quantity_dict.update({front_ledger_item: 1})
            current_ledger_item = self._linked_deque.remove_front()
            self._linked_deque.add_to_back(current_ledger_item)
            while current_ledger_item is not front_ledger_item:
                if current_ledger_item.cost not in price_list:
                    price_list.append(current_ledger_item.cost)
                    quantity_list.append(1)
                else:
                    quantity_list[
                        price_list.index(current_ledger_item.cost)
                    ] += 1
                current_ledger_item = self._linked_deque.remove_front()
                self._linked_deque.add_to_back(current_ledger_item)
            ledger_string = ""
            for each_price, each_quantity in zip(price_list, quantity_list):
                # ledger_string += str(f" {each_price:.1f} ({each_quantity} shares)")
                ledger_string += (
                    str(each_price) + " (" + str(each_quantity) + " shares)   "
                )
            print(self.symbol + ": " + ledger_string)

    def position_entry_add_between(self, cost_per_share: float) -> None:  # O(N)
        # positions entry such that addition of shares to back of queue keeps
        # queue in sorted order (ascending)  ### assumes that the queue is in
        # sorted (ascending) order
        for b_i in range(len(self)):
            if (cost_per_share <= self._linked_deque.get_front().cost) and (
                cost_per_share >= self._linked_deque.get_back().cost
            ):
                break  # positioned for adding to back -> ascending order
            else:
                self.increment_entry()

    def align_head_tail(self) -> None:  # O(N)
        for a_i in range(len(self)):
            if (
                self._linked_deque.get_front().cost
                < self._linked_deque.get_back().cost
            ):
                break  # assuming the deque is in ascending order, the lowest
            # cost shares are at the front
            else:
                self.increment_entry()

    def median(self) -> float:  # O(N^2) = O(N) + O(N) * O(N)
        """median gets the actual
        modified from codestepbystep.com solution to median (Python): https://www.codestepbystep.com/r/problem/view/python/collections/list/median?problemsetid=7217
        """
        ledger_length = len(self)  # O(N)
        median = None
        # deque position i
        for m_i in range(ledger_length):  # O(N) outer
            num_greater = 0
            num_lesser = 0
            num_equal = 0
            if not m_i == 0:
                self.increment_entry()  # increment entry to data portion to
                # check for median
            # deque position j
            current_cost = self.peek().cost
            if median is None:
                current_cost = self.peek().cost
                for m_j in range(
                    ledger_length
                ):  # O(N) inner  # count each incremented front value
                    if (
                        self.peek().cost > current_cost
                    ):  # using count_ methods of LinkedDeque, this would go
                        # through the deque 3 times
                        num_greater += 1
                    elif self.peek().cost < current_cost:
                        num_lesser += 1
                    else:
                        num_equal += 1
                if (
                    abs(num_lesser - num_greater) <= num_equal
                ):  # condition from codestepbystep solution  ### for 1 node,
                    # 0 - 0 <= 1
                    median = current_cost  #    # if the data were sorted then
                    # the current_cost would be the median
            # position j
            # loop ends with position j = position i + (length - 1)
        self.increment_entry()  # runs in the case when length is 1, but this
        # doesn't change the order
        # deque position i
        return median if median is not None else 0  #

    def median_2(self) -> float:  # O(N)
        """median_2 gets the maximum and minimum, and calculates a "median" (which may not be present in share costs) as (maximum - minimum) / 2 + minimum."""
        maximum = self.peek().cost
        minimum = self.peek().cost
        for m_i in range(len(self)):
            self.increment_entry()
            maximum = max(maximum, self.peek().cost)
            minimum = min(minimum, self.peek().cost)
        return (maximum - minimum) / 2 + minimum
