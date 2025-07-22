#!/usr/bin/env python3
"""
Solana Balance Watch / Rebate Calculation

Features:
1) One-off SOL balance snapshot
2) Weekly snapshots (every Monday at 00:00 UTC)
3) Per-epoch snapshots (~48h interval)
4) Compute balance change since any ISO‑8601 timestamp
5) Prompt for a custom RPC endpoint (e.g. Alchemy URL)
"""

import csv
import datetime
import os
import sys

from solana.rpc.api import Client
from apscheduler.schedulers.blocking import BlockingScheduler

# ── CONFIG ──────────────────────────────────────────────────────────────
DEFAULT_RPC = "https://api.mainnet-beta.solana.com"
CSV_FILE    = "balance_snapshots.csv"
# ─────────────────────────────────────────────────────────────────────────

client = None  # will be set in interactive_menu()

def get_balance(sol_address: str) -> float:
    """Return SOL balance (as float) for the given wallet."""
    resp = client.get_balance(sol_address)
    lamports = resp["result"]["value"]
    return lamports / 1e9

def record_snapshot(address: str):
    """Fetch balance and append a timestamped row to CSV."""
    now     = datetime.datetime.now(datetime.timezone.utc)
    balance = get_balance(address)
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "balance"])
        writer.writerow([now.isoformat(), f"{balance:.6f}"])
    print(f"[{now.isoformat()}] {address} → {balance:.6f} SOL")

def diff_since(address: str, iso_timestamp: str):
    """Compute balance change since the nearest logged snapshot."""
    try:
        with open(CSV_FILE) as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        print(f"No snapshots found ({CSV_FILE} missing).")
        return

    target = datetime.datetime.fromisoformat(iso_timestamp)
    snapshots = []
    for ts_str, bal_str in rows[1:]:
        ts  = datetime.datetime.fromisoformat(ts_str)
        bal = float(bal_str)
        snapshots.append((ts, bal))

    closest_time, closest_balance = min(snapshots, key=lambda x: abs(x[0] - target))
    current_balance = get_balance(address)
    delta = current_balance - closest_balance

    print(f"Snapshot @ {closest_time.isoformat()} → {closest_balance:.6f} SOL")
    print(f"Current balance → {current_balance:.6f} SOL")
    print(f"Δ since {closest_time.isoformat()} = {delta:+.6f} SOL")

def schedule_snapshots(address: str, frequency: str):
    """Start a blocking scheduler for periodic snapshots."""
    sched = BlockingScheduler(timezone="UTC")

    if frequency == "weekly":
        sched.add_job(
            lambda: record_snapshot(address),
            trigger="cron",
            day_of_week="mon",
            hour=0,
            minute=0,
            id="weekly_snapshot"
        )
        print("Scheduled weekly snapshots every Monday at 00:00 UTC.")

    elif frequency == "epoch":
        sched.add_job(
            lambda: record_snapshot(address),
            trigger="interval",
            hours=48,
            id="epoch_snapshot"
        )
        print("Scheduled snapshots every ~48 hours (approx. one epoch).")

    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

def interactive_menu():
    """CLI menu to choose functionality, including custom RPC."""
    global client

    print("=== Solana Balance Watch ===")
    rpc_input = input(f"Enter RPC endpoint [default: {DEFAULT_RPC}]: ").strip()
    client    = Client(rpc_input or DEFAULT_RPC)

    address = input("Enter Solana wallet address: ").strip()
    if not address:
        print("Wallet address is required. Exiting.")
        sys.exit(1)

    print("\nSelect an option:")
    print("1) Take a one-off snapshot")
    print("2) Schedule weekly snapshots")
    print("3) Schedule per-epoch snapshots (~48h)")
    print("4) Compute balance change since a timestamp")
    choice = input("Enter choice (1-4): ").strip()

    if choice == "1":
        record_snapshot(address)
    elif choice == "2":
        schedule_snapshots(address, "weekly")
    elif choice == "3":
        schedule_snapshots(address, "epoch")
    elif choice == "4":
        ts = input("Enter ISO‑8601 timestamp (e.g., 2025-07-15T12:00:00+00:00): ").strip()
        diff_since(address, ts)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    interactive_menu()
