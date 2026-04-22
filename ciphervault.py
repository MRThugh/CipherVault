

#!/usr/bin/env python3
"""
CipherVault - Advanced Encryption Software
A sophisticated encryption/decryption application built with CustomTkinter
By Ali kamrani -   https://github.com/MRThugh
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import base64
import hashlib
import os
import json
import secrets
import string
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import threading
import time
from datetime import datetime


# ============================================================
# CIPHERVAULT - Advanced Encryption Application
# ============================================================

# Application Constants
APP_NAME = "CipherVault"
APP_VERSION = "2.0"
APP_SUBTITLE = "Advanced Encryption Suite"

# Color Scheme - Cyberpunk/Security Theme
COLORS = {
    "bg_primary": "#0a0e1a",
    "bg_secondary": "#0d1526",
    "bg_card": "#111827",
    "accent_primary": "#00d4ff",
    "accent_secondary": "#7c3aed",
    "accent_green": "#00ff9f",
    "accent_red": "#ff4757",
    "accent_yellow": "#ffd700",
    "text_primary": "#e2e8f0",
    "text_secondary": "#94a3b8",
    "text_muted": "#475569",
    "border": "#1e293b",
    "success": "#10b981",
    "warning": "#f59e0b",
    "error": "#ef4444",
}


class CipherVaultApp(ctk.CTk):
    """Main application class for CipherVault encryption software"""

    def __init__(self):
        super().__init__()

        # Configure application appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Window configuration
        self.title(f"{APP_NAME} v{APP_VERSION} - {APP_SUBTITLE}")
        self.geometry("1200x800")
        self.minsize(900, 650)

        # Set application icon (placeholder for logo/favicon)
        self._setup_icon()

        # Configure dark background
        self.configure(fg_color=COLORS["bg_primary"])

        # Application state variables
        self.encryption_key = None
        self.current_algorithm = tk.StringVar(value="AES-256")
        self.key_strength = tk.StringVar(value="256-bit")
        self.encoding_mode = tk.StringVar(value="Encrypt")
        self.progress_value = tk.DoubleVar(value=0.0)
        self.status_text = tk.StringVar(value="Ready to encrypt...")

        # Initialize UI components
        self._build_interface()

        # Start animated status indicator
        self._start_pulse_animation()

    def _setup_icon(self):
        """
        Setup application icon - Logo and Favicon placeholder
        Replace the icon_data with actual base64 encoded icon data
        """
        try:
            # CipherVault Logo ASCII representation (placeholder)
            # In production, replace with actual .ico file or base64 encoded image
            # self.iconbitmap('ciphervault.ico')  # For .ico file

            # Favicon placeholder - Create a simple icon using tkinter
            icon_canvas = tk.Canvas(width=32, height=32, bg=COLORS["bg_primary"])

            # Draw a simple lock icon shape
            # This represents where your actual logo/favicon would go
            # LOGO PLACEHOLDER: Replace with actual base64 icon data
            # Example: icon_data = base64.b64decode("YOUR_BASE64_ICON_DATA")

            # Set window title with unicode lock symbol as visual indicator
            self.title(f"🔐 {APP_NAME} v{APP_VERSION} - {APP_SUBTITLE}")

        except Exception as e:
            # If icon setup fails, continue without icon
            pass

    def _build_interface(self):
        """Build the main application interface"""

        # ---- HEADER SECTION ----
        self._create_header()

        # ---- MAIN CONTENT AREA ----
        main_container = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=0
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Create left panel (controls) and right panel (output)
        left_panel = ctk.CTkFrame(
            main_container,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right_panel = ctk.CTkFrame(
            main_container,
            fg_color=COLORS["bg_card"],
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"],
        )
        right_panel.pack(side="right", fill="both", expand=True, padx=(8, 0))

        # Build panels
        self._create_input_panel(left_panel)
        self._create_output_panel(right_panel)

        # ---- BOTTOM STATUS BAR ----
        self._create_status_bar()

    def _create_header(self):
        """Create the application header with logo area and navigation"""

        header = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_secondary"],
            corner_radius=0,
            height=80,
            border_width=0,
        )
        header.pack(fill="x", padx=0, pady=(0, 15))
        header.pack_propagate(False)

        # Logo section
        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(side="left", padx=25, pady=10)

        # LOGO PLACEHOLDER - Replace with actual image widget
        # logo_image = ctk.CTkImage(Image.open("ciphervault_logo.png"), size=(50, 50))
        # logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
        # logo_label.pack(side="left")

        # Logo icon placeholder (unicode representation)
        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="🔐",
            font=ctk.CTkFont(size=36),
            text_color=COLORS["accent_primary"],
        )
        logo_icon.pack(side="left", padx=(0, 10))

        # App name and subtitle
        name_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        name_frame.pack(side="left")

        app_name_label = ctk.CTkLabel(
            name_frame,
            text=APP_NAME,
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"),
            text_color=COLORS["accent_primary"],
        )
        app_name_label.pack(anchor="w")

        subtitle_label = ctk.CTkLabel(
            name_frame,
            text=APP_SUBTITLE,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_secondary"],
        )
        subtitle_label.pack(anchor="w")

        # Right side controls
        controls_frame = ctk.CTkFrame(header, fg_color="transparent")
        controls_frame.pack(side="right", padx=25, pady=10)

        # Algorithm selector
        algo_label = ctk.CTkLabel(
            controls_frame,
            text="ALGORITHM",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["text_muted"],
        )
        algo_label.pack(anchor="w")

        algo_menu = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.current_algorithm,
            values=["AES-256", "Fernet (AES-128)", "XOR Custom", "ROT-47", "Base64"],
            fg_color=COLORS["bg_card"],
            button_color=COLORS["accent_secondary"],
            button_hover_color=COLORS["accent_primary"],
            text_color=COLORS["text_primary"],
            font=ctk.CTkFont(size=12, weight="bold"),
            width=180,
            command=self._on_algorithm_change,
        )
        algo_menu.pack()

        # Mode toggle
        mode_frame = ctk.CTkFrame(header, fg_color="transparent")
        mode_frame.pack(side="right", padx=15, pady=10)

        mode_label = ctk.CTkLabel(
            mode_frame,
            text="MODE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["text_muted"],
        )
        mode_label.pack(anchor="w")

        mode_segment = ctk.CTkSegmentedButton(
            mode_frame,
            values=["Encrypt", "Decrypt"],
            variable=self.encoding_mode,
            fg_color=COLORS["bg_card"],
            selected_color=COLORS["accent_primary"],
            selected_hover_color=COLORS["accent_secondary"],
            unselected_color=COLORS["bg_card"],
            unselected_hover_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_mode_change,
        )
        mode_segment.pack()

    def _create_input_panel(self, parent):
        """Create the input panel with text area and encryption controls"""

        # Panel header
        panel_header = ctk.CTkFrame(parent, fg_color="transparent")
        panel_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            panel_header,
            text="INPUT",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["accent_primary"],
        ).pack(side="left")

        # Character counter
        self.char_count_label = ctk.CTkLabel(
            panel_header,
            text="0 chars",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_muted"],
        )
        self.char_count_label.pack(side="right")

        # Input text area
        self.input_text = ctk.CTkTextbox(
            parent,
            fg_color=COLORS["bg_secondary"],
            text_color=COLORS["text_primary"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=8,
            font=ctk.CTkFont(family="Courier", size=12),
            scrollbar_button_color=COLORS["accent_secondary"],
        )
        self.input_text.pack(fill="both", expand=True, padx=15, pady=(5, 10))
        self.input_text.bind("<KeyRelease>", self._update_char_count)

        # Placeholder text
        self.input_text.insert("1.0", "Enter text to encrypt or decrypt here...")
        self.input_text.bind("<FocusIn>", self._clear_placeholder)

        # ---- KEY MANAGEMENT SECTION ----
        key_section = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_secondary"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"],
        )
        key_section.pack(fill="x", padx=15, pady=(0, 10))

        key_header = ctk.CTkFrame(key_section, fg_color="transparent")
        key_header.pack(fill="x", padx=12, pady=(10, 5))

        ctk.CTkLabel(
            key_header,
            text="🔑 ENCRYPTION KEY",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["accent_yellow"],
        ).pack(side="left")

        # Key strength indicator
        self.key_strength_label = ctk.CTkLabel(
            key_header,
            text="● STRONG",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["accent_green"],
        )
        self.key_strength_label.pack(side="right")

        # Key input field
        key_input_frame = ctk.CTkFrame(key_section, fg_color="transparent")
        key_input_frame.pack(fill="x", padx=12, pady=(0, 8))

        self.key_entry = ctk.CTkEntry(
            key_input_frame,
            placeholder_text="Enter encryption key or generate one...",
            fg_color=COLORS["bg_primary"],
            border_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            placeholder_text_color=COLORS["text_muted"],
            show="●",
            font=ctk.CTkFont(family="Courier", size=12),
            height=38,
        )
        self.key_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.key_entry.bind("<KeyRelease>", self._analyze_key_strength)

        # Toggle key visibility
        self.key_visible = False
        toggle_btn = ctk.CTkButton(
            key_input_frame,
            text="👁",
            width=38,
            height=38,
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["border"],
            corner_radius=8,
            command=self._toggle_key_visibility,
        )
        toggle_btn.pack(side="right")

        # Key action buttons
        key_actions = ctk.CTkFrame(key_section, fg_color="transparent")
        key_actions.pack(fill="x", padx=12, pady=(0, 10))

        ctk.CTkButton(
            key_actions,
            text="⚡ Generate Key",
            fg_color=COLORS["accent_secondary"],
            hover_color="#6d28d9",
            text_color="white",
            font=ctk.CTkFont(size=11, weight="bold"),
            height=32,
            corner_radius=6,
            command=self._generate_random_key,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            key_actions,
            text="📋 Copy Key",
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["border"],
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont(size=11),
            height=32,
            corner_radius=6,
            command=self._copy_key,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            key_actions,
            text="🗑 Clear",
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["accent_red"],
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont(size=11),
            height=32,
            corner_radius=6,
            command=self._clear_key,
        ).pack(side="left")

        # ---- ACTION BUTTONS ----
        action_frame = ctk.CTkFrame(parent, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=(5, 15))

        # Main encrypt/decrypt button
        self.main_action_btn = ctk.CTkButton(
            action_frame,
            text="🔒 ENCRYPT",
            fg_color=COLORS["accent_primary"],
            hover_color=COLORS["accent_secondary"],
            text_color=COLORS["bg_primary"],
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            command=self._process_encryption,
        )
        self.main_action_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        # File operations
        file_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        file_frame.pack(side="right")

        ctk.CTkButton(
            file_frame,
            text="📂",
            width=45,
            height=45,
            fg_color=COLORS["bg_secondary"],
            hover_color=COLORS["border"],
            corner_radius=10,
            command=self._load_file,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            file_frame,
            text="💾",
            width=45,
            height=45,
            fg_color=COLORS["bg_secondary"],
            hover_color=COLORS["border"],
            corner_radius=10,
            command=self._save_file,
        ).pack(side="left")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            parent,
            variable=self.progress_value,
            fg_color=COLORS["bg_secondary"],
            progress_color=COLORS["accent_primary"],
            height=4,
            corner_radius=2,
        )
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 10))

    def _create_output_panel(self, parent):
        """Create the output panel with encrypted/decrypted result display"""

        # Panel header
        panel_header = ctk.CTkFrame(parent, fg_color="transparent")
        panel_header.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            panel_header,
            text="OUTPUT",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["accent_green"],
        ).pack(side="left")

        # Output actions
        output_actions = ctk.CTkFrame(panel_header, fg_color="transparent")
        output_actions.pack(side="right")

        ctk.CTkButton(
            output_actions,
            text="📋 Copy",
            width=70,
            height=26,
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["accent_primary"],
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont(size=10),
            corner_radius=6,
            command=self._copy_output,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            output_actions,
            text="🔄 Swap",
            width=70,
            height=26,
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["accent_secondary"],
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont(size=10),
            corner_radius=6,
            command=self._swap_io,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            output_actions,
            text="🗑 Clear",
            width=60,
            height=26,
            fg_color=COLORS["bg_card"],
            hover_color=COLORS["accent_red"],
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont(size=10),
            corner_radius=6,
            command=self._clear_output,
        ).pack(side="left")

        # Output text area
        self.output_text = ctk.CTkTextbox(
            parent,
            fg_color=COLORS["bg_secondary"],
            text_color=COLORS["accent_green"],
            border_color=COLORS["border"],
            border_width=1,
            corner_radius=8,
            font=ctk.CTkFont(family="Courier", size=12),
            scrollbar_button_color=COLORS["accent_secondary"],
            state="disabled",
        )
        self.output_text.pack(fill="both", expand=True, padx=15, pady=(5, 10))

        # ---- ENCRYPTION INFO PANEL ----
        info_section = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_secondary"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"],
        )
        info_section.pack(fill="x", padx=15, pady=(0, 10))

        info_header = ctk.CTkLabel(
            info_section,
            text="📊 ENCRYPTION DETAILS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["text_secondary"],
        )
        info_header.pack(anchor="w", padx=12, pady=(10, 5))

        # Info grid
        info_grid = ctk.CTkFrame(info_section, fg_color="transparent")
        info_grid.pack(fill="x", padx=12, pady=(0, 10))

        # Create info labels
        self.info_labels = {}
        info_items = [
            ("Algorithm", "AES-256-CBC", "algo_value"),
            ("Key Size", "256 bits", "key_size_value"),
            ("Input Size", "0 bytes", "input_size_value"),
            ("Output Size", "0 bytes", "output_size_value"),
            ("Process Time", "0.00 ms", "time_value"),
            ("Security Level", "MILITARY GRADE", "security_value"),
        ]

        for i, (label, value, key) in enumerate(info_items):
            row = i // 2
            col = (i % 2) * 2

            ctk.CTkLabel(
                info_grid,
                text=f"{label}:",
                font=ctk.CTkFont(size=10),
                text_color=COLORS["text_muted"],
            ).grid(row=row, column=col, sticky="w", padx=(0, 5), pady=2)

            self.info_labels[key] = ctk.CTkLabel(
                info_grid,
                text=value,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=COLORS["accent_primary"],
            )
            self.info_labels[key].grid(row=row, column=col + 1, sticky="w", padx=(0, 20), pady=2)

        # ---- HASH VERIFICATION SECTION ----
        hash_section = ctk.CTkFrame(
            parent,
            fg_color=COLORS["bg_secondary"],
            corner_radius=8,
            border_width=1,
            border_color=COLORS["border"],
        )
        hash_section.pack(fill="x", padx=15, pady=(0, 15))

        hash_header = ctk.CTkFrame(hash_section, fg_color="transparent")
        hash_header.pack(fill="x", padx=12, pady=(8, 0))

        ctk.CTkLabel(
            hash_header,
            text="🔏 HASH VERIFICATION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=COLORS["text_secondary"],
        ).pack(side="left")

        ctk.CTkButton(
            hash_header,
            text="Generate Hash",
            width=100,
            height=24,
            fg_color=COLORS["accent_secondary"],
            hover_color="#6d28d9",
            text_color="white",
            font=ctk.CTkFont(size=9),
            corner_radius=5,
            command=self._generate_hash,
        ).pack(side="right")

        self.hash_display = ctk.CTkLabel(
            hash_section,
            text="SHA-256: Click 'Generate Hash' to compute",
            font=ctk.CTkFont(family="Courier", size=9),
            text_color=COLORS["text_muted"],
            wraplength=400,
        )
        self.hash_display.pack(anchor="w", padx=12, pady=(4, 10))

    def _create_status_bar(self):
        """Create the bottom status bar"""

        status_bar = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_secondary"],
            corner_radius=0,
            height=35,
        )
        status_bar.pack(fill="x", side="bottom", padx=0, pady=0)
        status_bar.pack_propagate(False)

        # Status indicator
        self.status_indicator = ctk.CTkLabel(
            status_bar,
            text="●",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["accent_green"],
        )
        self.status_indicator.pack(side="left", padx=(15, 5), pady=5)

        # Status text
        ctk.CTkLabel(
            status_bar,
            textvariable=self.status_text,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["text_secondary"],
        ).pack(side="left", padx=5, pady=5)

        # Right side info
        right_status = ctk.CTkFrame(status_bar, fg_color="transparent")
        right_status.pack(side="right", padx=15, pady=5)

        # Current time
        self.time_label = ctk.CTkLabel(
            right_status,
            text="",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_muted"],
        )
        self.time_label.pack(side="right", padx=10)
        self._update_time()

        ctk.CTkLabel(
            right_status,
            text=f"{APP_NAME} v{APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color=COLORS["text_muted"],
        ).pack(side="right")

    # ============================================================
    # ENCRYPTION ALGORITHMS
    # ============================================================

    def _encrypt_aes256(self, text: str, key: str) -> str:
        """Encrypt text using AES-256-CBC algorithm"""
        # Derive 256-bit key using PBKDF2
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        derived_key = kdf.derive(key.encode())

        # Generate random IV
        iv = os.urandom(16)

        # Create cipher
        cipher = Cipher(
            algorithms.AES(derived_key),
            modes.CBC(iv),
            backend=default_backend(),
        )
        encryptor = cipher.encryptor()

        # Pad plaintext
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(text.encode()) + padder.finalize()

        # Encrypt
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Combine salt + iv + ciphertext and encode to base64
        combined = salt + iv + ciphertext
        return base64.b64encode(combined).decode()

    def _decrypt_aes256(self, encrypted_text: str, key: str) -> str:
        """Decrypt AES-256-CBC encrypted text"""
        try:
            # Decode from base64
            combined = base64.b64decode(encrypted_text)

            # Extract components
            salt = combined[:16]
            iv = combined[16:32]
            ciphertext = combined[32:]

            # Derive key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend(),
            )
            derived_key = kdf.derive(key.encode())

            # Create cipher
            cipher = Cipher(
                algorithms.AES(derived_key),
                modes.CBC(iv),
                backend=default_backend(),
            )
            decryptor = cipher.decryptor()

            # Decrypt and unpad
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

            return plaintext.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def _encrypt_fernet(self, text: str, key: str) -> str:
        """Encrypt using Fernet (AES-128 with authentication)"""
        # Derive Fernet-compatible key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'ciphervault_salt',  # Static salt for Fernet compatibility
            iterations=100000,
            backend=default_backend(),
        )
        fernet_key = base64.urlsafe_b64encode(kdf.derive(key.encode()))
        f = Fernet(fernet_key)
        return f.encrypt(text.encode()).decode()

    def _decrypt_fernet(self, encrypted_text: str, key: str) -> str:
        """Decrypt Fernet encrypted text"""
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'ciphervault_salt',
                iterations=100000,
                backend=default_backend(),
            )
            fernet_key = base64.urlsafe_b64encode(kdf.derive(key.encode()))
            f = Fernet(fernet_key)
            return f.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            raise ValueError(f"Fernet decryption failed: {str(e)}")

    def _encrypt_xor(self, text: str, key: str) -> str:
        """Encrypt using XOR cipher with key repetition"""
        if not key:
            raise ValueError("Key cannot be empty for XOR encryption")

        key_bytes = key.encode()
        text_bytes = text.encode()
        encrypted = bytearray()

        for i, byte in enumerate(text_bytes):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])

        return base64.b64encode(bytes(encrypted)).decode()

    def _decrypt_xor(self, encrypted_text: str, key: str) -> str:
        """Decrypt XOR encrypted text"""
        if not key:
            raise ValueError("Key cannot be empty for XOR decryption")

        try:
            encrypted_bytes = base64.b64decode(encrypted_text)
            key_bytes = key.encode()
            decrypted = bytearray()

            for i, byte in enumerate(encrypted_bytes):
                decrypted.append(byte ^ key_bytes[i % len(key_bytes)])

            return bytes(decrypted).decode()
        except Exception as e:
            raise ValueError(f"XOR decryption failed: {str(e)}")

    def _encrypt_rot47(self, text: str, key: str = "") -> str:
        """Apply ROT-47 transformation"""
        result = []
        for char in text:
            if 33 <= ord(char) <= 126:
                result.append(chr(33 + ((ord(char) - 33 + 47) % 94)))
            else:
                result.append(char)
        return ''.join(result)

    def _decrypt_rot47(self, text: str, key: str = "") -> str:
        """ROT-47 is its own inverse"""
        return self._encrypt_rot47(text)

    def _encrypt_base64(self, text: str, key: str = "") -> str:
        """Encode text to Base64"""
        return base64.b64encode(text.encode()).decode()

    def _decrypt_base64(self, text: str, key: str = "") -> str:
        """Decode Base64 text"""
        try:
            return base64.b64decode(text).decode()
        except Exception as e:
            raise ValueError(f"Invalid Base64 data: {str(e)}")

    # ============================================================
    # MAIN PROCESSING FUNCTION
    # ============================================================

    def _process_encryption(self):
        """Main encryption/decryption processing function"""
        input_text = self.input_text.get("1.0", "end-1c")
        key = self.key_entry.get()
        mode = self.encoding_mode.get()
        algorithm = self.current_algorithm.get()

        # Validation
        if not input_text or input_text == "Enter text to encrypt or decrypt here...":
            self._show_status("⚠️ Please enter text to process", COLORS["accent_yellow"])
            return

        if not key and algorithm not in ["ROT-47", "Base64"]:
            self._show_status("⚠️ Please enter an encryption key", COLORS["accent_yellow"])
            return

        # Start processing in thread
        threading.Thread(
            target=self._run_encryption_thread,
            args=(input_text, key, mode, algorithm),
            daemon=True,
        ).start()

    def _run_encryption_thread(self, text: str, key: str, mode: str, algorithm: str):
        """Run encryption in a separate thread to prevent UI freezing"""
        try:
            # Update UI - processing
            self.after(0, lambda: self._show_status("⚙️ Processing...", COLORS["accent_primary"]))
            self.after(0, lambda: self.progress_value.set(0.1))

            start_time = time.time()

            # Simulate progress for UX
            for i in range(1, 9):
                time.sleep(0.05)
                self.after(0, lambda v=i * 0.1: self.progress_value.set(v))

            # Select algorithm and process
            result = ""
            if algorithm == "AES-256":
                if mode == "Encrypt":
                    result = self._encrypt_aes256(text, key)
                else:
                    result = self._decrypt_aes256(text, key)

            elif algorithm == "Fernet (AES-128)":
                if mode == "Encrypt":
                    result = self._encrypt_fernet(text, key)
                else:
                    result = self._decrypt_fernet(text, key)

            elif algorithm == "XOR Custom":
                if mode == "Encrypt":
                    result = self._encrypt_xor(text, key)
                else:
                    result = self._decrypt_xor(text, key)

            elif algorithm == "ROT-47":
                if mode == "Encrypt":
                    result = self._encrypt_rot47(text, key)
                else:
                    result = self._decrypt_rot47(text, key)

            elif algorithm == "Base64":
                if mode == "Encrypt":
                    result = self._encrypt_base64(text, key)
                else:
                    result = self._decrypt_base64(text, key)

            # Calculate processing time
            process_time = (time.time() - start_time) * 1000

            # Update UI with results
            self.after(0, lambda: self._display_result(result, text, process_time, algorithm, mode))
            self.after(0, lambda: self.progress_value.set(1.0))
            self.after(500, lambda: self.progress_value.set(0.0))

        except Exception as e:
            self.after(0, lambda: self._show_error(str(e)))
            self.after(0, lambda: self.progress_value.set(0.0))

    def _display_result(self, result: str, original: str, process_time: float, algorithm: str, mode: str):
        """Display the encryption/decryption result in the output panel"""

        # Enable and update output textbox
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", result)
        self.output_text.configure(state="disabled")

        # Update info labels
        self.info_labels["algo_value"].configure(text=algorithm)
        self.info_labels["key_size_value"].configure(
            text="256 bits" if "AES" in algorithm else "Variable"
        )
        self.info_labels["input_size_value"].configure(text=f"{len(original.encode())} bytes")
        self.info_labels["output_size_value"].configure(text=f"{len(result.encode())} bytes")
        self.info_labels["time_value"].configure(text=f"{process_time:.2f} ms")

        security_level = {
            "AES-256": "MILITARY GRADE",
            "Fernet (AES-128)": "HIGH SECURITY",
            "XOR Custom": "BASIC",
            "ROT-47": "DISPLAY ONLY",
            "Base64": "ENCODING ONLY",
        }
        self.info_labels["security_value"].configure(
            text=security_level.get(algorithm, "UNKNOWN")
        )

        # Show success status
        icon = "🔒" if mode == "Encrypt" else "🔓"
        self._show_status(
            f"{icon} {mode}ion complete! Processed {len(original.encode())} bytes → {len(result.encode())} bytes",
            COLORS["accent_green"],
        )

    def _show_error(self, error_msg: str):
        """Display error message in status bar"""
        self._show_status(f"❌ Error: {error_msg}", COLORS["accent_red"])
        messagebox.showerror("CipherVault Error", error_msg)

    def _show_status(self, message: str, color: str = None):
        """Update status bar with message"""
        self.status_text.set(message)

    # ============================================================
    # KEY MANAGEMENT
    # ============================================================

    def _generate_random_key(self):
        """Generate a cryptographically secure random key"""
        # Generate a strong random key
        characters = string.ascii_letters + string.digits + string.punctuation
        key_length = 32  # 256-bit equivalent

        # Use secrets module for cryptographically secure generation
        random_key = ''.join(secrets.choice(characters) for _ in range(key_length))

        # Update key entry
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, random_key)

        self._analyze_key_strength()
        self._show_status("⚡ Secure random key generated!", COLORS["accent_green"])

    def _analyze_key_strength(self, event=None):
        """Analyze and display key strength"""
        key = self.key_entry.get()

        if len(key) == 0:
            strength = "EMPTY"
            color = COLORS["accent_red"]
        elif len(key) < 8:
            strength = "WEAK"
            color = COLORS["accent_red"]
        elif len(key) < 16:
            strength = "MODERATE"
            color = COLORS["accent_yellow"]
        elif len(key) < 24:
            strength = "GOOD"
            color = COLORS["accent_primary"]
        else:
            # Check for character variety
            has_upper = any(c.isupper() for c in key)
            has_lower = any(c.islower() for c in key)
            has_digit = any(c.isdigit() for c in key)
            has_special = any(not c.isalnum() for c in key)

            variety_score = sum([has_upper, has_lower, has_digit, has_special])

            if variety_score >= 3:
                strength = "STRONG"
                color = COLORS["accent_green"]
            else:
                strength = "GOOD"
                color = COLORS["accent_primary"]

        self.key_strength_label.configure(text=f"● {strength}", text_color=color)

    def _toggle_key_visibility(self):
        """Toggle key visibility in entry field"""
        if self.key_visible:
            self.key_entry.configure(show="●")
            self.key_visible = False
        else:
            self.key_entry.configure(show="")
            self.key_visible = True

    def _copy_key(self):
        """Copy key to clipboard"""
        key = self.key_entry.get()
        if key:
            self.clipboard_clear()
            self.clipboard_append(key)
            self._show_status("📋 Key copied to clipboard", COLORS["accent_primary"])
        else:
            self._show_status("⚠️ No key to copy", COLORS["accent_yellow"])

    def _clear_key(self):
        """Clear the key entry field"""
        self.key_entry.delete(0, "end")
        self.key_strength_label.configure(text="● EMPTY", text_color=COLORS["accent_red"])
        self._show_status("🗑 Key cleared", COLORS["text_secondary"])

    # ============================================================
    # UI HELPER FUNCTIONS
    # ============================================================

    def _update_char_count(self, event=None):
        """Update character count in input panel"""
        text = self.input_text.get("1.0", "end-1c")
        if text != "Enter text to encrypt or decrypt here...":
            char_count = len(text)
            byte_count = len(text.encode())
            self.char_count_label.configure(
                text=f"{char_count} chars | {byte_count} bytes"
            )

    def _clear_placeholder(self, event=None):
        """Clear placeholder text when input gets focus"""
        current_text = self.input_text.get("1.0", "end-1c")
        if current_text == "Enter text to encrypt or decrypt here...":
            self.input_text.delete("1.0", "end")

    def _on_algorithm_change(self, choice: str):
        """Handle algorithm selection change"""
        self._show_status(f"Algorithm changed to: {choice}", COLORS["accent_primary"])

        # Update info display
        security_levels = {
            "AES-256": ("256 bits", "MILITARY GRADE", COLORS["accent_green"]),
            "Fernet (AES-128)": ("128 bits", "HIGH SECURITY", COLORS["accent_primary"]),
            "XOR Custom": ("Variable", "BASIC", COLORS["accent_yellow"]),
            "ROT-47": ("N/A", "DISPLAY ONLY", COLORS["text_muted"]),
            "Base64": ("N/A", "ENCODING ONLY", COLORS["text_muted"]),
        }

        if choice in security_levels:
            key_size, security, color = security_levels[choice]
            self.info_labels["key_size_value"].configure(text=key_size)
            self.info_labels["security_value"].configure(text=security, text_color=color)

    def _on_mode_change(self, mode: str):
        """Handle mode change between Encrypt and Decrypt"""
        if mode == "Encrypt":
            self.main_action_btn.configure(
                text="🔒 ENCRYPT",
                fg_color=COLORS["accent_primary"],
            )
            self.output_text.configure(text_color=COLORS["accent_green"])
        else:
            self.main_action_btn.configure(
                text="🔓 DECRYPT",
                fg_color=COLORS["accent_secondary"],
            )
            self.output_text.configure(text_color=COLORS["accent_primary"])

        self._show_status(f"Mode: {mode}", COLORS["text_secondary"])

    def _copy_output(self):
        """Copy output text to clipboard"""
        self.output_text.configure(state="normal")
        output = self.output_text.get("1.0", "end-1c")
        self.output_text.configure(state="disabled")

        if output:
            self.clipboard_clear()
            self.clipboard_append(output)
            self._show_status("📋 Output copied to clipboard", COLORS["accent_green"])
        else:
            self._show_status("⚠️ No output to copy", COLORS["accent_yellow"])

    def _swap_io(self):
        """Swap input and output text"""
        input_text = self.input_text.get("1.0", "end-1c")

        self.output_text.configure(state="normal")
        output_text = self.output_text.get("1.0", "end-1c")
        self.output_text.configure(state="disabled")

        if output_text:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", output_text)

            self.output_text.configure(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", input_text)
            self.output_text.configure(state="disabled")

            self._show_status("🔄 Input and output swapped", COLORS["accent_primary"])

    def _clear_output(self):
        """Clear the output text area"""
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        self._show_status("🗑 Output cleared", COLORS["text_secondary"])

    def _load_file(self):
        """Load text from a file"""
        file_path = filedialog.askopenfilename(
            title="Open File - CipherVault",
            filetypes=[
                ("Text files", "*.txt"),
                ("Encrypted files", "*.enc"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                self.input_text.delete("1.0", "end")
                self.input_text.insert("1.0", content)
                self._update_char_count()
                self._show_status(f"📂 File loaded: {os.path.basename(file_path)}", COLORS["accent_green"])

            except Exception as e:
                self._show_error(f"Could not load file: {str(e)}")

    def _save_file(self):
        """Save output text to a file"""
        self.output_text.configure(state="normal")
        output = self.output_text.get("1.0", "end-1c")
        self.output_text.configure(state="disabled")

        if not output:
            self._show_status("⚠️ No output to save", COLORS["accent_yellow"])
            return

        file_path = filedialog.asksaveasfilename(
            title="Save File - CipherVault",
            defaultextension=".enc",
            filetypes=[
                ("Encrypted files", "*.enc"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(output)

                self._show_status(f"💾 File saved: {os.path.basename(file_path)}", COLORS["accent_green"])

            except Exception as e:
                self._show_error(f"Could not save file: {str(e)}")

    def _generate_hash(self):
        """Generate SHA-256 hash of the input text"""
        input_text = self.input_text.get("1.0", "end-1c")

        if not input_text or input_text == "Enter text to encrypt or decrypt here...":
            self._show_status("⚠️ Enter text to generate hash", COLORS["accent_yellow"])
            return

        hash_sha256 = hashlib.sha256(input_text.encode()).hexdigest()
        hash_md5 = hashlib.md5(input_text.encode()).hexdigest()

        self.hash_display.configure(
            text=f"SHA-256: {hash_sha256}\nMD5: {hash_md5}",
            text_color=COLORS["accent_primary"],
        )
        self._show_status("🔏 Hash generated", COLORS["accent_green"])

    def _update_time(self):
        """Update the time display in status bar"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=f"⏱ {current_time}")
        self.after(1000, self._update_time)

    def _start_pulse_animation(self):
        """Start the pulsing animation for status indicator"""
        self._pulse_status(True)

    def _pulse_status(self, bright: bool):
        """Animate the status indicator"""
        color = COLORS["accent_green"] if bright else COLORS["bg_secondary"]
        try:
            self.status_indicator.configure(text_color=color)
            self.after(1000, lambda: self._pulse_status(not bright))
        except:
            pass


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():
    """Main entry point for CipherVault application"""
    try:
        # Check for required library
        import customtkinter
        from cryptography.fernet import Fernet # type: ignore
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Please install requirements: pip install customtkinter cryptography")
        return

    # Create and run the application
    app = CipherVaultApp()
    app.mainloop()


if __name__ == "__main__":
    main()
