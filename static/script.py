from js import window, document, alert
import json
from pyodide import create_proxy
from pyodide.http import pyfetch
import asyncio


#--- Enable Nami ---#
nami = window.cardano.nami

async def enable_nami(*args):
    global nami_api
    nami_api = await nami.enable()
    h3_ele = document.querySelector("#wallet")
    h3_ele.innerText = f'Wallet enabled: True'

enable_wallet_btn = document.querySelector("#enable-wallet")
enable_wallet_btn.addEventListener('click', create_proxy(enable_nami))
if await nami.isEnabled():
    enable_wallet_btn.click()


#--- Build tx --#
async def build_tx(*args):
    if not await nami.isEnabled():
        alert("Enable wallet first")
        return

    r = await pyfetch(
        url = "/cbor",
        method = "POST",
        headers = {
            "Content-Type": "application/json"
        },
        body = json.dumps({
            "sender_addr": (await nami_api.getUsedAddresses())[0],
            "change_addr": await nami_api.getChangeAddress()
        })
    )
    tx = await r.json()
    
    tx_cbor = tx["cborHex"]
    witness_cbor = await nami_api.signTx(tx_cbor)

    await pyfetch(
        url = "/submit",
        method = "POST",
        headers = {
            "Content-Type": "application/json"
        },
        body = json.dumps({
            "tx_cbor": tx_cbor,
            "witness_cbor": witness_cbor
        })
    )

build_tx_btn = document.querySelector("#build-tx")
build_tx_btn.addEventListener('click', create_proxy(build_tx))