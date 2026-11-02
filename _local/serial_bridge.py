#!/usr/bin/env python3
"""Bridge TCP ↔ Serial pour Sonoff ZBDongle-E. v4 — select-based, zero latency."""
import socket
import serial
import select
import threading
import sys

TCP_PORT = 6638
SERIAL_DEV = '/dev/tty.usbserial-1110'
BAUD = 115200

def bridge(conn, ser):
    """Bidirectional bridge using select for minimal latency."""
    conn.setblocking(False)
    ser.timeout = 0
    try:
        while True:
            # Wait for data on either socket or serial
            readable, _, _ = select.select([conn, ser], [], [], 0.05)
            if conn in readable:
                data = conn.recv(4096)
                if not data:
                    break
                ser.write(data)
                ser.flush()
            if ser in readable:
                data = ser.read(ser.in_waiting or 4096)
                if data:
                    conn.sendall(data)
    except (OSError, serial.SerialException):
        pass

def handle_client(conn, addr):
    print(f"[bridge] Connected: {addr}", flush=True)
    try:
        ser = serial.Serial(SERIAL_DEV, BAUD, timeout=0, rtscts=False)
        bridge(conn, ser)
        ser.close()
    except Exception as e:
        print(f"[bridge] Error: {e}", flush=True)
    finally:
        try: conn.close()
        except: pass
        print(f"[bridge] Disconnected: {addr}", flush=True)

def main():
    print(f"[bridge] TCP:{TCP_PORT} → {SERIAL_DEV}@{BAUD}", flush=True)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('0.0.0.0', TCP_PORT))
    srv.listen(5)
    while True:
        conn, addr = srv.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    main()
