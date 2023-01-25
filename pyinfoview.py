from icmplib import ping
from rich.console import Console
from rich.table import Table

import time

from rich.live import Live
from rich.table import Table

hosts = ['1.1.1.1', '8.8.8.8', '153.106.4.1', '192.168.88.3']


# for host in hosts:
#   result = ping(host, count=1, privileged=False)  
#   print(result.is_alive, result.avg_rtt)

# table = Table()
# table.add_column("Alive")
# table.add_column("Host")
# table.add_column("Last RTT")

# with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
#   for host in hosts:
#     time.sleep(0.4)  # arbitrary delay
#     # update the renderable internally
#     result = ping(host, count=1, privileged=False)
#     table.add_row(f"{result.is_alive}", f"{host}", "[red]ERROR")


# {'1.1.1.1': { 'is_alive': True, 
#               'packets_sent': 0, 
#               'packets_received': 0, 
#               'packet_loss': 0, 
#               'rtts': [0]
# }
# }

results = {}

def ping_host(host):
  if host not in results: results[host] = {}
  result = ping(host, count=1, privileged=False, timeout=2)  
  results[host]['is_alive'] = result.is_alive
  if 'history' not in results[host]: results[host]['history'] = []
  if result.is_alive:
    results[host]['history'].append(':white_check_mark:')
  else:
    results[host]['history'].append(':x:')
  if 'packets_sent' not in results[host]: results[host]['packets_sent'] = 0
  results[host]['packets_sent'] += result.packets_sent
  if 'packets_received' not in results[host]: results[host]['packets_received'] = 0
  results[host]['packets_received'] += result.packets_received
  results[host]['packet_loss'] = ((results[host]['packets_sent'] - results[host]['packets_received']) / results[host]['packets_sent']) * 100
  if 'rtts' not in results[host]: results[host]['rtts'] = []
  results[host]['rtts'].append(result.avg_rtt)
  # avg = sum(number_list)/len(number_list)
  results[host]['last_rtt'] = result.avg_rtt
  results[host]['average_rtt'] = sum(results[host]['rtts'])/len(results[host]['rtts'])
  # print(results)


def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("Alive")
    table.add_column("Host")
    table.add_column("History")
    table.add_column("Loss")
    table.add_column("Received")
    table.add_column("Sent")
    table.add_column("Last RTT")
    table.add_column("Mean RTT")

    for host in hosts:
        ping_host(host)
        # result = ping(host, count=1, privileged=False, timeout=2)  
        table.add_row(
            f"[green]UP" if results[host]['is_alive'] else "[red]DOWN", 
            f"{host}", 
            # history = ()
            f"{''.join(results[host]['history'][-10:])}",
            # result = ''.join(str(item) for item in list_of_integers)
            f"{results[host]['packet_loss']}%",
            f"{results[host]['packets_received']}",
            f"{results[host]['packets_sent']}",
            f"{round(results[host]['last_rtt'], 2)}",
            f"{round(results[host]['average_rtt'], 2)}",
        )
    return table

with Live(generate_table(), refresh_per_second=4) as live:
  while(True):
    time.sleep(1)
    live.update(generate_table())
