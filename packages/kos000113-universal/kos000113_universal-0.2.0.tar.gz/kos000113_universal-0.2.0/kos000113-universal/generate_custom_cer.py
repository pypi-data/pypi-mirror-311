from . import generate_key
import socket

def generate_cer_SDTP():
    hostname = socket.gethostname()
    path = f"{hostname}.SDTP_CERTIFICATE"
    hostname = hostname + "\n"
    
    header = "SDTP_CERTIFICATE\n"
    start_marker = "------------------------START_CERTIFICATE------------------------\n"
    end_marker = "\n------------------------END_CERTIFICATE------------------------"
    
    generated_data = generate_key.generate_random_key(2048)
    
    certificate_data = header + hostname + start_marker + generated_data + end_marker 
    certificate_data = certificate_data.encode()  
    
    with open(path, "wb") as certificate_file:
        certificate_file.write(certificate_data)
