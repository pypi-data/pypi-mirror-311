from mind_castle.stores.plaintext import PlaintextSecretStore


def test_put_secret():
    secret_store = PlaintextSecretStore()
    response = secret_store.put_secret("some_secret_value")

    # Just read the memory from this implementation
    assert response["key"] == "some_secret_value"
    assert response["mind_castle_secret_type"] == secret_store.store_type


def test_get_secret():
    secret_store = PlaintextSecretStore()
    response = secret_store.put_secret("some_secret_value")

    assert (
        secret_store.get_secret(
            {"mind_castle_secret_type": "plaintext", "key": response["key"]}
        )
        == "some_secret_value"
    )
