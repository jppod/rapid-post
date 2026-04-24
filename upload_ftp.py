import ftplib
import os

# Configuración del servidor FTP
FTP_HOSTS = ["ftpupload.net", "anaconews.free.nf"]
FTP_USER = "if0_41704527".strip()
FTP_PASS = "bGjoKjNwiGJ".strip()
# En InfinityFree/hosting gratuito, la carpeta pública suele ser htdocs
REMOTE_ROOT = "htdocs" 

def upload_directory(ftp, local_dir, remote_dir):
    try:
        ftp.mkd(remote_dir)
        print(f"Directorio creado: {remote_dir}")
    except ftplib.error_perm:
        # El directorio ya existe
        pass

    for item in os.listdir(local_dir):
        # Evitar subir archivos innecesarios
        if item in ['.git', '.DS_Store', 'node_modules', 'package.json', 'upload_ftp.py']:
            continue
            
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"

        if os.path.isfile(local_path):
            with open(local_path, "rb") as file:
                print(f"Subiendo: {item} -> {remote_path}")
                ftp.storbinary(f"STOR {remote_path}", file)
        elif os.path.isdir(local_path):
            upload_directory(ftp, local_path, remote_path)

def main():
    for host in FTP_HOSTS:
        print(f"\n--- Intentando con host: {host} ---")
        print(f"Conectando (usando TLS/SSL)...")
        try:
            ftp = ftplib.FTP_TLS(host)
            ftp.connect()
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            ftp.prot_p()
            ftp.set_pasv(True)
            print(f"Conexión segura exitosa en {host}. Iniciando subida...")
            upload_directory(ftp, ".", REMOTE_ROOT)
            ftp.quit()
            print("\n¡Éxito! Todos los archivos han sido cargados.")
            return # Salir si tuvo éxito
        except Exception as e:
            print(f"Fallo con TLS: {e}")
            print(f"Intentando conexión estándar en {host}...")
            try:
                ftp = ftplib.FTP(host)
                ftp.login(user=FTP_USER, passwd=FTP_PASS)
                ftp.set_pasv(True)
                print(f"Conexión estándar exitosa en {host}. Iniciando subida...")
                upload_directory(ftp, ".", REMOTE_ROOT)
                ftp.quit()
                print("\n¡Éxito! Todos los archivos han sido cargados.")
                return # Salir si tuvo éxito
            except Exception as e2:
                print(f"Error final en {host}: {e2}")

    print("\nNo se pudo conectar a ninguno de los hosts.")
    print("IMPORTANTE: Si acabas de crear la cuenta, puede tardar hasta 72 horas en activarse el FTP.")

if __name__ == "__main__":
    main()
