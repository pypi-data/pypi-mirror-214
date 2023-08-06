from .builder import FILE_TRANSFORMERS
import tarfile
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pyAesCrypt
import hashlib
import binascii
import tempfile
from glob import glob
import os
import sys
sys.path.insert(0, os.path.join(".."))
from cetl import Base, transform_wrapper, context_name

def get_fernet_key(fernet_key_file):
    with open(fernet_key_file, "r") as f:
        # fernet_key = f.read().strip()
        fernet_key = f.read()
        # return fernet_key.encode('utf-8')
        return fernet_key

def get_hash_string(filepath):
    # Read the hash bytes from a binary file
    with open(filepath, 'rb') as f:
        hash_bytes = f.read()
    # hash_string = binascii.hexlify(hash_bytes).decode('utf-8')
    return hash_bytes


def generate_hash_key(salt="my_salt", num_digit=256):
    # Derive a key from a passphrase using PBKDF2 with SHA-256
    passphrase = b"my_secret_passphrase"
    salt = b"my_salt"
    iterations = 100_000
    key_length = num_digit  # 256 bits
    algorithm = hashes.SHA256()

    kdf = PBKDF2HMAC(
        algorithm=algorithm,
        length=key_length,
        salt=salt,
        iterations=iterations,
    )

    key = kdf.derive(passphrase)

    return key

def generate_hash_string(salt="my_salt"):
    input_bytes = salt.encode("utf-8")

    # Generate teh SHA-256 hash object
    sha256 = hashlib.sha256()

    # update the hash object with the input bytes
    sha256.update(input_bytes)

    # get teh hexadecimal representation of the hash
    # hash_string = sha256.hexdigest()
    hash_bytes = sha256.digest()

    return hash_bytes


@FILE_TRANSFORMERS.add()
class compress2Tar(Base):
    """
    this transformer can help compress a list of files to tar.gz file
    {"type":"compress2Tar", "target_dir":"", "file_filter_regex":"", "out_dir":"", "out_file":""}
    """
    def __init__(   self, 
                    target_dir=None, 
                    file_filter_regex=None,
                    out_dir=None,
                    out_file=None):
        super().__init__()

        self.target_dir = target_dir
        self.file_filter_regex = file_filter_regex
        self.out_dir = out_dir
        self.out_file = out_file


    @transform_wrapper
    def transform(self, input):
        # retrieve filepaths
        filepaths = glob(os.path.join(self.target_dir, self.file_filter_regex))


        # compress file one by one into the out_archive
        out_archive = os.path.join(self.out_dir, self.out_file)
        with tarfile.open(out_archive, 'w:gz') as archive:
            for filepath in filepaths:
                archive.add(filepath)
            return {context_name:out_archive}


@FILE_TRANSFORMERS.add()
class splitFileIntoMultiple(Base):
    """
    this transformer can help compress a list of files to tar.gz file
    {"type":"splitFileIntoMultiple", "module_type":"file", "in_file":"", 
        "out_dir":"", "out_file_prefix":"", "max_size":1024*1024*100}

    1024 * 1024 * 100  # 100 MB
    """
    def __init__(   self, 
                    in_file=None,
                    out_dir=None,
                    out_file_prefix=None,
                    max_size=None):
        super().__init__()

        self.in_file = in_file
        self.out_dir = out_dir
        self.out_file_prefix = out_file_prefix
        self.max_size = max_size

        self.out_split_dir = os.path.join(self.out_dir, self.out_file_prefix)


    @transform_wrapper
    def transform(self, input):

        if not os.path.exists(self.out_split_dir):
            os.makedirs(self.out_split_dir)

        # Split the tar file into multiple files
        with open(self.in_file, 'rb') as f:
            chunk = f.read(self.max_size)
            i = 1
            while chunk:
                with open(os.path.join(self.out_split_dir, f'{self.out_file_prefix}.{i:03d}'), 'wb') as chunk_file:
                    chunk_file.write(chunk)
                i += 1
                chunk = f.read(self.max_size)

            return {context_name:self.out_split_dir}


@FILE_TRANSFORMERS.add()
class recoverFromMultipleFilesIntoOne(Base):
    """
    this transformer can help compress a list of files to tar.gz file
    {"type":"recoverFromMultipleFilesIntoOne", "module_type":"file", "in_dir":"", 
        "in_file_prefix":"",
        "out_dir":"", "out_file_ext":""}

    1024 * 1024 * 100  # 100 MB
    """
    def __init__(   self, 
                    in_dir=None,
                    in_file_prefix=None,
                    out_file_ext="tar.gz.enc",
                    out_dir=None):
        super().__init__()

        self.in_dir = in_dir
        self.in_file_prefix = in_file_prefix
        self.out_file_ext= out_file_ext
        self.out_dir = out_dir


    @transform_wrapper
    def transform(self, input):

        # List the split tar files in the input directory
        split_parts = [filename for filename in os.listdir(self.in_dir) if filename.startswith(self.in_file_prefix)]

        # Sort the split tar files in numerical order
        split_parts.sort(key=lambda filename: int(filename.split('.')[-1]))

        # Create a new file for the reconstructed tar archive
        out_file = os.path.join(self.out_dir, self.in_file_prefix+"."+self.out_file_ext)
        with open(out_file, 'wb') as f:
            # Concatenate the split tar files together
            for part in split_parts:
                with open(os.path.join(self.in_dir, part), 'rb') as part_file:
                    f.write(part_file.read())

        return {context_name:out_file}



@FILE_TRANSFORMERS.add()
class compressFilesToTarWithFernetKey(Base):
    """
    this transformer can help compress a list of files to tar.gz file
    {"type":"compressFilesToTarWithFernetKey", "fernet_key_file":"", "target_dir":"", 
        "file_filter_regex":"", "out_dir":"", "out_file":""}

    Usage:
        {"pipeline":[

        ]}
    """
    def __init__(   self, 
                    fernet_key_file=None,
                    target_dir=None, 
                    file_filter_regex=None,
                    out_dir=None,
                    out_file=None):
        super().__init__()

        self.fernet_key_file = fernet_key_file
        self.target_dir = target_dir
        self.file_filter_regex = file_filter_regex
        self.out_dir = out_dir
        self.out_file = out_file


    @transform_wrapper
    def transform(self, input):
        ##################################### save as a tar file
        # retrieve filepaths
        filepaths = glob(os.path.join(self.target_dir, self.file_filter_regex))
        # compress file one by one into the out_archive
        out_archive = os.path.join(self.out_dir, self.out_file)
        with tarfile.open(out_archive, 'w:gz') as archive:
            for filepath in filepaths:
                archive.add(filepath)

        #################################### encrypt the tar file content
        with open(out_archive, "r") as f:
            # retrieve tar file content
            content = f.read()

        # retreive fernet key
        fernet_key = get_fernet_key(self.fernet_key_file)
        # create fernet
        fernet = Fernet(fernet_key)
        # encrypted_data 
        encrypted_data = fernet.fernet.encrypt(content)
        # write encrypted_data to out file
        with open(out_archive, "w") as f:
            f.write(encrypted_data)

        return {context_name:out_archive}


@FILE_TRANSFORMERS.add()
class compressDirectoryToTarWithFernet(Base):
    """
    this transformer can help compress a list of files to tar.gz file
    {"type":"compressDirectoryToTarWithFernet", "fernet_key":"", "fernet_key_file":"", "target_dir":"", 
        "out_dir":"", "out_file":""}

    Usage:
        {"pipeline":[]

        ]}
    """
    def __init__(   self, 
                    custom_fernet_key = None,
                    fernet_key_file=None,
                    target_dir=None, 
                    out_dir=None,
                    out_file_prefix=None):
        super().__init__()
 
        self.custom_fernet_key = custom_fernet_key.encode()
        self.fernet_key_file = fernet_key_file
        self.target_dir = target_dir
        self.out_dir = out_dir
        self.out_file_prefix = out_file_prefix


    @transform_wrapper
    def transform(self, input):
        ##################################### save as a tar file
        # compress file one by one into the out_archive
        if self.out_file_prefix:
            archive_path = os.path.join(self.out_dir, self.out_file_prefix+".tar.gz")
        else:
            archive_path = os.path.join(self.out_dir, os.path.basename(self.target_dir)+".tar.gz")
        
        archive_name = os.path.basename(self.target_dir) 


        with tempfile.NamedTemporaryFile(suffix=".tar.gz") as tmp_file:
            with tarfile.open(tmp_file.name, mode='w:gz') as archive:
                archive.add(self.target_dir, arcname = archive_name)

            tmp_file_path = tmp_file.name
            print(tmp_file_path)

            # Read the tar file content
            with open(tmp_file_path, "rb") as tar:
                content = tar.read()

            # print(content)

            # retreive fernet key
            # print(f"self.fernet_key: {self.custom_fernet_key}")
            if not self.custom_fernet_key and self.fernet_key_file:
                key_bytes = get_fernet_key(self.fernet_key_file)
                fernet = Fernet(key_bytes)
            else:
                fernet = Fernet(self.custom_fernet_key)


            # encrypted_data 
            encrypted_data = fernet.encrypt(content)
            # write encrypted_data to out file
            with open(archive_path+".enc", "wb") as f:
                f.write(encrypted_data)

        return {context_name:archive_path+".enc"}


@FILE_TRANSFORMERS.add()
class compressDirectoryToTarWithPyAesCript(Base):
    """
    this transformer can help compress a list of files to tar.gz file
    {"type":"compressDirectoryToTarWithFernetKey", "fernet_key":"", "fernet_key_file":"", "target_dir":"", 
        "out_dir":""}

    Usage:
        {"pipeline":[]

        ]}
    """
    def __init__(   self, 
                    fernet_key = None,
                    fernet_key_file=None,
                    target_dir=None,
                    out_dir =None):
        super().__init__()

        self.fernet_key = fernet_key
        self.fernet_key_file = fernet_key_file
        self.target_dir = target_dir
        self.out_dir = out_dir

    @transform_wrapper
    def transform(self, input):
        ##################################### save as a tar file
        # compress file one by one into the out_archive
        archive_name = os.path.basename(self.target_dir)

        out_archive = os.path.join(self.out_dir, archive_name+".tar.gz")
        print(f"out file 1: {out_archive}")
        
        with tarfile.open(out_archive, 'w:gz') as archive:
            archive.add(self.target_dir, arcname = archive_name)

        #################################### encrypt the tar file
        # retreive fernet key
        if not self.fernet_key and self.fernet_key_file:
            fernet_key = get_fernet_key(self.fernet_key_file)
        else:
            fernet_key = self.fernet_key
        
        print(f"fernet key: {fernet_key}")
            
        # encrypted_data 
        bufferSize = 64 * 1024
        pyAesCrypt.encryptFile( out_archive,
                                out_archive+".enc",
                                fernet_key,
                                bufferSize)

        print(f"out file 2: {out_archive}.enc")

        return {context_name:out_archive+".enc"}


@FILE_TRANSFORMERS.add() 
class generateFernetKey(Base):
    """
    {"type":"generateFernetKey", "out_file":"", "isHash256":1, "salt":"nice to meet you"}
    """
    def __init__(self, 
                out_file=None, 
                isHash256=0,
                salt="nice"):
        super().__init__()

        self.out_file = out_file
        self.isHash256 = isHash256
        self.salt = salt

    @transform_wrapper
    def transform(self, input):
        # Generate a Fernet key
        if self.isHash256:
            key = generate_hash_string(salt=self.salt)
            # key = key.encode('utf-8')
        else:
            key = Fernet.generate_key()

        # save the key to a file
        with open(self.out_file, "wb") as f:
            f.write(key)

        return {context_name:self.out_file}


@FILE_TRANSFORMERS.add()
class decryptDirectoryToTarWithPyAesCript(Base):
    """
    this transformer can help compress a list of files to tar.gz file
    {"type":"decryptDirectoryToTarWithPyAesCript", "fernet_key":"", "fernet_key_file":"", "target_encypt_file":"", 
        "out_dir":""}

    Usage:
        {"pipeline":[]

        ]}
    """
    def __init__(   self, 
                    fernet_key = None,
                    fernet_key_file=None,
                    target_encypt_file=None,
                    out_dir =None):
        super().__init__()

        self.fernet_key = fernet_key
        self.fernet_key_file = fernet_key_file
        self.target_encypt_file = target_encypt_file
        self.out_dir = out_dir

    @transform_wrapper
    def transform(self, input):

        # retreive fernet key
        if not self.fernet_key and self.fernet_key_file:
            fernet_key = get_fernet_key(self.fernet_key_file)
        else:
            fernet_key = self.fernet_key
        
        print(f"fernet key: {fernet_key}")
            
        # decrypted file
        bufferSize = 64 * 1024
        pyAesCrypt.decryptFile( self.target_encypt_file,
                                self.target_encypt_file[:-4],
                                fernet_key,
                                bufferSize)

        # Extract the decrypted tar.gz file
        with tarfile.open(self.target_encypt_file[:-4], 'r:gz') as tar:
            tar.extractall(path=self.out_dir)


        return {context_name:self.target_encypt_file[:-4]}




@FILE_TRANSFORMERS.add()
class decryptEncFileToDirectoryWithFernet(Base):
    """to be modified
    this transformer can help compress a list of files to tar.gz file
    {"type":"decryptDirectoryToTarWithFernet", "fernet_key":"", "fernet_key_file":"", "target_encypt_file":"", 
        "out_dir":"", "num_files":3}

    Usage:
        {"pipeline":[]

        ]}
    """
    def __init__(   self, 
                    custom_fernet_key = None,
                    fernet_key_file=None,
                    target_encypt_file=None,
                    out_dir =None):
        super().__init__()

        self.custom_fernet_key = custom_fernet_key.encode()
        self.fernet_key_file = fernet_key_file
        self.target_encypt_file = target_encypt_file
        self.out_dir = out_dir

    @transform_wrapper
    def transform(self, input):

        # retreive fernet key
        if not self.custom_fernet_key and self.fernet_key_file:
            fernet_key = get_fernet_key(self.fernet_key_file)
        else:
            fernet_key = self.custom_fernet_key
        
        # print(f"fernet key: {fernet_key}")
            
        with open(self.target_encypt_file, "rb") as enc_file:
            encrypted_data = enc_file.read()


        # decrypted content
        fernet = Fernet(fernet_key)
        decrypted_data = fernet.decrypt(encrypted_data)

        # write the decrypted content to tar.gz
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tar.gz") as tmp_file:
            print(tmp_file.name)
            # print(decrypted_data)
            with open(tmp_file.name, "wb") as f:
                f.write(decrypted_data)

            # Extract the decrypted tar.gz file
            with tarfile.open(tmp_file.name, 'r:gz') as tar2:
                tar2.extractall(path=self.out_dir)
                tar_infos = tar2.getmembers()
                member = tar_infos[0].name

        return {context_name:os.path.join(self.out_dir, member)}