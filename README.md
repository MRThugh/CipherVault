<div align="center">

# 🔐 CipherVault
**Advanced Encryption Suite**

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-darkgreen.svg?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![Cryptography](https://img.shields.io/badge/Security-Cryptography-red.svg?style=for-the-badge)](https://cryptography.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

<p align="center">
  A sophisticated, cyberpunk-themed desktop application for secure text and file encryption, featuring military-grade algorithms and advanced key management.
</p>

[**Report Bug**](https://github.com/MRThugh/CipherVault/issues) · [**Request Feature**](https://github.com/MRThugh/CipherVault/issues)

</div>

---

## ✨ Features

- **🛡️ Multi-Algorithm Support**: 
  - `AES-256 (CBC)` (Military Grade)
  - `Fernet (AES-128)` (High Security)
  - `XOR Custom` (Basic/Educational)
  - `ROT-47` & `Base64` (Encoding/Display)
- **🔑 Advanced Key Management**: Generate cryptographically secure random keys, analyze key strength in real-time, and securely toggle visibility.
- **📁 File Operations**: Easily load text/encrypted files directly into the vault and save your outputs seamlessly.
- **🔏 Hash Verification**: Built-in SHA-256 and MD5 hash generation for data integrity checking.
- **⚡ Threaded Processing**: Heavy encryption tasks run on background threads, ensuring the UI remains buttery smooth.
- **🎨 Cyberpunk UI**: A stunning, dark-themed interface built with `CustomTkinter` featuring pulse animations and real-time statistics.

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.8 or higher installed. You will also need the following Python libraries:

```bash
pip install customtkinter cryptography

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MRThugh/CipherVault.git
   ```
2. Navigate to the project directory:
   ```bash
   cd CipherVault
   ```
3. Run the application:
   ```bash
   python ciphervault.py
   ```

## 💻 Usage

1. **Select Algorithm**: Choose your desired encryption standard from the top-right dropdown (e.g., AES-256).
2. **Set Mode**: Toggle between `Encrypt` and `Decrypt`.
3. **Input Data**: Type your text or use the 📂 button to load a file.
4. **Provide a Key**: Enter your secret key or click `⚡ Generate Key` for a secure random one.
5. **Execute**: Click the main `🔒 ENCRYPT` or `🔓 DECRYPT` button.
6. **Save/Copy**: Copy the output to your clipboard or save it directly to a `.enc` file using the 💾 button.

## 📸 Screenshots

> 
> *<div align="center"><img src="https://via.placeholder.com/800x450.png?text=Add+Screenshot+Here" alt="CipherVault Screenshot"></div>*

## 🛠️ Tech Stack

- **[Python 3](https://www.python.org/)** - Core logic
- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** - Modern UI framework
- **[Cryptography](https://cryptography.io/en/latest/)** - Industry-standard cryptographic recipes and primitives (PBKDF2HMAC, AES-CBC, PKCS7)

## 🔒 Security Disclaimer

While CipherVault implements industry-standard algorithms (like AES-256), this software is provided "as is". Always keep your encryption keys safe. Lost keys cannot be recovered, and data encrypted with lost keys will be permanently inaccessible. 

## 👨‍💻 Author

**MRThugh**
- GitHub: [@MRThugh](https://github.com/MRThugh)

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<div align="center">
  <i>Built with ❤️ and Python</i>
</div>
