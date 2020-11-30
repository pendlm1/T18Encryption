import requests, json, re, os, sys, struct, time, shutil
from werkzeug.utils import secure_filename
from flask import Flask, render_template, url_for, session, redirect, request
from wtforms import (StringField, SubmitField, BooleanField, DateTimeField, RadioField,
SelectField, FloatField, TextField, TextAreaField, IntegerField)
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Declare global variables to store file names
aesKeyFileName = 'aesKey.txt'
arc4KeyFileName = 'arc4Key.txt'
chachaKeyFileName = 'chachaKey.txt'
chachaNonceFileName = 'chachaNonce.txt'

#AWS requires a variable called application
application = app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/select')
def select():
    return render_template("select.html")

@app.route('/aesdecrypt')
def aesdecrypt():
    return render_template("aesdecrypt.html")

@app.route('/arc4decrypt')
def arc4decrypt():
    return render_template("arc4decrypt.html")

@app.route('/chacha20decrypt')
def chacha20decrypt():
    return render_template("chacha20decrypt.html")

@app.route('/doubleDecrypt')
def doubleDecrypt():
    return render_template("doubleDecrypt.html")

@app.route('/tripleDecrypt')
def tripleDecrypt():
    return render_template("tripleDecrypt.html")

@app.route('/aesuploads', methods=["GET","POST"])
def aesuploads():
    if request.method == 'POST':
        f = request.files['fileName']
        f.save(f.filename)
        aes = request.files['aesKey']
        aes.save(aes.filename)
        return render_template("aesuploads.html", fileName = f.filename, aesKey = aes.filename)
    else:
        return render_template("aesdecrypt.html")

@app.route('/arc4uploads', methods=["GET","POST"])
def arc4uploads():
    if request.method == 'POST':
        f = request.files['fileName']
        f.save(f.filename)
        k = request.files['arc4Key']
        k.save(k.filename)
        return render_template("arc4uploads.html", fileName = f.filename, arc4Key = k.filename)
    else:
        return render_template("arc4decrypt.html")

@app.route('/chacha20uploads', methods=["GET","POST"])
def chacha20uploads():
    if request.method == 'POST':
        f = request.files['fileName']
        f.save(f.filename)
        k = request.files['chacha20Key']
        k.save(k.filename)
        n = request.files['chachaNonce']
        n.save(n.filename)
        return render_template("chacha20uploads.html", fileName = f.filename, chacha20Key = k.filename, chachaNonce = n.filename)
    else:
        return render_template("chacha20decrypt.html")

@app.route('/doubleDecryptUploads', methods=["GET","POST"])
def doubleDecryptUploads():
    if request.method == 'POST':
        f = request.files['fileName']
        f.save(f.filename)
        k = request.files['chacha20Key']
        k.save(k.filename)
        aes = request.files['aesKey']
        aes.save(aes.filename)
        n = request.files['chachaNonce']
        n.save(n.filename)
        return render_template("doubleDecryptUploads.html", fileName = f.filename, aesKey = aes.filename, chacha20Key = k.filename, chachaNonce = n.filename)
    else:
        return render_template("doubleDecrypt.html")

@app.route('/tripleDecryptUploads', methods=["GET","POST"])
def tripleDecryptUploads():
    if request.method == 'POST':
        f = request.files['fileName']
        f.save(f.filename)
        k = request.files['chacha20Key']
        k.save(k.filename)
        aes = request.files['aesKey']
        aes.save(aes.filename)
        arc4 = request.files['arc4Key']
        arc4.save(arc4.filename)
        n = request.files['chachaNonce']
        n.save(n.filename)
        return render_template("tripleDecryptUploads.html", fileName = f.filename, aesKey = aes.filename, arc4Key = arc4.filename, chacha20Key = k.filename, chachaNonce = n.filename)
    else:
        return render_template("tripleDecrypt.html")

@app.route('/upload', methods=["GET","POST"])
def upload():
    if request.method == 'POST':
        f = request.files['fileName']
        f.save(f.filename,)
        shutil.copyfile(f.filename,"static/uploads/"+f.filename)
        return render_template("upload.html", fileName = f.filename)
    else:
        return render_template("home.html")

@app.route('/decryptionResults', methods=["GET", "POST"])
def decryptionResults():
    file = request.args.get("fileName")
    method = request.args.get("encryptionType")
    if method == "AES Decryption":
        aesKey = request.args.get("aesKey")
        aesDecrypt(file,aesKey)
    elif method == "ARC4 Decryption":
        arc4Key = request.args.get("arc4Key")
        arc4Decrypt(file, arc4Key)
    elif method == "ChaCha20 Decryption":
        nonce = request.args.get("chachaNonce")
        chachaKey = request.args.get("chacha20Key")
        chachaDecrypt(file, chachaKey, nonce)
    elif method == "Double Decryption":
        aesKey = request.args.get("aesKey")
        nonce = request.args.get("chachaNonce")
        chachaKey = request.args.get("chacha20Key")
        doubleDecrypt(file, nonce, chachaKey, aesKey)
    elif method == "Triple Decryption":
        file2Decrypt = file
        tripleDecrypt(file2Decrypt, chachaNonceFileName, chachaKeyFileName, aesKeyFileName, arc4KeyFileName)
    return render_template("decryptionResults.html",fileName = file, encryptionType = method)

@app.route('/results', methods=["GET", "POST"])
def results():
    file = request.args.get("fileName")
    aesKey = request.args.get("aesKey")
    method = request.args.get("encryptionType")
    keys = generatreKeys()
    fileSize = os.path.getsize(str(file))
    price = 0.005
    total = fileSize*price
    if method == "AES Encryption":
        file2Encrypt = file
        aesEncrypt(file2Encrypt, aesKeyFileName)
        shutil.copyfile("aesKey.txt","static/keys/"+file+"aeskey.txt")
    elif method == "ARC4 Encryption":
        file2Encrypt = file
        arc4Encrypt(file2Encrypt, arc4KeyFileName)
        shutil.copyfile("arc4Key.txt","static/keys/"+file+"arc4key.txt")
    elif method == "Chacha20 Encryption":
        file2Encrypt = file
        chachaEncrypt(file2Encrypt, chachaKeyFileName, chachaNonceFileName)
        shutil.copyfile("chachaKey.txt","static/keys/"+file+"chachakey.txt")
        shutil.copyfile("chachaNonce.txt","static/keys/"+file+"chachaNonce.txt")
    elif method == 'Double Encryption':
        file2Encrypt = file
        doubleEncrypt(file2Encrypt, chachaNonceFileName, chachaKeyFileName, aesKeyFileName)
        shutil.copyfile("aesKey.txt","static/keys/"+file+"aeskey.txt")
        shutil.copyfile("chachaKey.txt","static/keys/"+file+"chachakey.txt")
        shutil.copyfile("chachaNonce.txt","static/keys/"+file+"chachaNonce.txt")
    elif method == "Triple Encryption":
        file2Encrypt = file
        tripleEncrypt(file2Encrypt, chachaNonceFileName, chachaKeyFileName, aesKeyFileName, arc4KeyFileName)
        shutil.copyfile("aesKey.txt","static/keys/"+file+"aeskey.txt")
        shutil.copyfile("arc4Key.txt","static/keys/"+file+"arc4key.txt")
        shutil.copyfile("chachaKey.txt","static/keys/"+file+"chachakey.txt")
        shutil.copyfile("chachaNonce.txt","static/keys/"+file+"chachaNonce.txt")
    return render_template("results.html",fileName = file, encryptionType = method, aesKey=keys[0], arc4Key=keys[1],chachaKey=keys[2],nonce=keys[3], fileSize = fileSize, price=price, total =total)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

def generatreKeys():
    # Generate keys for Chacha20, ARC4, and AES
    key1 = os.urandom(32)
    key2 = os.urandom(32)
    key3 = os.urandom(32)
    nonce = os.urandom(16)
    # Write keys/nonce to file
    with open("aesKey.txt", 'wb') as aesKey:
        aesKey.write((key1))
    with open("arc4Key.txt", 'wb') as arc4Key:
        arc4Key.write((key2))
    with open("chachaKey.txt", 'wb') as chachaKey:
        chachaKey.write((key3))
    with open("chachaNonce.txt", 'wb') as nonceFile:
        nonceFile.write((nonce))
    return [key1,key2,key3,nonce]

# AES encryption
def aesEncrypt(file2Encrypt, keyFileName):
    # Get the key from the file.
    with open(keyFileName, 'rb') as keyFile:
        try:
            key = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    with open(file2Encrypt, 'rb') as inputFile:
        outFile = 'static/uploads/encrypted_' + file2Encrypt
        fileSize = os.path.getsize(file2Encrypt)
        iv = os.urandom(16)
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = backend)
        with open(outFile, 'wb') as outputFile:
            outputFile.write(struct.pack('<Q', fileSize))
            outputFile.write(iv)
            print("Time to encrypt the file.")
            chunk = inputFile.read()
            block_length = 16
            remainder = (fileSize) % block_length
            padding = block_length - remainder
            if remainder != 0:
                for pad in range(padding):
                    chunk += b'0'
            encryptor = cipher.encryptor()
            ct = encryptor.update(chunk) + encryptor.finalize()
            outputFile.write(ct)
        print("Encryption complete.")
    return outFile

# AES Decryption
def aesDecrypt(file2Decrypt, keyFileName):
    with open(keyFileName, 'rb') as keyFile:
        try:
            key = keyFile.read()
            #key = bytes(info, 'utf-8')
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    with open(file2Decrypt, 'rb') as inputFile:
        originalSize = struct.unpack('<Q', inputFile.read(struct.calcsize('Q')))[0]
        iv = inputFile.read(16)
        backend = default_backend()
        outFile = 'static/uploads/decrypted_' + file2Decrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = backend)
        print("Time to decrypt the file.")
        with open(outFile, 'wb') as outputFile:
            while True:
                chunk = inputFile.read()
                if len(chunk) == 0:
                    break
                decryptor = cipher.decryptor()
                pt = decryptor.update(chunk) + decryptor.finalize()
                outputFile.write(pt[:originalSize])
        print("Decryption complete.")
    return outFile

# Chacha20 Encrytion
def chachaEncrypt(file2Encrypt, keyFileName, nonceFile):
    # Get the key from the file.
    with open(keyFileName, 'rb') as keyFile:
        try:
            key = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    with open(nonceFile, 'rb') as nFile:
        try:
            nonce = nFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    with open(file2Encrypt, 'rb') as inputFile:
        content = inputFile.read()
    outFile = 'static/uploads/encrypted_' + file2Encrypt
    backend = default_backend()
    with open(outFile, 'wb') as outputFile:
        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode = None, backend = backend)
        print("Time to encrypt the file.")
        encryptor = cipher.encryptor()
        ct = encryptor.update(content)
        outputFile.write(ct)
    print("Encryption complete.")
    return outFile

# Chacha20 Decryption
def chachaDecrypt(file2Decrypt, keyFileName, nonceFile):
    # Get the key from the file.
    with open(keyFileName, 'rb') as keyFile:
        try:
            key = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    with open(nonceFile, 'rb') as nFile:
        try:
            nonce = nFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    with open(file2Decrypt, 'rb') as inputFile:
        content = inputFile.read()
    outFile = 'static/uploads/decrypted_' + file2Decrypt
    backend = default_backend()
    with open(outFile, 'wb') as outputFile:
        algorithm = algorithms.ChaCha20(key, nonce)
        cipher = Cipher(algorithm, mode = None, backend = backend)
        print("Time to decrypt the file.")
        decryptor = cipher.decryptor()
        pt = decryptor.update(content)
        outputFile.write(pt)
    print("Decryption complete.")
    return outFile

# ARC4 Encryption
def arc4Encrypt(file2Encrypt, keyFileName):
    # Get the key from the file.
    with open(keyFileName, 'rb') as keyFile:
        try:
            key = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    with open(file2Encrypt, 'rb') as inputFile:
        content = inputFile.read()
    outFile = 'static/uploads/encrypted_' + file2Encrypt
    backend = default_backend()
    with open(outFile, 'wb') as outputFile:
        algorithm = algorithms.ARC4(key)
        cipher = Cipher(algorithm, mode = None, backend = backend)
        print("Time to encrypt the file.")
        encryptor = cipher.encryptor()
        ct = encryptor.update(content)
        outputFile.write(ct)
    print("Encryption complete.")
    return outFile

# ARC4 Decryption
def arc4Decrypt(file2Decrypt, keyFileName):
    # Get the key from the file.
    with open(keyFileName, 'rb') as keyFile:
        try:
            key = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    with open(file2Decrypt, 'rb') as inputFile:
        content = inputFile.read()
    outFile = 'static/uploads/decrypted_' + file2Decrypt
    backend = default_backend()
    with open(outFile, 'wb') as outputFile:
        algorithm = algorithms.ARC4(key)
        cipher = Cipher(algorithm, mode = None, backend = backend)
        print("Time to decrypt the file.")
        decryptor = cipher.decryptor()
        pt = decryptor.update(content)
        outputFile.write(pt)
    print("Decryption complete.")
    return outFile

# Double encryption
def doubleEncrypt(file2Encrypt, nonceFileName, chaFileName, aesFileName):
    #Get the nonce from the file.
    with open(nonceFileName, 'rb') as nFile:
        try:
            nonce = nFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    # Get the chacha20 key from the file.
    with open(chaFileName, 'rb') as keyFile:
        try:
            chachaKey = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    # Get the aes key from the file.
    with open(aesFileName, 'rb') as aFile:
        try:
            aesKey = aFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")
    # Read in file
    with open(file2Encrypt, 'rb') as inputFile:
        content = inputFile.read()
    outFile = "static/uploads/encrypted_" +file2Encrypt
    backend = default_backend()
    print("Time to encrypt the file.")
    # Encrypt with chacha 20
    algorithm1 = algorithms.ChaCha20(chachaKey, nonce)
    cipher1 = Cipher(algorithm1, mode = None, backend = backend)
    print("Encrypting file using method one.")
    encryptor1 = cipher1.encryptor()
    chaCT = encryptor1.update(content)
    #Encrypt with aes
    iv = os.urandom(16)
    cipher2 = Cipher(algorithms.AES(aesKey), modes.CBC(iv), backend = backend)
    print("Encrypting file using method two.")
    fileSize = os.path.getsize(file2Encrypt)
    outFile = "static/uploads/encrypted_" + file2Encrypt
    with open(outFile, 'wb') as outputFile2:
        outputFile2.write(struct.pack('<Q', fileSize))
        outputFile2.write(iv)
        chunk = chaCT
        block_length = 16
        remainder = (fileSize) % block_length
        padding = block_length - remainder
        if remainder != 0:
            for pad in range(padding):
                chunk += b'0'
        encryptor2 = cipher2.encryptor()
        ct = encryptor2.update(chunk) + encryptor2.finalize()
        outputFile2.write(ct)
    print("Encryption complete.")
    return outFile

# Double decryption
def doubleDecrypt(file2Decrypt, nonceFileName, chaFileName, aesFileName):
   #Get the nonce from the file.
    with open(nonceFileName, 'rb') as nFile:
        try:
            nonce = nFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    # Get the chacha20 key from the file.
    with open(chaFileName, 'rb') as keyFile:
        try:
            chachaKey = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    # Get the aes key from the file.
    with open(aesFileName, 'rb') as aFile:
        try:
            aesKey = aFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    outFile = 'static/uploads/decrypted_' + file2Decrypt
    backend = default_backend()

    # Read in file
    with open(file2Decrypt, 'rb') as inputFile:
        originalSize = struct.unpack('<Q', inputFile.read(struct.calcsize('Q')))[0]
        iv = inputFile.read(16)

        cipher1 = Cipher(algorithms.AES(aesKey), modes.CBC(iv), backend = backend)

        print("Time to decrypt the file.")
        print("Decrypting using method two.")
        while True:
            chunk = inputFile.read()
            if len(chunk) == 0:
                break
            decryptor1 = cipher1.decryptor()
            aesPT = decryptor1.update(chunk) + decryptor1.finalize()

    # Decrypt using ChaCha20
    algorithm2 = algorithms.ChaCha20(chachaKey, nonce)
    cipher2 = Cipher(algorithm2, mode = None, backend = backend)
    print("Decrypting using method one.")
    decryptor2 = cipher2.decryptor()
    chachaPT = decryptor2.update(aesPT)


    with open(outFile, 'wb') as outputFile1:
        outputFile1.write(chachaPT)

    print("Decryption complete.")

    return outFile

# Triple encryption
def tripleEncrypt(file2Encrypt, nonceFileName, chaFileName, aesFileName, arc4FileName):
    #Get the nonce from the file.
    with open(nonceFileName, 'rb') as nFile:
        try:
            nonce = nFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    # Get the chacha20 key from the file.
    with open(chaFileName, 'rb') as keyFile:
        try:
            chachaKey = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    # Get the aes key from the file.
    with open(aesFileName, 'rb') as aFile:
        try:
            aesKey = aFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    # Get the ARC4 key from the file
    with open(arc4FileName, 'rb') as arc4File:
        try:
            arc4Key = arc4File.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    with open(file2Encrypt, 'rb') as inputFile:
        content = inputFile.read()
    outFile = file2Encrypt
    backend = default_backend()

    print("Time to encrypt the file.")

    # Encrypt with chacha 20
    algorithm1 = algorithms.ChaCha20(chachaKey, nonce)
    cipher1 = Cipher(algorithm1, mode = None, backend = backend)
    print("Encrypting file using method one.")
    encryptor1 = cipher1.encryptor()
    chaCT = encryptor1.update(content)

    # Encrypt with ARC4
    algorithm2 = algorithms.ARC4(arc4Key)
    cipher2 = Cipher(algorithm2, mode = None, backend = backend)
    print("Encrypting file using method two.")
    encryptor2 = cipher2.encryptor()
    arc4CT = encryptor2.update(chaCT)

    #Encrypt with aes
    iv = os.urandom(16)
    cipher3 = Cipher(algorithms.AES(aesKey), modes.CBC(iv), backend = backend)
    print("Encrypting file using method three.")
    fileSize = os.path.getsize(file2Encrypt)
    outFile = "static/uploads/encrypted_" + file2Encrypt

    with open(outFile, 'wb') as outputFile2:
        outputFile2.write(struct.pack('<Q', fileSize))
        outputFile2.write(iv)

        chunk = arc4CT
        block_length = 16
        remainder = (fileSize) % block_length
        padding = block_length - remainder

        if remainder != 0:
            for pad in range(padding):
                chunk += b'0'

        encryptor = cipher3.encryptor()
        ct = encryptor.update(chunk) + encryptor.finalize()
        outputFile2.write(ct)
    print("Encryption complete.")

    return outFile

# Triple Decryption
def tripleDecrypt(file2Decrypt, nonceFileName, chaFileName, aesFileName, arc4FileName):
   #Get the nonce from the file.
    with open(nonceFileName, 'rb') as nFile:
        try:
            nonce = nFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    # Get the chacha20 key from the file.
    with open(chaFileName, 'rb') as keyFile:
        try:
            chachaKey = keyFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    # Get the aes key from the file.
    with open(aesFileName, 'rb') as aFile:
        try:
            aesKey = aFile.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    # Get the ARC4 key from the file
    with open(arc4FileName, 'rb') as arc4File:
        try:
            arc4Key = arc4File.read()
        except FileNotFoundError:
            print("File name is invalid. Enter the correct key file name.")

    outFile = 'static/uploads/decrypted_' + file2Decrypt
    backend = default_backend()

    with open(file2Decrypt, 'rb') as inputFile:
        originalSize = struct.unpack('<Q', inputFile.read(struct.calcsize('Q')))[0]
        iv = inputFile.read(16)

        cipher1 = Cipher(algorithms.AES(aesKey), modes.CBC(iv), backend = backend)

        print("Time to decrypt the file.")
        print("Decrypting using method three.")
        while True:
            chunk = inputFile.read()
            if len(chunk) == 0:
                break
            decryptor1 = cipher1.decryptor()
            aesPT = decryptor1.update(chunk) + decryptor1.finalize()

    # Decrypt using ARC4
    algorithm2 = algorithms.ARC4(arc4Key)
    cipher2 = Cipher(algorithm2, mode = None, backend = backend)
    print("Decrypting using method two.")
    decryptor2 = cipher2.decryptor()
    arc4PT = decryptor2.update(aesPT)

    # Decrypt using ChaCha20
    algorithm3 = algorithms.ChaCha20(chachaKey, nonce)
    cipher3 = Cipher(algorithm3, mode = None, backend = backend)
    print("Decrypting using method one.")
    decryptor3 = cipher3.decryptor()
    chachaPT = decryptor3.update(arc4PT)


    with open(outFile, 'wb') as outputFile1:
        outputFile1.write(chachaPT)

    print("Decryption complete.")

    return outFile

if __name__ == '__main__':
    app.run(debug=True)
