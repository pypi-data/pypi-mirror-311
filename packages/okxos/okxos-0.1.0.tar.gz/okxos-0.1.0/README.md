# okxos

`okxos` 是一个基于 OKX OS API 的 Python 异步客户端库，使用 `httpx` 实现 HTTP 请求封装，支持 Wallet API、DEX API、Marketplace API 和 DeFi API 的功能，旨在为开发者提供简便快捷的 Web3 应用开发解决方案。

## 功能特性

- **Wallet API**: 支持链查询、实时币价、代币转账等功能。
- **DEX API**: 支持链信息查询、交易聚合等功能。
- **Marketplace API**: 提供 NFT 市场功能（未来支持）。
- **DeFi API**: 查询协议列表、投资产品信息等。

## 安装

```bash
pip install okxos
```

## 快速开始
```bash
from okxos import OKXClient, WalletAPI

# 初始化客户端
client = OKXClient(
    api_key="your_api_key",
    secret_key="your_secret_key",
    passphrase="your_passphrase",
    project_id="your_project_id",
)

# 初始化 WalletAPI
wallet_api = WalletAPI(client)
