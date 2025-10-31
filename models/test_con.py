import requests
import socket

def test_connection():
    print("Testing network connectivity...")
    
    # Test DNS resolution
    try:
        host_info = socket.getaddrinfo("api.safepath.ai", 443)
        print("✓ DNS resolution successful")
        print(f"Resolved IP addresses: {[info[4][0] for info in host_info]}")
    except Exception as e:
        print(f"✗ DNS resolution failed: {e}")
        return False
    
    # Test HTTPS connection
    try:
        response = requests.get("https://api.safepath.ai", timeout=10)
        print(f"✓ HTTPS connection successful (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"✗ HTTPS connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()