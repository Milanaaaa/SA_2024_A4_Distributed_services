import configparser
from typing import Any
from json import JSONDecodeError

from requests import Session, HTTPError


class UsersAPI:
    def __init__(self, base_url: str):
        self.http = Session()
        self.base_url = base_url

    def register(self, username: str) -> None:
        self.http.post(
            self.base_url + '/register',
            json={'username': username}
        ).raise_for_status()


class PostsAPI:
    def __init__(self, base_url: str):
        self.http = Session()
        self.base_url = base_url

    def send_post(self, username: str, content: str) -> dict[str: Any]:
        r = self.http.post(
            self.base_url + '/posts',
            json={
                'username': username,
                'content': content
            }
        )

        r.raise_for_status()

        return r.json()

    def like_post(self, username: str, post_id: int) -> None:
        self.http.post(
            self.base_url + f'/posts/{post_id}/like',
            json={'username': username}
        ).raise_for_status()


class FeedsAPI:
    def __init__(self, base_url: str):
        self.http = Session()
        self.base_url = base_url

    def get_feed(self) -> dict[str: Any]:
        r = self.http.get(self.base_url + '/feed')

        r.raise_for_status()

        return r.json()


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    username = None

    users_api = UsersAPI(config['servers']['UsersBaseURL'])
    posts_api = PostsAPI(config['servers']['PostsBaseURL'])
    feeds_api = FeedsAPI(config['servers']['FeedsBaseURL'])

    print('Enter one of this commands:')
    print(' /auth [username]')
    print(' /register [username]')
    print(' /feed')
    print(' /post [content]')
    print(' /like [post_id]')
    print()

    while True:
        tokens = input('> ').split()

        try:
            if tokens[0] == '/auth' and len(tokens) == 2:
                username = tokens[1]
            elif tokens[0] == '/register' and len(tokens) == 2:
                users_api.register(tokens[1])
                username = tokens[1]
            elif tokens[0] == '/feed' and len(tokens) == 1:
                for post in feeds_api.get_feed()['posts']:
                    print(f" #{post['id']} [{post['username']}] {post['content']}")

                    if post['liked_by']:
                        print(' Liked by:', ', '.join(post['liked_by']))
            elif tokens[0] == '/post' and len(tokens) >= 2:
                if not username:
                    print(' [!] You didn\'t authorized')
                    continue

                posts_api.send_post(username, ' '.join(tokens[1:]))
            elif tokens[0] == '/like' and len(tokens) == 2:
                if not username:
                    print(' [!] You didn\'t authorized')
                    continue

                posts_api.like_post(username, int(tokens[1]))
            else:
                print(' [!] Unknown command')
        except HTTPError as err:
            try:
                print(' [!]', err.response.json().get('detail', 'unexpected error'))
            except JSONDecodeError:
                print(' [!]', err.response.text)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('[*] Exited')
    except ConnectionError:
        print('[!] Connection error')
    except Exception as e:
        print(f'[!] Unknown error: {e}')
