import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent
from limit.limit_order_agent import ExecutionAgent

class LimitOrderAgentTest(unittest.TestCase):

    # def test_positive_buy_1000_share(self):
    #     execution_client = ExecutionAgent()
    #     execution_client.buy = MagicMock()
    #
    #     limit_order_agent = LimitOrderAgent(execution_client)
    #
    #     # Trigger a buy order
    #     limit_order_agent.on_price_tick("IBM", 99)
    #     self.assertEqual(execution_client.buy.call_count, 1000)
    #

    # def test_negative_buy_1000_share(self):
    #     execution_client = ExecutionAgent()
    #     execution_client.buy = MagicMock()
    #
    #     limit_order_agent = LimitOrderAgent(execution_client)
    #
    #     # Trigger a buy order
    #     limit_order_agent.on_price_tick("IBM", 100)
    #     self.assertEqual(execution_client.buy.call_count, 0)


    def test_to_buy_price(self):
        execution_client = ExecutionAgent()
        execution_client.buy = MagicMock()

        limit_order_agent = LimitOrderAgent(execution_client)
        limit_order_agent.on_price_tick("IBM", 99)

        execution_client.buy.assert_called_once_with("IBM", 99)

    def test_to_sell_price(self):
        execution_client = ExecutionAgent()
        execution_client.sell = MagicMock()
        execution_client.buy = MagicMock()

        limit_order_agent = LimitOrderAgent(execution_client)
        limit_order_agent.on_price_tick("IBM", 99)
        execution_client.buy.assert_called_once_with("IBM", 99)

        limit_order_agent.on_price_tick('IBM',200)

        execution_client.sell.assert_called_once_with("IBM", 200)


    def test_sell_not_excicute(self):
        execution_client = ExecutionAgent()
        execution_client.sell = MagicMock()
        execution_client.buy = MagicMock()

        limit_order_agent = LimitOrderAgent(execution_client)
        limit_order_agent.on_price_tick("IBM", 90)
        execution_client.buy.assert_called_once_with("IBM", 90)

        limit_order_agent.on_price_tick('IBM',150)

        execution_client.sell.assert_not_called()


    def test_sell_excicute_at_high_price(self):
        execution_client = ExecutionAgent()
        execution_client.sell = MagicMock()
        execution_client.buy = MagicMock()

        limit_order_agent = LimitOrderAgent(execution_client)
        limit_order_agent.on_price_tick("IBM", 90)
        execution_client.buy.assert_called_once_with("IBM", 90)

        limit_order_agent.on_price_tick('IBM',230)

        execution_client.sell.assert_called_once_with("IBM", 230)


if __name__ == "__main__":
    unittest.main()