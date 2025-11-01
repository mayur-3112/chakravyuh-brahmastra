#!/bin/bash
# Quick non-interactive demo
# Save as: ~/chakravyuh/brahmastra/quick_demo.sh

echo "🔥 Brahmastra Quick Demo"
echo ""

echo "1️⃣ Low Severity..."
brahmastra respond --threat-type port_scan --severity low --source-ip 192.168.1.100 --target-ip 10.0.0.5

echo ""
echo "2️⃣ Medium Severity..."
brahmastra respond --threat-type suspicious_activity --severity medium --source-ip 172.16.0.50 --target-ip 10.0.0.8

echo ""
echo "3️⃣ High Severity..."
brahmastra respond --threat-type intrusion --severity high --source-ip 203.0.113.45 --target-ip 10.0.0.10

echo ""
echo "4️⃣ Critical Severity with Export..."
brahmastra respond --threat-type exploit_attempt --severity critical --source-ip 198.51.100.89 --target-ip 10.0.0.15 --export json

echo ""
echo "✅ Demo Complete!"
