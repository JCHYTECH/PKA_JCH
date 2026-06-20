#!/usr/bin/env python3
"""Bridge TCP:6638 <-> /dev/cu.usbserial-10 @ 115200 pour ZHA/EZSP.
v3 — threaded (stable), shared serial, graceful."""
import socket, serial, threading, signal, sys, time

SERIAL_PORT = "/dev/cu.usbserial-10"
BAUD = 115200
TCP_PORT = 6638

running = True

def shutdown(sig, frame):
    global running
    print("[bridge] shutdown", flush=True)
    running = False

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# Shared serial — opened once
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=0.05)
print(f"[bridge] serial {SERIAL_PORT}@{BAUD}", flush=True)

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", TCP_PORT))
srv.listen(1)
srv.settimeout(1.0)
print(f"[bridge] TCP:{TCP_PORT}", flush=True)

write_lock = threading.Lock()

def handle(conn, addr):
    print(f"[bridge] client {addr}", flush=True)
    stop = threading.Event()
    
    def tcp_to_ser():
        try:
            while not stop.is_set():
                try:
                    data = conn.recv(4096)
                except socket.timeout:
                    continue
                if not data:
                    break
                with write_lock:
                    ser.write(data)
        except Exception as e:
            print(f"[tcp→ser] {e}", flush=True)
        finally:
            stop.set()

    def ser_to_tcp():
        try:
            while not stop.is_set():
                with write_lock:
                    waiting = ser.in_waiting
                    if waiting:
                        data = ser.read(waiting)
                    else:
                        data = None
                if data:
                    try:
                        conn.sendall(data)
                    except Exception:
                        break
                else:
                    time.sleep(0.001)
        except Exception as e:
            if not stop.is_set():
                print(f"[ser→tcp] {e}", flush=True)

    t1 = threading.Thread(target=tcp_to_ser, daemon=True)
    t2 = threading.Thread(target=ser_to_tcp, daemon=True)
    t1.start(); t2.start()
    t1.join()
    stop.set()
    t2.join(timeout=1)
    conn.close()
    print(f"[bridge] client {addr} déconnecté", flush=True)

try:
    while running:
        try:
            conn, addr = srv.accept()
            conn.settimeout(0.1)
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
        except socket.timeout:
            continue
except KeyboardInterrupt:
    pass
finally:
    ser.close()
    srv.close()
    print("[bridge] terminé", flush=True)
