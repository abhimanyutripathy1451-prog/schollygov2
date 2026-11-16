import pytest
from pydantic import ValidationError
from backend.main import Signup,ProfilePatch,mobile,otp_verifier

def test_mobile_normalization():
    assert mobile('0987654321')=='+910987654321'
    assert mobile('+91 09876 54321')=='+910987654321'
    with pytest.raises(ValueError): mobile('123')

def test_pin_string_and_profile_boundary():
    data=Signup(mobile='0987654321',grant='x',pin='0001',full_name='Student',curriculum_code='CBSE_G5_EN')
    assert data.pin=='0001'
    with pytest.raises(ValidationError): Signup(**{**data.model_dump(),'pin':1234})
    with pytest.raises(ValidationError): ProfilePatch(mobile_e164='+910987654321')

def test_otp_keyed(monkeypatch):
    monkeypatch.setenv('OTP_SECRET','x'*32)
    assert otp_verifier('+910987654321','signup','123456')!=otp_verifier('+910987654321','recovery','123456')
