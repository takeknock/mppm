# mppm
Implementations in this repository are based on mypa introduced in [エムスリーテックブック5](https://techbookfest.org/product/rpXewXTtekXgNPFBCWLrX4?productVariantID=nrAyYa0LsLwUZUk5Qee80X).

# 機能一覧

- [x] mppm runコマンドのone way実装
- [x] mppm buildコマンドのone way実装
- [x] mppm publishコマンドのone way実装
- [x] mppm lockコマンドのone way実装
- [x] mppm installコマンドのone way実装
- [ ] mppm runコマンドでpython --versionが実行できる
- [ ] mppm lockコマンドで環境に存在しないPythonの環境を作成できる
- [ ] poetry add --devのような開発時のみ利用するパッケージを追加できる
- [ ] marker付パッケージのインストールを可能にする
- [ ] 自身をビルドできるように修正する


# テストケース

- [x] mppm lockコマンドでローカルに存在しないPythonの環境を作成するテストケースの追加
- [ ] mppm runコマンドでpython --versionを実行するテストケースの追加

# 環境面

- [x] pytestの導入
- [x] mypyの導入
- [ ] github actionsの導入
- [ ] dependabotの導入

# その他
- [x] テストのため任意の場所のpyproject.tomlを読み込めるよう、PyProjectTomlクラスを修正


# issues
## testの追加

## formatter、linterの追加

