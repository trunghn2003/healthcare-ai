import subprocess
import sys
import os

def install_requirements(service_path):
    requirements_path = os.path.join(service_path, "requirements.txt")
    if os.path.exists(requirements_path):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])

def start_service(name, path, port):
    print(f"Starting {name} on port {port}...")
    subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        f"services.{name}.main:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--reload"
    ])

def main():
    # Install requirements for each service
    services = ["ai_service", "patient_service", "gateway", "frontend"]
    for service in services:
        print(f"Installing requirements for {service}...")
        install_requirements(f"services/{service}")

    # Start services
    start_service("ai_service", "services/ai_service", 8001)
    start_service("patient_service", "services/patient_service", 8002)
    start_service("gateway", "services/gateway", 8000)

    # Start Django frontend
    print("Starting frontend on port 8080...")
    subprocess.Popen([
        sys.executable, "services/frontend/manage.py", "runserver",
        "0.0.0.0:8080"
    ])

    print("\nAll services started!")
    print("Access the API documentation at:")
    print("- Gateway: http://localhost:8000/docs")
    print("- AI Service: http://localhost:8001/docs")
    print("- Patient Service: http://localhost:8002/docs")

    # Keep the script running
    try:
        input("Press Enter to stop all services...\n")
    except KeyboardInterrupt:
        print("\nStopping services...")

if __name__ == "__main__":
    main()
