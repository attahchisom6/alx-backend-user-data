#!/usr/bin/env python3
import bcrypt

def _hash_password(password: str) -> bytes:
    """
    method that converts a stringed password to a hashed bytes
    password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
