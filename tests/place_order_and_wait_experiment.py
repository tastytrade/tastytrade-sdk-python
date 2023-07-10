import logging

from tastytrade_sdk import Order, Leg
from tests.utils import get_tasty


def main():
    logging.basicConfig(level=logging.DEBUG)
    tasty = get_tasty()
    print(tasty.orders.place_order_and_wait(
        account_number='5WT06363',
        timeout_seconds=5,
        order=Order(
            order_type='Market',
            time_in_force='Day',
            legs=[
                Leg(
                    instrument_type='Equity',
                    symbol='DOCU',
                    action='Buy to Open',
                    quantity=0.15
                )
            ]
        )
    ))


if __name__ == '__main__':
    main()
