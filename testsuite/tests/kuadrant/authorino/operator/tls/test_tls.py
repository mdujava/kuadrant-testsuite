"""Tests that envoy deployed with TLS security works with Authorino"""
import pytest
from httpx import ReadError


def test_valid_certificate(envoy_authority, valid_cert, auth, envoy):
    """Tests that valid certificate will be accepted"""
    with envoy.client(verify=envoy_authority, cert=valid_cert) as client:
        response = client.get("/get", auth=auth)
        assert response.status_code == 200


def test_no_certificate(envoy, envoy_authority):
    """Test that request without certificate will be rejected"""
    with pytest.raises(ReadError, match="certificate required"):
        with envoy.client(verify=envoy_authority) as client:
            client.get("/get")


def test_invalid_certificate(envoy_authority, invalid_cert, auth, envoy):
    """Tests that certificate with different CA will be rejeceted"""
    with pytest.raises(ReadError, match="unknown ca"):
        with envoy.client(verify=envoy_authority, cert=invalid_cert) as client:
            client.get("/get", auth=auth)
