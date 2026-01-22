## Deque Buy and Sell Methods in `TradingBot`s controlled by strings

Alan MH Beem

Refactor due: $01/21/2026$

|**Contents of README**|
|-|
|-|
|Description|
|Refactors|
|Profit for buy methods x sell methods|
|UML Class Diagram|
|Re. Obfuscation|

---

### **Description**

This is a project examining the deque data structure, and writing algorithms on it. The TradingBot class contains buy and sell behaviors that utilize deque operations, and when applied in a Cartesian product of buy methods x sell methods, over a sequence of trades (the same for each TradingBot), result in a spread of profit and wall time, both of which are described in [main.ipynb](https://github.com/AlanBeem/AD325_Project1/blob/main/main.ipynb) [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/AlanBeem/AD325_Project1/blob/main/main.ipynb).

---

### **Refactors**

### $decorator$

#### before

```python
...

class TradingBot:

    ...

    def buy(self, stock_symbol: str, quantity: int, price: float) -> None:  # O(f(N))
        buy_time_start = time.time()
        if self.buy_setting == 1:                                           # O(1)
            self.stock_ledger.buy(stock_symbol, quantity, price)
        elif self.buy_setting == 2:                                         # O(N)
            self.stock_ledger.buyRandom(stock_symbol, quantity, price)
        elif self.buy_setting == 3:                                         # O(N)
            self.stock_ledger.buyOptimal_1(stock_symbol, quantity, price)
        elif self.buy_setting == 4:                                         # O(N^2)
            self.stock_ledger.buyOptimal_2(stock_symbol, quantity, price)
        elif self.buy_setting == 5:                                         # O(1)
            self.stock_ledger.buyOptimal_3(stock_symbol, quantity, price)
        buy_time_end = time.time()
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)
        self.buy_time += buy_time_end - buy_time_start
    
    def sell(self, stock_symbol: str, quantity: int, price: float) -> None:  #                            # O(f(N))
        sell_time_start = time.time()
        if self.sell_setting == 1:                                                                        # O(1)
            self.stock_sales_list.append(self.stock_ledger.sell(stock_symbol, quantity, price))
        elif self.sell_setting == 2:                                                                      # O(N)
            self.stock_sales_list.append(self.stock_ledger.sellRandom(stock_symbol, quantity, price))
        elif self.sell_setting == 3:                                                                      # O(N)
            self.stock_sales_list.append(self.stock_ledger.sellOptimal_1(stock_symbol, quantity, price))
        elif self.sell_setting == 4:                                                                      # O(N^2)
            self.stock_sales_list.append(self.stock_ledger.sellOptimal_2(stock_symbol, quantity, price))
        elif self.sell_setting == 5:                                                                      # O(1)
            self.stock_sales_list.append(self.stock_ledger.sellOptimal_3(stock_symbol, quantity, price))
        if self.stock_sales_list[-1] is None:
            self.stock_sales_list.remove(None)
        else:
            sell_time_end = time.time()
            self.balance += quantity * price
            self.profit_per_sell.append(self.last_profit())
            self.sell_time += sell_time_end - sell_time_start

    ...
```

#### after

```python
...

def timing(func):
    def wrapper(*args):
        start = time.time()
        ret = func(*args)
        return time.time() - start

    return wrapper


class TradingBot:

    ...

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
        self.balance -= quantity * price
        self.balance_over_transactions.append(self.balance)

    def buy(self, stock_symbol: str, quantity: int, price: float) -> None:  # O(f(N))
        self.buy_time += self._match_buy(stock_symbol, quantity, price)

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
        if self.stock_sales_list[-1] is None:
            self.stock_sales_list.remove(None)
        else:
            self.balance += quantity * price
            self.profit_per_sell.append(self.last_profit())

    def sell(
        self, stock_symbol: str, quantity: int, price: float
    ) -> None:  #                            # O(f(N))
        self.sell_time += self._match_sell(stock_symbol, quantity, price)

    ...
```


### $lambdas$ 1, 2

#### before

```python
...

tb = TradingBot(0, 1, 1)
buy_methods_testing_additions(tb)
tb.stock_ledger.ledger_entries[0]._linked_deque.display()

...

tb = TradingBot(0, 2, 1)  # using buyRandom
buy_methods_testing_additions(tb)
tb.stock_ledger.ledger_entries[0]._linked_deque.display()
sell_methods_testing_removals(tb)

...
```

#### after

```python
...

bot_buy = lambda x, y, z: [
    tb := TradingBot(x, y, z),
    buy_methods_testing_additions(tb),
    tb.stock_ledger.ledger_entries[0]._linked_deque.display(),
][0]

...

sell_bot = lambda x, y, z: [
    tb := TradingBot(x, y, z),
    buy_methods_testing_additions(tb),
    tb.stock_ledger.ledger_entries[0]._linked_deque.display(),
    sell_methods_testing_removals(tb),
][0]

...

tb = bot_buy(0, 1, 1)

...

tb = sell_bot(0, 2, 4)  # using buyRandom

...
```

### $lambda$ 3

#### before
```python
...

average_performance_matrix = [
    [0 for n in sell_row] for m in buy_column
]
average_elapsed_time_matrix = [
    [0 for n in sell_row] for m in buy_column
]
total_elapsed_time_matrix = [
    [0 for n in sell_row] for m in buy_column
]
total_buy_time_matrix = [
    [0 for n in sell_row] for m in buy_column
]
total_sell_time_matrix = [
    [0 for n in sell_row] for m in buy_column
]

...
```

#### after
```python
...

get_performance_matrix = lambda: [
    [0 for n in sell_row] for m in buy_column
]

...

average_performance_matrix = get_performance_matrix()
average_elapsed_time_matrix = get_performance_matrix()
total_elapsed_time_matrix = get_performance_matrix()
total_buy_time_matrix = get_performance_matrix()
total_sell_time_matrix = get_performance_matrix()

...
```

### $lambdas$ 4, 5, 6, 7, 8, 9

**before**

```python
...

print(f"Profit divided by revenue for each combination, averaged over {num_iterations} iterations\n")
print(''.join([each_s.ljust(15).rjust(20) for each_s in ([''] + sell_row)]))
maximum = 0
for i in range(5):
    print()
    current_row = buy_column[i].ljust(15).rjust(20)
    for j in range(5):
        maximum = max(maximum, average_performance_matrix[i][j])
        current_row += f"{average_performance_matrix[i][j]:.3f}".ljust(15).rjust(20)
    print(current_row)
print()
print(f"Maximum average ratio of profit to revenue: {maximum : .3f}")

...
```

**after**

```python
...

just_entry = lambda entry: entry.ljust(15).rjust(20)
get_sell_headers = lambda sell_row: "".join(
    [just_entry(each_s) for each_s in ([""] + sell_row)]
)
get_a_row = lambda label, row, div: just_entry(label) + "".join(
    just_entry(f"{row[j] / div:.4f}") for j in range(len(row))
)
get_rows = lambda row_labels, matrix, normalization_value: [
    get_a_row(row_labels[i], matrix[i], normalization_value)
    for i in range(len(matrix))
]
print_matrix_report = lambda title, column_labels, row_labels, matrix, normalization_value=1: \
    print(
    "\n\n".join(
        [
            title,
            get_sell_headers(column_labels),
            *get_rows(row_labels, matrix, normalization_value),
        ]
    )
)

...

print_matrix_report(
    "Profit divided by revenue for each combination, averaged over"
    + f" {num_iterations} iterations\n",
    sell_row,
    buy_column,
    average_performance_matrix,
)
print(
    f"Maximum average ratio of profit to revenue: {max(map(max, average_performance_matrix)) : .3f}"
)

...
```

---

### **Profit for buy methods x sell methods**

![](https://github.com/AlanBeem/AD325_Project1/blob/main/figures/a_profit_result_buyxsell.png)

---

### **UML Class Diagram**

![](https://github.com/AlanBeem/AD325_Project1/blob/main/diagrams/Beem_Project1_Class_Diagram_Final_10_21_2024.png)

---

### **Regarding Obfuscation**

This repository is based on a project for a class that required the repository be private for grading- I don't know why, but I've made some efforts to respect that by compiling code for modules outside the refactor for the present project.


