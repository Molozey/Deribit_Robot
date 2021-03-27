import unittest
import Python_Trade_Bot


class MyTestCase(unittest.TestCase):

    def test_json_access_token(self):
        """Правильное определение access_token"""
        test_string = '{"jsonrpc":"2.0","id":9929,"result":{"token_type":"bearer","scope":"account:read_write block_trade:read_write custody:read_write expires:60000 mainaccount session:testnet, trade:read_write wallet:read_write","refresh_token":"1617424727145.1JHKf7ty.A0G8Ukt7OAg8hQ13L4F7D1IkGw1JNyNLjwO22agC2D3JYn3TNFyRDoH7vMEcqghbZ1R_kmDWsLY8f8FNG52UWL4gjre_e9XY9gmMBRhTpMPsuA2-82QfOrPEORoNwFprMK_P3LQQclYf2NWPzjmhFji8pE3WgH2uHlo1-71i0drmcASTkuUYJn3RcX6a-UGQ4bA2WRF_gho7Z2vhmw-4Bvhl4YLhyuoc4md5q0YNWmh06SZrA2SJKWwX4IbkK4sQP9EwITbxSduThx83ZpHRj9jl-wtzIqBH0di9mMDV8TKqE7VUSNqs9A5OQX2XVaX07QypeDLhEuOFhknuQMx9bw","expires_in":59999,"access_token":"1616879927145.1DNwGFp6.JhVRXpB1gIc0hYhLWBoreCiCL32FtZs9BBsXtaytfCCrDpdM_yS20V9g39271AhkL9R63NRs9ldIki0LOfxJY396-NSy9fL7LRfyMBpsBAQbBkuHqh8K1EMLpQSGMXlp1EOsbPeE6zrovPHXYMCPYll2c0iKpa8dGEH40Ethi3DMisZigYInUo_i7_JbpA_GM1ClNemrxClgN4IrtBG14VdsLxl0mOe5iI0kwmSzNRlQULfX5bXBEZDlxJqfip6Pi8rdDqilYMoKRVshs67sRFsAsfl3JOhfcjgfTEMaKRPBSFCOqXlwLaixXZjAgZlRH0M43whPf8lx74NmOvCqbfs"},"usIn":1616819927145557,"usOut":1616819927146288,"usDiff":731,"testnet":true'
        answer = Python_Trade_Bot.get_value_from_json(test_string, 'access_token')
        self.assertEqual("1616879927145.1DNwGFp6.JhVRXpB1gIc0hYhLWBoreCiCL32FtZs9BBsXtaytfCCrDpdM_yS20V9g39271AhkL9R63NRs9ldIki0LOfxJY396-NSy9fL7LRfyMBpsBAQbBkuHqh8K1EMLpQSGMXlp1EOsbPeE6zrovPHXYMCPYll2c0iKpa8dGEH40Ethi3DMisZigYInUo_i7_JbpA_GM1ClNemrxClgN4IrtBG14VdsLxl0mOe5iI0kwmSzNRlQULfX5bXBEZDlxJqfip6Pi8rdDqilYMoKRVshs67sRFsAsfl3JOhfcjgfTEMaKRPBSFCOqXlwLaixXZjAgZlRH0M43whPf8lx74NmOvCqbfs", answer)

    def test_json_order_id(self):
        """Корректное определение id ордера"""
        test_string = '{"jsonrpc":"2.0","id":5275,"result":{"trades":[],"order":{"web":false,"time_in_force":"good_til_cancelled","replaced":false,"reduce_only":false,"profit_loss":0.0,"price":54379.0,"post_only":false,"order_type":"limit","order_state":"open","order_id":"5522795550","max_show":100.0,"last_update_timestamp":1616823207098,"label":"market0000234","is_liquidation":false,"instrument_name":"BTC-PERPETUAL","filled_amount":0.0,"direction":"buy","creation_timestamp":1616823207098,"commission":0.0,"average_price":0.0,"api":true,"amount":100.0}},"usIn":1616823207096723,"usOut":1616823207099112,"usDiff":2389,"testnet":true}'
        answer = Python_Trade_Bot.get_value_from_json(test_string, 'order_id')
        self.assertEqual("5522795550", answer)

    def test_json_market_price(self):
        test_string ='{"jsonrpc":"2.0","id":8772,"result":{"timestamp":1616823546526,"stats":{"volume_usd":102739010.0,"volume":1942.7546511,"price_change":3.1429,"low":50473.0,"high":55060.0},"state":"open","settlement_price":53613.07,"open_interest":3406513330,"min_price":53614.58,"max_price":55247.51,"mark_price":54433.83,"last_price":54379.5,"instrument_name":"BTC-PERPETUAL","index_price":54992.06,"funding_8h":-0.00402411,"estimated_delivery_price":54992.06,"current_funding":-0.005,"change_id":5522812526,"bids":[[54379.0,95720.0],[54378.5,20.0],[54378.0,20.0],[54377.5,20.0],[54377.0,20.0]],"best_bid_price":54379.0,"best_bid_amount":95720.0,"best_ask_price":54379.5,"best_ask_amount":5430.0,"asks":[[54379.5,5430.0],[54390.0,10.0],[54468.0,5450.0],[54816.5,56270.0],[54922.0,6400.0]]},"usIn":1616823547058540,"usOut":1616823547058891,"usDiff":351,"testnet":true}'
        answer = Python_Trade_Bot.get_value_from_json(test_string, 'mark_price')
        self.assertEqual(54433.83, float(answer))

    def test_json_order_status(self):
        test_string = '{"jsonrpc":"2.0","id":4316,"result":{"web":false,"time_in_force":"good_til_cancelled","replaced":false,"reduce_only":false,"profit_loss":0.0,"price":54379.5,"post_only":false,"order_type":"limit","order_state":"open","order_id":"5522826459","max_show":100.0,"last_update_timestamp":1616823816111,"label":"market0000234","is_liquidation":false,"instrument_name":"BTC-PERPETUAL","filled_amount":0.0,"direction":"buy","creation_timestamp":1616823816111,"commission":0.0,"average_price":0.0,"api":true,"amount":100.0},"usIn":1616823816459040,"usOut":1616823816459757,"usDiff":717,"testnet":true}'
        answer = Python_Trade_Bot.get_value_from_json(test_string, 'order_state')
        self.assertEqual("open", answer)

    def test_filled_status(self):
        test_string = '{"jsonrpc":"2.0","id":4316,"result":{"web":false,"time_in_force":"good_til_cancelled","replaced":false,"reduce_only":false,"profit_loss":0.0,"price":54379.5,"post_only":false,"order_type":"limit","order_state":"open","order_id":"5522826459","max_show":100.0,"last_update_timestamp":1616823816111,"label":"market0000234","is_liquidation":false,"instrument_name":"BTC-PERPETUAL","filled_amount":0.0,"direction":"buy","creation_timestamp":1616823816111,"commission":0.0,"average_price":0.0,"api":true,"amount":100.0},"usIn":1616823816459040,"usOut":1616823816459757,"usDiff":717,"testnet":true}'
        answer = Python_Trade_Bot.get_value_from_json(test_string, 'filled_amount')
        self.assertEqual(0.0, float(answer))

    def test_filled_status_not_null(self):
        test_string = '{"jsonrpc":"2.0","id":4316,"result":{"web":false,"time_in_force":"good_til_cancelled","replaced":false,"reduce_only":false,"profit_loss":0.0,"price":54379.5,"post_only":false,"order_type":"limit","order_state":"open","order_id":"5522826459","max_show":100.0,"last_update_timestamp":1616823816111,"label":"market0000234","is_liquidation":false,"instrument_name":"BTC-PERPETUAL","filled_amount":168.0,"direction":"buy","creation_timestamp":1616823816111,"commission":0.0,"average_price":0.0,"api":true,"amount":100.0},"usIn":1616823816459040,"usOut":1616823816459757,"usDiff":717,"testnet":true}'
        answer = Python_Trade_Bot.get_value_from_json(test_string, 'filled_amount')
        self.assertEqual(168.0, float(answer))


if __name__ == '__main__':
    unittest.main()
