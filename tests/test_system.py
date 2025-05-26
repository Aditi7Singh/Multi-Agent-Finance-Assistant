import httpx
import time
from typing import Dict, List

def test_service_health() -> Dict[str, bool]:
    """Test the health endpoints of all services."""
    services = {
        "orchestrator": "http://localhost:8000",
        "api": "http://localhost:8001",
        "scraping": "http://localhost:8002",
        "analysis": "http://localhost:8003",
        "retriever": "http://localhost:8004",
        "voice": "http://localhost:8005",
        "language": "http://localhost:8006"
    }
    
    results = {}
    for service, url in services.items():
        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get(f"{url}/health")
                results[service] = response.status_code == 200
        except Exception as e:
            results[service] = False
            print(f"Error testing {service}: {str(e)}")
    
    return results

def test_market_brief() -> bool:
    """Test the market brief generation pipeline."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                "http://localhost:8000/get_market_brief",
                json={
                    "query": "Give me a brief on tech stocks performance"
                }
            )
            result = response.json()
            return "brief" in result and "audio_url" in result
    except Exception as e:
        print(f"Error testing market brief: {str(e)}")
        return False

def main():
    print("Starting system tests...\n")
    
    # Test 1: Service Health
    print("Test 1: Checking service health...")
    health_results = test_service_health()
    for service, is_healthy in health_results.items():
        status = "✓" if is_healthy else "✗"
        print(f"{status} {service}")
    
    all_healthy = all(health_results.values())
    print(f"\nAll services healthy: {'✓' if all_healthy else '✗'}\n")
    
    # Test 2: Market Brief Generation
    if all_healthy:
        print("Test 2: Testing market brief generation...")
        brief_success = test_market_brief()
        status = "✓" if brief_success else "✗"
        print(f"{status} Market brief generation")
    
    print("\nTest Summary:")
    print(f"Services Health: {'✓' if all_healthy else '✗'}")
    if all_healthy:
        print(f"Market Brief: {'✓' if brief_success else '✗'}")

if __name__ == "__main__":
    main()