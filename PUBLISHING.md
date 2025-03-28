# Ansible Galaxyへの公開手順

このドキュメントでは、Ansible Bellコレクションを[Ansible Galaxy](https://galaxy.ansible.com/)に公開する手順を説明します。

## 前提条件

1. [Ansible Galaxy](https://galaxy.ansible.com/)のアカウントを持っていること
2. Ansible Galaxyの[API Key](https://galaxy.ansible.com/me/preferences)を取得していること

## 公開手順

1. コレクションをビルドする

```bash
ansible-galaxy collection build ansible_collections/cahlchang/bell
```

2. コレクションを公開する

```bash
ansible-galaxy collection publish cahlchang-bell-1.0.0.tar.gz --api-key=<your-api-key>
```

`<your-api-key>`は、Ansible Galaxyの[API Key](https://galaxy.ansible.com/me/preferences)から取得したキーに置き換えてください。

## 公開後の確認

公開が完了したら、以下のコマンドでインストールできることを確認してください：

```bash
ansible-galaxy collection install cahlchang.bell
```

## 新しいバージョンの公開

1. `ansible_collections/cahlchang/bell/galaxy.yml`の`version`を更新する
2. 上記の手順でビルドと公開を行う

## トラブルシューティング

公開に失敗した場合は、以下を確認してください：

- API Keyが正しいか
- コレクション名が既に使用されていないか
- `galaxy.yml`の内容が正しいか（特にバージョン番号）