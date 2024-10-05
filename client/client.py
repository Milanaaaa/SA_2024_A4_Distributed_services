import configparser
from requests import Session


class UsersAPI:
    ...


class PostsAPI:
    ...


class FeedsAPI:
    ...


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    ...


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] Exited')
    except ConnectionError:
        print('[!] Connection error')
    except Exception as e:
        print(f'[!] Unknown error: {e}')
