import sqlite3
import subprocess
import wakeonlan
import argparse
import time

DATABASE_PATH = 'endpoints.db'  # Update with the path to your SQLite database

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def get_devices(conn, tags=None):
    cur = conn.cursor()
    if tags:
        placeholders = ', '.join('?' for tag in tags)
        query = f"SELECT * FROM devices WHERE tag IN ({placeholders})"
        cur.execute(query, tags)
    else:
        cur.execute("SELECT * FROM devices")
    return cur.fetchall()

def ping_ip(ip_address):
    try:
        subprocess.check_output(["ping", "-c", "1", ip_address], stderr=subprocess.STDOUT, universal_newlines=True)
        return True
    except subprocess.CalledProcessError:
        return False

def wake_on_lan(mac_address):
    wakeonlan.send_magic_packet(mac_address)

def status(conn):
    devices = get_devices(conn)
    for ip, mac, _ in devices:
        if ping_ip(ip):
            print(f"{ip} is online.")
        else:
            print(f"{ip} is offline.")

def wake(conn, tags=None):
    devices = get_devices(conn, tags)
    for ip, mac, _ in devices:
        if not ping_ip(ip):
            wake_on_lan(mac)
            print(f"WoL signal sent to {mac} for IP {ip}")

def list_devices(conn):
    devices = get_devices(conn)
    for ip, mac, tag in devices:
        print(f"IP: {ip}, MAC: {mac}, Tag: {tag}")

def upsert_device(conn, ip, mac, tag):
    cur = conn.cursor()
    cur.execute("INSERT INTO devices (ip_address, mac_address, tag) VALUES (?, ?, ?) ON CONFLICT(ip_address) DO UPDATE SET mac_address=excluded.mac_address, tag=excluded.tag", (ip, mac, tag))
    conn.commit()

def remove_device(conn, ip):
    cur = conn.cursor()
    cur.execute("DELETE FROM devices WHERE ip_address = ?", (ip,))
    conn.commit()

def monitor_tags(conn, tags):
    while True:
        devices = get_devices(conn, tags)
        for ip, mac, _ in devices:
            if not ping_ip(ip):
                wake_on_lan(mac)
                print(f"WoL signal sent to {mac} for IP {ip}")
            else:
                print(f"{ip} is online.")
        time.sleep(60)  # Wait for 60 seconds before the next check

def main():
    parser = argparse.ArgumentParser(description="Manage and wake devices on a network.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Status command
    subparsers.add_parser('status', help='Check the status of all devices.')

    # Wake command
    wake_parser = subparsers.add_parser('wake', help='Wake devices on the network.')
    wake_parser.add_argument('tags', nargs='*', help='Tags of the devices to wake.')

    # List command
    subparsers.add_parser('list', help='List all devices in the database.')

    # Upsert command
    upsert_parser = subparsers.add_parser('upsert', help='Add or update a device in the database.')
    upsert_parser.add_argument('ip', help='IP address of the device.')
    upsert_parser.add_argument('mac', help='MAC address of the device.')
    upsert_parser.add_argument('tag', help='Tag associated with the device.')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a device from the database.')
    remove_parser.add_argument('ip', help='IP address of the device to remove.')

    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor and wake devices with specific tags.')
    monitor_parser.add_argument('tags', nargs='+', help='Tags of the devices to monitor and wake.')

    args = parser.parse_args()

    conn = create_connection(DATABASE_PATH)
    if conn is not None:
        if args.command == 'status':
            status(conn)
        elif args.command == 'wake':
            wake(conn, args.tags)
        elif args.command == 'list':
            list_devices(conn)
        elif args.command == 'upsert':
            upsert_device(conn, args.ip, args.mac, args.tag)
        elif args.command == 'remove':
            remove_device(conn, args.ip)
        elif args.command == 'monitor':
            monitor_tags(conn, args.tags)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()

