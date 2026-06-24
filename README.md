# django-docker

授業でDjangoを触るための開発環境

## Get Started

### Dev Container

1. 任意のDocker Deamonを起動しておく
2. 任意のエディタでこのリポジトリを開く
3. Reopen in Containerを実行
4. コンテナ内のターミナルで以下を実行する:
```bash
uv run python manage.py migrate
uv run python manage.py runserver 0.0.0.0:8000
```

Dev Containerがうまくいかなかったらこれでもいける:

```bash
cd .devcontainer
docker compose build
docker compose up -d
docker compose exec web bash
```

5. ブラウザで`http://127.0.0.1:8000`を開く

## 指定環境との差分

- パッケージ管理をpyproject.tomlとuvでやる
- DBは特に指定がなさそうなので、PostgresSQLを採用した
