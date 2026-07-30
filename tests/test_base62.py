from app.services.base62 import encode


# Test if short_code for 0 is 'a'
def test_encode_zero():
    short_code = encode(0)

    assert short_code == 'a' , f"Short code for id 0 must be 'a'. Founded: '{short_code}'"
    

# Test if short_code for 61 is '9'
def test_encode_single_digit_boundary():
    short_code = encode(61)

    assert short_code == '9' , f"Short code for id 61 must be '9'. Founded: '{short_code}'"


# Test if short_code for 62 is 'ba'
def test_encode_two_digit_boundary():
    short_code = encode(62)

    assert short_code == 'ba' , f"Short code for id 62 must be 'ba'. Founded: '{short_code}'"


# Test if first five-digit short_code is 'baaaa'
def test_encode_five_digit_boundary():
    short_code = encode(14776336)

    assert short_code == 'baaaa' , f"Short code for id 14776336 must be 'baaaa'. Founded: '{short_code}'"
