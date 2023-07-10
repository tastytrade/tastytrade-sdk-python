from tastytrade_sdk import Order, Leg
from tests.utils import get_tasty


def main():
    tasty = get_tasty()
    print(tasty.orders.place_order_and_wait(
        account_number='5WT06363',
        timeout_seconds=5,
        order=Order(
            order_type='Limit',
            time_in_force='Day',
            price=1.5,
            price_effect='Debit',
            legs=[
                Leg(
                    instrument_type='Equity',
                    symbol='DOCU',
                    action='Buy to Open',
                    quantity=1
                )
            ]
        )
    ))


if __name__ == '__main__':
    main()
