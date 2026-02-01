# Task 3: Digital Identity and Trust

**1. Commands used:**
```bash
openssl s_client -connect ouf.fi:443 -showcerts | openssl x509 -text -noout
```

**2. Who has issued the certificate?**
*   **Answer:** Let's Encrypt (Intermediate CA: R12).
*   **Identification:** The `Issuer` field in the certificate data specifies `C = US, O = Let's Encrypt, CN = R12`.

**3. For what exact domain it has been certificated?**
*   **Answer:** ouf.fi
*   **Identification:** Listed in the `Subject` field as `CN = ouf.fi` and under `X509v3 Subject Alternative Name` as `DNS:ouf.fi`.

**4. When does it expire?**
*   **Answer:** April 19, 2026, at 18:01:12 GMT.
*   **Identification:** Found in the `Validity` section under `Not After : Apr 19 18:01:12 2026 GMT`.

**5. What is the encryption algorithm and key size?**
*   **Answer:** RSA Encryption with a 4096-bit key.
*   **Identification:** Found in `Subject Public Key Info` as `Public Key Algorithm: rsaEncryption` and `Public-Key: (4096 bit)`.

**6. Manual validation with openssl verify:**
*   **Initial Attempt:** Running `openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt ouf.crt` failed with `error 20: unable to get local issuer certificate`.
*   **Reason for Failure:** The system trust store only contains Root CAs. The `ouf.fi` certificate is signed by an Intermediate CA (R12), which is not in the system's root bundle. `openssl verify` does not automatically search for intermediates unless they are explicitly provided.
*   **Successful Validation:** I used the `-untrusted` flag to provide the intermediate certificates sent by the server:
    `openssl verify -CAfile /etc/ssl/certs/ca-certificates.crt -untrusted ouf_chain.pem ouf_chain.pem`
*   **Result:** This returned **ouf_chain.pem: OK**, confirming that the leaf certificate correctly chains to a trusted root through the provided intermediate.

**7. Validation process on Linux:**
*   **How it works:** Linux applications (like `curl` or `openssl`) verify certificates by comparing the certificate's issuer signature against a local "Trust Store" of known-good Root Certificate Authorities. The process involves building a path from the website's certificate, through any intermediate certificates, to a trusted root certificate stored on the local machine.
*   **Arch Linux Package:** The package containing these trusted root CAs is `ca-certificates`.
*   **Directory Location:** Individual certificates are located in `/etc/ssl/certs/`, and the combined bundle file used for verification is typically at `/etc/ssl/certs/ca-certificates.crt`.

