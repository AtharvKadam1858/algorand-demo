# algorand_tool.py
import os
from algosdk import account, mnemonic
from algosdk.v2client import algod

# Connect to Algorand TestNet (public API from AlgoNode)
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
client = algod.AlgodClient("", ALGOD_ADDRESS)

MNEMONIC_FILE = "mnemonic.txt"

def create_account():
    """Generate a new TestNet account and save mnemonic to file"""
    private_key, address = account.generate_account()
    mnemo = mnemonic.from_private_key(private_key)

    print("\n🎉 New Algorand TestNet account generated!\n")
    print("Address:", address)
    print("Mnemonic (save this safely):", mnemo)

    # Save mnemonic to file
    with open(MNEMONIC_FILE, "w") as f:
        f.write(mnemo)
    print(f"\n📝 Mnemonic saved to {MNEMONIC_FILE}\n")

    return address

def check_balance(address):
    """Check balance of an account"""
    account_info = client.account_info(address)
    balance = account_info.get("amount") / 1e6
    print(f"\n💰 Account {address} balance: {balance} Algos")
    if balance == 0.0:
        print("\n⚠️ Your account has 0 Algos.")
        print("👉 Fund it using the official TestNet dispenser:")
        print("   🔗 https://bank.testnet.algorand.network/")

def reuse_account():
    """Reuse saved mnemonic from file or ask user"""
    try:
        if os.path.exists(MNEMONIC_FILE):
            with open(MNEMONIC_FILE, "r") as f:
                mnemo = f.read().strip()
            print(f"\n📂 Loaded mnemonic from {MNEMONIC_FILE}")
        else:
            mnemo = input("\nPaste your 25-word mnemonic:\n> ").strip()

        private_key = mnemonic.to_private_key(mnemo)
        address = account.address_from_private_key(private_key)
        print("\n🔑 Reusing account:")
        print("Address:", address)
        check_balance(address)
    except Exception as e:
        print("❌ Error: Invalid mnemonic provided")
        print(e)

def main():
    print("====================================")
    print("   🚀 Algorand Demo Tool (TestNet)   ")
    print("====================================")
    print("1. Generate new account")
    print("2. Reuse existing account (from file or manual)")
    choice = input("\nChoose an option (1/2): ")

    if choice == "1":
        address = create_account()
        check_balance(address)
    elif choice == "2":
        reuse_account()
    else:
        print("❌ Invalid choice. Please run again.")

if __name__ == "__main__":
    main()
