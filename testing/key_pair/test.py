from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_key_pairs(count=20):
    for i in range(1, count + 1):
        # Tạo private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Serialize private key (PEM format)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Tạo public key từ private key
        public_key = private_key.public_key()
        
        # Serialize public key (PEM format)
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Lưu ra file (hoặc tùy bạn muốn)
        with open(f"private_key_{i}.pem", "wb") as priv_file:
            priv_file.write(private_pem)
        
        with open(f"public_key_{i}.pem", "wb") as pub_file:
            pub_file.write(public_pem)
        
        print(f"Cặp key {i} đã tạo xong!")

if __name__ == "__main__":
    generate_key_pairs()
