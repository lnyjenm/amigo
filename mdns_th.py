# zeroconf_discovery.py

from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import threading
import json

class MyListener(ServiceListener):
    def __init__(self):
        self.services = []  # List to store discovered service information

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            service_info = {
                'name': name,
                'type': type_,
                'address': info.parsed_addresses(),  # Get the service's IP address
                'port': info.port,  # Service port
                'properties': info.properties  # Service properties (e.g., TXT records)
            }
            print(f"Service {name} added, service info: {service_info}")
            self.services.append(service_info)  # Save the service information

def convert_bytes_to_str(services):
    for service in services:
        # Convert byte strings in the properties dictionary
        service['properties'] = {key.decode('utf-8'): value.decode('utf-8') for key, value in service['properties'].items()}
    return services

def discover_services(timeout=20):
    # Initialize Zeroconf and start browsing
    zeroconf = Zeroconf()
    listener = MyListener()
    browser = ServiceBrowser(zeroconf, "_daidm._tcp.local.", listener)

    # Function to stop Zeroconf after a specified time and return service data
    def stop_browser():
        print("Stopping Zeroconf browsing...")
        zeroconf.close()

    # Set a timer to stop the browser after the specified timeout
    timer = threading.Timer(timeout, stop_browser)
    timer.start()

    try:
        print(f"Browsing for services for {timeout} seconds...")
        timer.join()  # Wait until the timer completes
    finally:
        zeroconf.close()

    # Return the services collected
    services_collected = listener.services
    corrected_services = convert_bytes_to_str(services_collected)
    result = corrected_services[0]["properties"]["dcs"]
    print(result)
    return result
