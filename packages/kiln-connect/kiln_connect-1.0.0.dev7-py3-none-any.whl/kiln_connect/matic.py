from kiln_connect import utils
import logging
from kiln_connect.integrations import Integrations, Asset
from kiln_connect.openapi_client import (
    MaticApi,
    ApiClient,
)
from kiln_connect.openapi_client import (
    MATICCraftApproveTxPayload,
    MATICCraftBuyVoucherTxPayload,
    MATICPrepareTxPayload,
    MATICBroadcastTxPayload,
    MATICCraftSellVoucherTxPayload,
    MATICCraftUnstakeClaimTokensTxPayload,
    MATICCraftWithdrawRewardsTxPayload,
    MATICCraftRestakeRewardsTxPayload
)


class MATIC(MaticApi):
    """Wrapper for the Polygon API.
    """

    def __init__(self, api: ApiClient, integrations: Integrations):
        super().__init__(api)
        self.integrations = integrations

    def stake(self, integration: str, account_id: str, wallet: str, contract_addr: str, validator: str, amount: str):
        """
        Delegate the amount, with an approval step
        :param integration: integration name
        :param account_id: id of the kiln account to use for the stake transaction
        :param wallet: wallet address signing the transaction
        :param contract_addr: contract address that you allow to spend the token
        :param validator: ValidatorShare proxy contract address of the validator
        :param amount: how many tokens to stake and approve in MATIC
        """

        response = super().post_matic_approve_tx(MATICCraftApproveTxPayload(
            wallet=wallet,
            contract=contract_addr,
            amount_wei=utils.matic_to_wei(amount)
        ))
        logging.debug(f"Approval TX Hash: {response.data.unsigned_tx_hash}")
        # buy
        response = super().post_matic_buy_voucher_tx(MATICCraftBuyVoucherTxPayload(
            account_id=account_id,
            wallet=wallet,
            validator_share_proxy_address=validator,
            amount_wei=utils.matic_to_wei(amount)
        ))
        logging.debug(f"Buy Voucher TX Hash: {response.data.unsigned_tx_hash}")

        fb = self.integrations.get_integration(integration)
        sig = fb.raw_sign(Asset.matic, response.data.unsigned_tx_hash)
        logging.debug("TX Signed")

        response = super().post_matic_prepare_tx(MATICPrepareTxPayload(
            unsigned_tx_serialized=response.data.unsigned_tx_serialized,
            r=sig.get("r"),
            s=sig.get("s"),
            v=sig.get("v")
        ))

        logging.debug(f"TX Prepared: {response.data.signed_tx_serialized}")

        response = super().post_matic_broadcast_tx(MATICBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized
        ))
        logging.debug(f"TX Broadcasted: {response.data.tx_hash}")

        return response.data

    def unstake(self, integration: str, wallet: str, validator: str, amount: str):
        """
        Unstake the amount
        :param integration: integration name
        :param wallet: wallet address signing the transaction
        :param validator: ValidatorShare proxy contract address of the validator
        :param amount: how many tokens to stake and approve in MATIC
        """

        response = super().post_matic_sell_voucher_tx(MATICCraftSellVoucherTxPayload(
            wallet=wallet,
            validator_share_proxy_address=validator,
            amount_wei=utils.matic_to_wei(amount)
        ))
        logging.debug(f"[bold]TX Hash:[/bold] {response.data.unsigned_tx_hash}")

        fb = self.integrations.get_integration(integration)
        sig = fb.raw_sign(Asset.matic, response.data.unsigned_tx_hash)
        logging.debug("TX Signed")

        response = super().post_matic_prepare_tx(MATICPrepareTxPayload(
            unsigned_tx_serialized=response.data.unsigned_tx_serialized,
            r=sig.get("r"),
            s=sig.get("s"),
            v=sig.get("v")
        ))

        logging.debug(f"TX Prepared: {response.data.signed_tx_serialized}")

        response = super().post_matic_broadcast_tx(MATICBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized
        ))
        logging.debug(f"TX Broadcasted: {response.data.tx_hash}")

        return response.data

    def withdraw_rewards(self, integration: str, wallet: str, validator: str):
        """
        Generates a withdraw rewards transaction to withdraw available rewards to your wallet
        :param integration: integration name
        :param wallet: wallet address signing the transaction
        :param validator: ValidatorShare proxy contract address of the validator
        """

        response = super().post_matic_withdraw_rewards_tx(MATICCraftWithdrawRewardsTxPayload(
            wallet=wallet,
            validator_share_proxy_address=validator
        ))
        logging.debug(f"[bold]TX Hash:[/bold] {response.data.unsigned_tx_hash}")

        fb = self.integrations.get_integration(integration)
        sig = fb.raw_sign(Asset.matic, response.data.unsigned_tx_hash)
        logging.debug("TX Signed")

        response = super().post_matic_prepare_tx(MATICPrepareTxPayload(
            unsigned_tx_serialized=response.data.unsigned_tx_serialized,
            r=sig.get("r"),
            s=sig.get("s"),
            v=sig.get("v")
        ))

        logging.debug(f"TX Prepared: {response.data.signed_tx_serialized}")

        response = super().post_matic_broadcast_tx(MATICBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized
        ))
        logging.debug(f"TX Broadcasted: {response.data.tx_hash}")

        return response.data

    def unstake_claim_tokens(self, integration: str, wallet: str, validator: str):
        """
        Generates an unstakeClaimTokens transaction to withdraw unbonded tokens back to your wallet
        :param integration: integration name
        :param wallet: wallet address signing the transaction
        :param validator: ValidatorShare proxy contract address of the validator
        """

        response = super().post_matic_unstake_claim_tokens_tx(MATICCraftUnstakeClaimTokensTxPayload(
            wallet=wallet,
            validator_share_proxy_address=validator
        ))
        logging.debug(f"[bold]TX Hash:[/bold] {response.data.unsigned_tx_hash}")

        fb = self.integrations.get_integration(integration)
        sig = fb.raw_sign(Asset.matic, response.data.unsigned_tx_hash)
        logging.debug("TX Signed")

        response = super().post_matic_prepare_tx(MATICPrepareTxPayload(
            unsigned_tx_serialized=response.data.unsigned_tx_serialized,
            r=sig.get("r"),
            s=sig.get("s"),
            v=sig.get("v")
        ))

        logging.debug(f"TX Prepared: {response.data.signed_tx_serialized}")

        response = super().post_matic_broadcast_tx(MATICBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized
        ))
        logging.debug(f"TX Broadcasted: {response.data.tx_hash}")

        return response.data

    def restake_rewards(self, integration: str, wallet: str, validator: str):
        """
        Generates a restake rewards transaction to restake available rewards to the given validator
        :param integration: integration name
        :param wallet: wallet address signing the transaction
        :param validator: ValidatorShare proxy contract address of the validator
        """

        response = super().post_matic_restake_rewards_tx(MATICCraftRestakeRewardsTxPayload(
            wallet=wallet,
            validator_share_proxy_address=validator
        ))
        logging.debug(f"[bold]TX Hash:[/bold] {response.data.unsigned_tx_hash}")

        fb = self.integrations.get_integration(integration)
        sig = fb.raw_sign(Asset.matic, response.data.unsigned_tx_hash)
        logging.debug("TX Signed")

        response = super().post_matic_prepare_tx(MATICPrepareTxPayload(
            unsigned_tx_serialized=response.data.unsigned_tx_serialized,
            r=sig.get("r"),
            s=sig.get("s"),
            v=sig.get("v")
        ))

        logging.debug(f"TX Prepared: {response.data.signed_tx_serialized}")

        response = super().post_matic_broadcast_tx(MATICBroadcastTxPayload(
            tx_serialized=response.data.signed_tx_serialized
        ))
        logging.debug(f"TX Broadcasted: {response.data.tx_hash}")

        return response.data
