# wallet-balance-calculations
Interactive Python script to monitor Solana wallet balances: take one‑off snapshots, schedule weekly or per‑epoch snapshots, and compute balance changes since any ISO‑8601 timestamp. Logs all data to a CSV file for easy analysis. Requires Python 3.6+, solana, and apscheduler.
# Solana Balance Watch

**Interactive Python script to snapshot and monitor SOL balances**  
Provides one‑off snapshots, weekly or per‑epoch scheduling, and balance‑change calculations since a given timestamp.

## Features

- 🔍 **One‑off snapshot** of any Solana wallet’s SOL balance  
- 📆 **Weekly scheduler** (every Monday at 00:00 UTC)  
- ⏳ **Per‑epoch scheduler** (approx. every 48 hours)  
- 📈 **Delta calculation**: compute balance change since any ISO‑8601 timestamp  
- 💾 Logs all snapshots to a CSV file for audit and analysis  

## Requirements

- Python 3.6+  
- Install dependencies:
  ```bash
  pip install solana apscheduler
You’ll be asked for:

Wallet address

Option:

One‑off snapshot

Schedule weekly snapshots

Schedule per‑epoch snapshots

Compute balance change since a timestamp

For example, to compute delta since July 15, 2025 at noon UTC:

java
Copy
Edit
Enter choice (1-4): 4
Enter timestamp (e.g. 2025-07-15T12:00:00+00:00): 2025-07-15T12:00:00+00:00
Snapshots are appended to balance_snapshots.csv in the project directory.

Configuration
RPC_ENDPOINT: Change the Solana JSON‑RPC endpoint if you use a custom node or a provider like QuickNode/Helius.

CSV_FILE: Modify the filename or path where snapshots are stored.

Next Steps
🔧 Swap CSV for a database (Postgres/Mongo) for more robust querying

🔔 Integrate alerts (e.g., email/Slack) when balance dips below a threshold

🔄 Add token‑account support to track SPL tokens

License
MIT License © 2025 Georgy S. Ezhakunnel
