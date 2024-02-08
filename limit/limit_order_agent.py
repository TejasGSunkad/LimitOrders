from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class ExecutionAgent(ExecutionClient):
    def __init__(self):
        super().__init__()

    def buy(self, product_id: str, amount: int):
        print(f"\norder bought: product- {product_id} at the price {amount}.\n")


    def sell(self, product_id: str, amount: int):
        print(f"\norder sold : product- {product_id} at the price {amount}\n")


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.held_orders_list = []
        self.executed_orders_list = []

    def on_price_tick(self, product_id: str, price: float):


        '''
        ## 1 Implement LimitOrderAgent such that it buys 1000 shares of IBM when the price drops below $100

        ```if product_id == "IBM" and price < 100:
            for _ in range(1000):
                self.execution_client.buy(product_id, price)```

                '''

        # Note please comment the below code to test the buy 1000 share and then run the test case.

        ## Note comment above code to run the  and test 2nd part

        # Extend LimitOrderAgent such that it:
        #
        #     accepts orders through an add_order method, that accepts the following parameters
        #         a flag indicating whether to buy or sell
        #         a product id
        #         an amount to buy/sell
        #         the limit at which to buy or sell
        #     executes any held orders when the market price is at or better than the limit (you can set aside or comment out the changes made for part 1)

        if product_id == "IBM" and price <= 100:
            self.add_order("buy", "IBM", price, 99)

        elif product_id == "IBM" and price >= 200:
            self.add_order("sell", "IBM", price, 102)
        else:
            print(f"price not in the range of buy or sell. Details : product- {product_id} with the price {price}")
            return

        self.execute_held_orders(product_id, price)

    def add_order(self, order_type: str, product_id: str, amount: int, limit: int):
        order = {
            "type": order_type,
            "product_id": product_id,
            "amount": amount,
            "limit": limit
        }

        self.held_orders_list.append(order)


    def execute_held_orders(self, product_id: str, current_price: int):

        try:
            for held_order in self.held_orders_list:

                if held_order["product_id"] == product_id:
                    if  held_order["type"] == "buy":
                        if current_price <= held_order["limit"]:
                            self.execution_client.buy(held_order["product_id"], current_price)
                            self.executed_orders_list.append(held_order)

                    elif held_order["type"] == "sell":
                        if current_price >= held_order["limit"]:
                            self.execution_client.sell(held_order["product_id"], current_price)
                            self.executed_orders_list.append(held_order)


            self.held_orders_list = [order for order in self.held_orders_list if order not in self.executed_orders_list]

        except ExecutionClient.ExecutionException as e:
                print(f"Execution failed: {e}")



if __name__ == "__main__":
    execution_protocol = ExecutionAgent()
    obj1 = LimitOrderAgent(execution_protocol)
    obj1.on_price_tick('IBM',90)
    obj1.on_price_tick('IBM',300)
    obj1.on_price_tick('IBM',140)