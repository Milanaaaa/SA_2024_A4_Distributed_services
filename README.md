# Twitter 2.0

## ⬇️ Download 
```shell
git clone https://github.com/Milanaaaa/SA_2024_A4_Distributed_services
```

## 🚀 Run

### Server
1. Rename `.env.example` to `.env` and update this file if necessary
    ```shell
    mv .env.example .env
    ```
2. Run application using [docker](https://www.docker.com/)
    ```shell
    docker compose up
    ```

### Client
1. Go to `client`
    ```shell
    cd client
    ```
2. Update `config.ini` if necessary
3. Install requirements
    ```shell
    pip install -r requirements.txt
    ```
4. Run client 
    ```shell
    python client.py
    ```