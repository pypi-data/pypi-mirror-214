import tls_client


requests = tls_client.Session(
    client_identifier="chrome112",
    random_tls_extension_order=True
)
