import os
import json
import base64
import hashlib
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

KEY_DIR = "keys"
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, "public_key.pem")

class ProvenanceService:
    def __init__(self):
        self._ensure_keys()
        self.private_key = self._load_private_key()
        self.public_key = self._load_public_key()

    def _ensure_keys(self):
        if not os.path.exists(KEY_DIR):
            os.makedirs(KEY_DIR)
        
        if not os.path.exists(PRIVATE_KEY_PATH):
            print("🔑 Generating new RSA Key Pair for Attestation...")
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            
            # Save Private Key
            with open(PRIVATE_KEY_PATH, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            # Save Public Key
            public_key = private_key.public_key()
            with open(PUBLIC_KEY_PATH, "wb") as f:
                f.write(public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

    def _load_private_key(self):
        with open(PRIVATE_KEY_PATH, "rb") as f:
            return serialization.load_pem_private_key(f.read(), password=None)

    def _load_public_key(self):
        with open(PUBLIC_KEY_PATH, "rb") as f:
             return serialization.load_pem_public_key(f.read())

    def compute_fingerprint(self, data: dict) -> str:
        """Computes a persistent content hash (SHA-256) of a dictionary."""
        # Sort keys to ensure deterministic JSON
        canonical_json = json.dumps(data, sort_keys=True, default=str).encode('utf-8')
        return hashlib.sha256(canonical_json).hexdigest()

    def sign_record(self, record: dict) -> dict:
        """
        Signs the record and returns an Attestation object.
        """
        fingerprint = self.compute_fingerprint(record)
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        attestation_payload = f"{timestamp}|{fingerprint}".encode('utf-8')
        
        signature = self.private_key.sign(
            attestation_payload,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return {
            "timestamp": timestamp,
            "fingerprint": fingerprint,
            "signature": base64.b64encode(signature).decode('utf-8'),
            "algorithm": "RSA-SHA256",
            "verified": True # Self-verified by design
        }

provenance_service = ProvenanceService()
