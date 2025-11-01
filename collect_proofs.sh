echo "🔥 BRAHMASTRA PROOF COLLECTION STARTED"
echo "======================================"
echo ""

# ============================================
# 1. HEALTH CHECK
# ============================================
echo "✓ Collecting: Health Check..."
curl -s http://localhost:8000/health | jq > proofs/01_health.json
curl -s http://localhost:8000/health | jq

echo ""
echo "--------------------"

# ============================================
# 2. PLAYBOOKS LIST
# ============================================
echo "✓ Collecting: All Playbooks..."
curl -s http://localhost:8000/playbooks | jq > proofs/02_playbooks.json
curl -s http://localhost:8000/playbooks | jq

echo ""
echo "--------------------"

# ============================================
# 3. STATISTICS
# ============================================
echo "✓ Collecting: Statistics..."
curl -s http://localhost:8000/stats | jq > proofs/03_stats.json
curl -s http://localhost:8000/stats | jq

echo ""
echo "--------------------"

# ============================================
# 4. LOW SEVERITY THREAT
# ============================================
echo "✓ Testing: LOW Severity Port Scan..."
curl -s -X POST http://localhost:8000/threats \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "192.168.1.100",
    "target_ip": "10.0.0.5",
    "target_ports": [22, 80, 443],
    "severity": "LOW",
    "threat_type": "port_scan",
    "description": "Proof: Low severity port scan"
  }' | jq > proofs/04_low_severity.json

cat proofs/04_low_severity.json | jq

echo ""
echo "--------------------"

# ============================================
# 5. MEDIUM SEVERITY THREAT
# ============================================
echo "✓ Testing: MEDIUM Severity Suspicious Activity..."
curl -s -X POST http://localhost:8000/threats \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "172.16.0.50",
    "target_ip": "10.0.0.8",
    "severity": "MEDIUM",
    "threat_type": "suspicious_activity",
    "description": "Proof: Medium severity anomaly"
  }' | jq > proofs/05_medium_severity.json

cat proofs/05_medium_severity.json | jq

echo ""
echo "--------------------"

# ============================================
# 6. HIGH SEVERITY THREAT
# ============================================
echo "✓ Testing: HIGH Severity Intrusion..."
curl -s -X POST http://localhost:8000/threats \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "203.0.113.45",
    "target_ip": "10.0.0.10",
    "target_ports": [22],
    "severity": "HIGH",
    "threat_type": "intrusion",
    "description": "Proof: High severity SSH attack",
    "confidence_score": 0.95
  }' | jq > proofs/06_high_severity.json

cat proofs/06_high_severity.json | jq

echo ""
echo "--------------------"

# ============================================
# 7. CRITICAL SEVERITY THREAT
# ============================================
echo "✓ Testing: CRITICAL Severity Exploit..."
curl -s -X POST http://localhost:8000/threats \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "198.51.100.89",
    "target_ip": "10.0.0.15",
    "target_ports": [443],
    "severity": "CRITICAL",
    "threat_type": "exploit_attempt",
    "description": "Proof: Log4Shell exploitation",
    "cve_ids": ["CVE-2021-44228"],
    "confidence_score": 0.98
  }' | jq > proofs/07_critical_severity.json

cat proofs/07_critical_severity.json | jq

echo ""
echo "--------------------"

# ============================================
# 8. BATCH PROCESSING
# ============================================
echo "✓ Testing: Batch Threat Processing..."
curl -s -X POST http://localhost:8000/threats/batch \
  -H "Content-Type: application/json" \
  -d '[
    {
      "source_ip": "192.168.1.10",
      "target_ip": "10.0.0.1",
      "severity": "LOW",
      "threat_type": "port_scan"
    },
    {
      "source_ip": "203.0.113.50",
      "target_ip": "10.0.0.2",
      "severity": "HIGH",
      "threat_type": "intrusion"
    },
    {
      "source_ip": "198.51.100.100",
      "target_ip": "10.0.0.3",
      "severity": "CRITICAL",
      "threat_type": "exploit_attempt"
    }
  ]' | jq > proofs/08_batch_processing.json

cat proofs/08_batch_processing.json | jq

echo ""
echo "--------------------"

# ============================================
# 9. CLI TESTS
# ============================================
echo "✓ Testing: CLI List Command..."
brahmastra list > proofs/09_cli_list.txt 2>&1

echo "✓ Testing: CLI Response Command..."
brahmastra respond \
  --threat-type port_scan \
  --severity low \
  --source-ip 192.168.1.200 \
  --target-ip 10.0.0.50 \
  --export json > proofs/10_cli_response.txt 2>&1

echo ""
echo "--------------------"

# ============================================
# 10. UNIT TESTS
# ============================================
echo "✓ Running: All Unit Tests..."
python3 -m unittest discover tests -v > proofs/11_test_results.txt 2>&1

echo ""
echo "======================================"
echo "✅ PROOF COLLECTION COMPLETE!"
echo ""
echo "📁 All proofs saved in: ~/chakravyuh/brahmastra/proofs/"
echo ""
echo "Files created:"
ls -lh proofs/
echo ""
echo "Total files: $(ls proofs/ | wc -l)"
