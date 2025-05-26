import argparse
import numpy as np
import zlib

def text_to_bits(text):
    """Konwertuje tekst na ciąg bitów z kompresją zlib."""
    compressed = zlib.compress(text.encode('utf-8'))
    bits = ''.join(format(byte, '08b') for byte in compressed)
    return bits

def bits_to_bytes(bits):
    """Konwertuje ciąg bitów na bajty, pakując 8 bitów na bajt."""
    padded_bits = bits + '0' * (8 - len(bits) % 8) if len(bits) % 8 != 0 else bits
    bytes_data = bytearray(int(padded_bits[i:i+8], 2) for i in range(0, len(padded_bits), 8))
    return bytes_data

def bytes_to_bits(bytes_data):
    """Konwertuje bajty na ciąg bitów."""
    bits = ''.join(format(byte, '08b') for byte in bytes_data)
    return bits

def bits_to_text(bits):
    """Konwertuje ciąg bitów na tekst z dekodowaniem zlib."""
    padded_bits = bits + '0' * (8 - len(bits) % 8) if len(bits) % 8 != 0 else bits
    bytes_data = bytearray(int(padded_bits[i:i+8], 2) for i in range(0, len(padded_bits), 8))
    try:
        decompressed = zlib.decompress(bytes_data)
        return decompressed.decode('utf-8')
    except zlib.error:
        return "Błąd dekodowania: uszkodzony plik"

def encode_to_binary(text, output_file):
    """Koduje tekst w niskopoziomowym pliku binarnym."""
    bits = text_to_bits(text)
    bytes_data = bits_to_bytes(bits)
    with open(output_file, 'wb') as f:
        f.write(bytes_data)
    print(f"Tekst zakodowany w {output_file}")

def decode_from_binary(input_file):
    """Dekoduje tekst z niskopoziomowego pliku binarnego."""
    with open(input_file, 'rb') as f:
        bytes_data = f.read()
    bits = bytes_to_bits(bytes_data)
    decoded_text = bits_to_text(bits)
    print("Zdekodowany tekst:", decoded_text)
    return decoded_text

def main():
    parser = argparse.ArgumentParser(description="Niskopoziomowe kodowanie i dekodowanie tekstu w pliku binarnym")
    parser.add_argument('-enc', action='store_true', help="Koduj tekst do pliku binarnego")
    parser.add_argument('-dec', action='store_true', help="Dekoduj plik binarny do tekstu")
    parser.add_argument('--input', default='input.txt', help="Plik wejściowy (tekst)")
    parser.add_argument('--output', default='output.bin', help="Plik wyjściowy (binarny)")
    parser.add_argument('--decoded', default='decoded_output.txt', help="Plik wyjściowy (tekst)")
    
    args = parser.parse_args()
    
    if args.enc:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
        encode_to_binary(text, args.output)
    elif args.dec:
        decoded_text = decode_from_binary(args.output)
        with open(args.decoded, 'w', encoding='utf-8') as f:
            f.write(decoded_text)
    else:
        print("Proszę podać -enc lub -dec")

if __name__ == "__main__":
    main()