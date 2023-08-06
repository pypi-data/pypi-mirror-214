"""Polygon commands.

This file contains multiple CLI commands showcasing how to use the
KilnConnect SDK to interact with the Polygon blockchain.

Code here is voluntarily kept simple: it could be refactored with some
levels of abstraction to avoid repetitions, but would imply readers to
understand things unrelated to what their primary goal is: use the
SDK. So let's keep it stupid simple so the integration work is
simpler.
"""
import typer

from rich.console import Console

import kiln_connect

matic_cli = typer.Typer(
    name='matic', help='Staking utilities for Polygon', no_args_is_help=True)

console = Console()
error_console = Console(stderr=True)


@matic_cli.command("stake")
def matic_stake(account_id: str, wallet: str, contract_addr: str, validator: str, amount: str):
    """
    Stake to a ValidatorShare proxy contract
    :param account_id: id of the kiln account to use for the stake transaction
    :param wallet: wallet address delegating
    :param contract_addr: ValidatorShare proxy contract address of the validator
    :param validator: ValidatorShare proxy contract address of the validator
    :param amount: how many tokens to stake in MATIC
    :return:
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        response = kc.matic.stake(
            integration="fireblocks",
            account_id=account_id,
            wallet=wallet,
            contract_addr=contract_addr,
            validator=validator,
            amount=amount
        )
        console.print(f"[bold]Done:[/bold] {response.data.tx_hash}")


@matic_cli.command("unstake")
def matic_unstake(wallet_addr: str, validator_addr: str, amount: str):
    """
    Unstake wallet from a ValidatorShare proxy contract
    :param wallet_addr: wallet address delegating
    :param validator_addr: ValidatorShare proxy contract address of the validator
    :param amount: how many tokens to unbond in MATIC
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        response = kc.matic.unstake(
            integration="fireblocks",
            wallet_addr=wallet_addr,
            validator=validator_addr,
            amount=amount
        )
        console.print(f"[bold]Done:[/bold] {response.data.tx_hash}")


@matic_cli.command("claim_tokens")
def matic_claim_tokens(wallet_addr: str, validator_addr: str):
    """
    Claim unbonded tokens from a ValidatorShare proxy contract
    :param wallet_addr: wallet address delegating
    :param validator_addr: ValidatorShare proxy contract address of the validator
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        response = kc.matic.unstake_claim_tokens(
            integration="fireblocks",
            wallet_addr=wallet_addr,
            validator=validator_addr,
        )
        console.print(f"[bold]Done:[/bold] {response.data.tx_hash}")


@matic_cli.command("withdraw_rewards")
def matic_withdraw_rewards(wallet_addr: str, validator_addr: str):
    """
    Withdraw available rewards to your wallet
    :param wallet_addr: wallet address delegating
    :param validator_addr: ValidatorShare proxy contract address of the validator
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        response = kc.matic.withdraw_rewards(
            integration="fireblocks",
            wallet_addr=wallet_addr,
            validator_share_proxy_address=validator_addr,
        )
        console.print(f"[bold]Done:[/bold] {response.data.tx_hash}")


@matic_cli.command("restake_rewards")
def matic_restake_rewards(wallet_addr: str, validator_addr: str):
    """
    Restakes available rewards
    :param wallet_addr: wallet address delegating
    :param validator_addr: ValidatorShare proxy contract address of the validator
    """
    with kiln_connect.KilnConnect(kiln_connect.KilnConfig.from_env()) as kc:
        response = kc.matic.withdraw_rewards(
            integration="fireblocks",
            wallet_addr=wallet_addr,
            validator_share_proxy_address=validator_addr,
        )
        console.print(f"[bold]Done:[/bold] {response.data.tx_hash}")