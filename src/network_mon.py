# Script for monitoring network health and statistics

import json
import requests
import psutil
import pyshark
import netifaces
from scapy.all import sniff, Raw
from bcc import BPF

# Bandwidth monitoring

net_io = psutil.net_io_counters(pernic=True)  # Get per-interface stats

# Format JSON output
network_stats = {iface: {
    "bytes_sent": stats.bytes_sent,
    "bytes_recv": stats.bytes_recv,
    "packets_sent": stats.packets_sent,
    "packets_recv": stats.packets_recv
} for iface, stats in net_io.items()}

print(json.dumps(network_stats, indent=4))

#Sniff and Analyise

## Function to process packets
def process_packet(packet):
    if packet.haslayer(Raw):
        packet_data = {
            "src": packet[0].src,
            "dst": packet[0].dst,
            "protocol": packet[0].proto,
            "payload": packet[Raw].load.hex()
        }
        print(json.dumps(packet_data, indent=4))

## Sniff packets on eth0 (change to correct interface)
sniff(iface="eth0", filter="port 1935", prn=process_packet, count=10)

#Protocal Analysis

## Capture packets on eth0 for RTMP (port 1935)
capture = pyshark.LiveCapture(interface='eth0', display_filter='tcp.port == 1935')

for packet in capture.sniff_continuously(packet_count=5):
    packet_info = {
        "timestamp": packet.sniff_time.isoformat(),
        "src_ip": packet.ip.src,
        "dst_ip": packet.ip.dst,
        "protocol": packet.transport_layer,
        "length": packet.length
    }
    print(json.dumps(packet_info, indent=4))

#NIC Info



interfaces = {iface: netifaces.ifaddresses(iface) for iface in netifaces.interfaces()}
print(json.dumps(interfaces, indent=4))

#Network Monitoring

## BPF program to monitor TCP packets
bpf_script = """
int kprobe__tcp_sendmsg(struct pt_regs *ctx) {
    bpf_trace_printk("TCP packet sent\\n");
    return 0;
}
"""

bpf = BPF(text=bpf_script)
while True:
    packet = bpf.trace_fields()
    print(json.dumps({"event": "TCP packet sent"}, indent=4))

# Speedtest

## Fetch speed test from Fast API
response = requests.get("https://fast.com/api/v1?https=true")
speedtest_results = response.json()

## Print JSON
print(json.dumps(speedtest_results, indent=4))
