#!/bin/bash

# Brahmastra CLI Demo Script
# Demonstrates all capabilities of the threat response engine
# Save as: ~/chakravyuh/brahmastra/demo.sh

echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║           BRAHMASTRA CLI DEMONSTRATION                ║"
echo "║        Automated Threat Response Engine               ║"
echo "║              Project Chakravyuh                       ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Function to pause between demos
pause() {
    echo ""
    echo "Press [ENTER] to continue..."
    read
    echo ""
}

# 1. List all playbooks
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 1: Listing Available Playbooks"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
brahmastra list
pause

# 2. Low Severity - Port Scan
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 2: Low Severity Threat - Port Scan"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Simulating: Port scan from 192.168.1.100 targeting 10.0.0.5"
echo ""
brahmastra respond \
    --threat-type port_scan \
    --severity low \
    --source-ip 192.168.1.100 \
    --target-ip 10.0.0.5 \
    --ports 22 80 443 8080 \
    --description "Systematic port scanning detected on multiple services"
pause

# 3. Medium Severity - Suspicious Activity
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 3: Medium Severity Threat - Suspicious Activity"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Simulating: Unusual traffic pattern from 172.16.0.50"
echo ""
brahmastra respond \
    --threat-type suspicious_activity \
    --severity medium \
    --source-ip 172.16.0.50 \
    --target-ip 10.0.0.8 \
    --description "Anomalous network behavior detected"
pause

# 4. High Severity - Intrusion Attempt
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 4: High Severity Threat - Intrusion Attempt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Simulating: SSH brute force attack from 203.0.113.45"
echo ""
brahmastra respond \
    --threat-type intrusion \
    --severity high \
    --source-ip 203.0.113.45 \
    --target-ip 10.0.0.10 \
    --ports 22 \
    --description "Multiple failed SSH authentication attempts" \
    --confidence 0.95
pause

# 5. Critical Severity - Exploit Attempt with JSON Export
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 5: Critical Severity Threat - Exploit Attempt"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Simulating: Log4Shell exploitation attempt from 198.51.100.89"
echo "Results will be exported to JSON file"
echo ""
brahmastra respond \
    --threat-type exploit_attempt \
    --severity critical \
    --source-ip 198.51.100.89 \
    --target-ip 10.0.0.15 \
    --ports 443 \
    --description "CVE-2021-44228 Log4Shell exploitation detected" \
    --confidence 0.98 \
    --export json
pause

# 6. Show exported results
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO 6: Viewing Exported Results"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Latest exported JSON file:"
ls -lth brahmastra_results_*.json 2>/dev/null | head -1
echo ""
echo "JSON Contents:"
cat $(ls -t brahmastra_results_*.json 2>/dev/null | head -1) 2>/dev/null | head -30
pause

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DEMO COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Demonstrated capabilities:"
echo "   • Playbook listing"
echo "   • Low severity response (1 action)"
echo "   • Medium severity response (2 actions)"
echo "   • High severity response (2+ actions with IP blocking)"
echo "   • Critical severity response (3+ actions with isolation)"
echo "   • JSON export functionality"
echo ""
echo "📊 All response actions executed successfully!"
echo "📁 Results exported to: brahmastra_results_*.json"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
