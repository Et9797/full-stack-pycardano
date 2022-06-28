from pycardano import *


NETWORK = Network.TESTNET
chain_context = BlockFrostChainContext(
    project_id="testnetVrmjl6D9NhZQF7HM2AZYDew9HyWXnw7a",
    network=NETWORK
)


def build_unsigned_tx(data) -> Transaction:
    sender_addr = Address.from_primitive(bytes.fromhex(data["sender_addr"]))
    change_addr = Address.from_primitive(bytes.fromhex(data["change_addr"]))
    receiver_addr = Address.from_primitive("addr_test1qz9y3jwn73yxx30qppvgt9vg9jqdgh0wt75gu6xf0gj9t52h2gyvwzj5amupeaj0nnuva3nhquh9mzmchqw654qm962q6gln5t")

    builder = TransactionBuilder(chain_context)

    builder.add_input_address(sender_addr)
    builder.add_output(
        TransactionOutput(
            address=receiver_addr,
            amount=249_000_000
        )
    )
    
    tx_body = builder.build(change_address=change_addr)
    unsigned_tx = Transaction(tx_body, TransactionWitnessSet())

    return unsigned_tx


def compose_tx_and_witness(data) -> Transaction:
    tx = Transaction.from_cbor(data['tx_cbor'])
    witness = TransactionWitnessSet.from_cbor(data['witness_cbor'])
    tx.transaction_witness_set = witness
    return tx