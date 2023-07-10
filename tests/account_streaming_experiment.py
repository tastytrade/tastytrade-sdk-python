from tests.utils import get_tasty


def main():
    tasty = get_tasty()
    streamer = tasty.accounts.get_streamer(account_numbers=['5WX82645'])

    streamer.start(on_message=print)


if __name__ == '__main__':
    main()
