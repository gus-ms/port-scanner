import socket
import argparse
from datetime import datetime


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


def banner():
    print(f"""
{Colors.BLUE}
========================================
             PORT SCANNER
========================================
{Colors.RESET}
""")


def get_hostname(target):
    try:
        hostname = socket.gethostbyaddr(target)
        print(f"{Colors.GREEN}[+] Hostname:{Colors.RESET} {hostname[0]}")
    except socket.herror:
        print(f"{Colors.YELLOW}[!] Hostname não encontrado{Colors.RESET}")


def scan_ports(target, start_port, end_port):
    print(f"{Colors.GREEN}[+] Escaneando:{Colors.RESET} {target}")
    get_hostname(target)
    print()

    open_ports = []
    start_time = datetime.now()

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "unknown"

            print(f"{Colors.GREEN}[PORTA ABERTA]{Colors.RESET} Porta {port} ({service})")
            open_ports.append((port, service))

        sock.close()

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\n{Colors.BLUE}[+] Scan finalizado em:{Colors.RESET} {duration}")

    if not open_ports:
        print(f"{Colors.RED}[-] Nenhuma porta aberta encontrada.{Colors.RESET}")

    return open_ports


def save_report(target, open_ports):
    filename = f"scan_{target}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Scan report for {target}\n")
        file.write(f"Date: {datetime.now()}\n\n")

        if open_ports:
            for port, service in open_ports:
                file.write(f"Port {port} - {service}\n")
        else:
            file.write("Nenhuma porta aberta encontrada.\n")

    print(f"{Colors.BLUE}[+] Relatório salvo em:{Colors.RESET} {filename}")


def main():
    parser = argparse.ArgumentParser(description="Port Scanner em Python")
    parser.add_argument("target", help="IP ou domínio alvo")
    parser.add_argument("--start", type=int, default=1, help="Porta inicial")
    parser.add_argument("--end", type=int, default=1024, help="Porta final")
    parser.add_argument("--save", action="store_true", help="Salvar relatório")

    args = parser.parse_args()

    banner()

    open_ports = scan_ports(args.target, args.start, args.end)

    if args.save:
        save_report(args.target, open_ports)


if __name__ == "__main__":
    main()