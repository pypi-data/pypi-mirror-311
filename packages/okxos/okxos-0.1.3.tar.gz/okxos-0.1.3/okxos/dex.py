from okxos.okxos.client import OKXClient


class DEXAPI:
    def __init__(self, client: OKXClient):
        self.client = client

    async def get_supported_chains(self, chain_id=None):
        """
        获取支持的链信息。

        官方文档: https://www.okx.com/zh-hans/web3/build/docs/waas/dex-get-aggregator-supported-chains

        :param chain_id: 指定的链 ID，默认为 None 返回所有链信息。
        :return: 链信息的 JSON 数据。
        """
        endpoint = "/api/v5/dex/aggregator/supported/chain"
        params = {"chainId": chain_id} if chain_id else None
        return await self.client.request("GET", endpoint, params=params)

    # 获取币种列表
    async def get_all_tokens(self, chain_id):

        """
        获取指定链上的所有币种列表。
        官方文档: https://www.okx.com/zh-hans/web3/build/docs/waas/dex-get-tokens

        :param chain_id: 链 ID
        :return: 币种列表的 JSON 数据
        """

        endpoint = "/api/v5/dex/aggregator/all-tokens"
        params = {"chainId": chain_id}
        return await self.client.request("GET", endpoint, params=params)