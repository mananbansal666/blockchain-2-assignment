import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

# -----------------------------
# Vehicle Registration Storage
# -----------------------------
vehicles = {}

# -----------------------------
# SHA-256 Hashing
# -----------------------------
def sha256_hash():
    message = input("Enter message to hash: ").strip()
    if not message:
        print("Message cannot be empty.")
        return
    hash_value = hashlib.sha256(message.encode()).hexdigest()
    print("SHA-256 Hash:", hash_value)

# -----------------------------
# Digital Signature
# -----------------------------
def digital_signature():
    message = input("Enter message to sign: ").encode()

    # Generate key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Sign message
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("Message signed successfully.")

    # Verify signature
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature is VALID.")
    except InvalidSignature:
        print("Signature is INVALID.")

# -----------------------------
# Vehicle Registration
# -----------------------------
def register_vehicle():
    number_plate = input("Enter Number Plate: ").upper().strip()

    if not number_plate:
        print("Number plate cannot be empty.")
        return

    if number_plate in vehicles:
        print("Error: Vehicle already registered.")
        return

    owner = input("Enter Owner Name: ").strip()
    model = input("Enter Vehicle Model: ").strip()

    if not owner or not model:
        print("Owner and Model cannot be empty.")
        return

    vehicles[number_plate] = {
        "Owner": owner,
        "Model": model
    }
    print("Vehicle registered successfully.")

def get_vehicle():
    number_plate = input("Enter Number Plate to search: ").upper().strip()

    if number_plate in vehicles:
        vehicle = vehicles[number_plate]
        print("Owner:", vehicle["Owner"])
        print("Model:", vehicle["Model"])
    else:
        print("Error: Vehicle not found.")

# -----------------------------
# Menu Loop
# -----------------------------
def main_menu():
    while True:
        print("\n--- Cryptography & Blockchain App ---")
        print("1. Generate SHA-256 Hash")
        print("2. Digital Signature (Sign & Verify)")
        print("3. Register Vehicle")
        print("4. Retrieve Vehicle Details")
        print("5. Exit")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            sha256_hash()
        elif choice == "2":
            digital_signature()
        elif choice == "3":
            register_vehicle()
        elif choice == "4":
            get_vehicle()
        elif choice == "5":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select 1–5.")

# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    main_menu()
