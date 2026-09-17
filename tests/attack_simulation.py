import sys
import requests

if len(sys.argv) < 2:
    print("[-] Error: Missing API Endpoint.")
    print("    Usage: python attack_simulation.py <API_ENDPOINT>")
    sys.exit(1)

API_ENDPOINT = sys.argv[1]

def run_attack_suite():
    print("=== STARTING CLOUD THREAT SIMULATION ===")

    # Test 1: Unauthenticated request (Missing Bearer Token)
    print("\n[+] Executing Test 1: Unauthenticated Endpoint Scan")
    res1 = requests.get(API_ENDPOINT)
    print(f"    Response Status: {res1.status_code} (Expected: 401 Unauthorized)")

    # Test 2: Invalid/Tampered Token Injection
    print("\n[+] Executing Test 2: Tampered Bearer Token Injection")
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.MALICIOUS_PAYLOAD"}
    res2 = requests.get(API_ENDPOINT, headers=headers)
    print(f"    Response Status: {res2.status_code} (Expected: 401 Unauthorized)")

    # Test 3: Path Enumeration Attack
    print("\n[+] Executing Test 3: Reconnaissance & Path Enumeration")
    base_url = API_ENDPOINT.rsplit('/', 1)[0]
    for path in ["/admin", "/config", "/env", "/v1/keys"]:
        res3 = requests.get(f"{base_url}{path}")
        print(f"    Scanning {path} -> Status: {res3.status_code}")

    print("\n=== THREAT SIMULATION COMPLETE ===")

if __name__ == "__main__":
    run_attack_suite()