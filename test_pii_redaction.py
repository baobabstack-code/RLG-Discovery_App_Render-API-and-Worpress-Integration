"""
Property-based tests for PII redaction patterns (Email and Phone).

Uses hypothesis for property-based testing.

Feature: improved-pii-redaction
"""
import re
from typing import List
from hypothesis import given, strategies as st, settings, assume, HealthCheck

from logic import PRESETS, load_patterns


# =============================================================================
# Test Infrastructure and Strategies
# =============================================================================

def get_email_patterns() -> List[re.Pattern]:
    """Load compiled Email patterns from PRESETS."""
    return load_patterns(["Email"], "", "", False)


def get_phone_patterns() -> List[re.Pattern]:
    """Load compiled Phone patterns from PRESETS."""
    return load_patterns(["Phone"], "", "", False)


def matches_any_pattern(text: str, patterns: List[re.Pattern]) -> bool:
    """Check if text matches any of the given patterns."""
    return any(p.search(text) for p in patterns)


# Strategy for generating valid email local parts
email_local_part = st.from_regex(r"[a-zA-Z][a-zA-Z0-9._%+-]{0,20}", fullmatch=True)

# Strategy for generating valid email domains
email_domain = st.from_regex(r"[a-zA-Z][a-zA-Z0-9-]{0,10}", fullmatch=True)

# Strategy for generating valid TLDs
email_tld = st.sampled_from(["com", "org", "net", "edu", "gov", "io", "co", "uk", "de", "fr"])

# Strategy for generating 3-digit area codes (valid US area codes don't start with 0 or 1)
area_code = st.from_regex(r"[2-9][0-9]{2}", fullmatch=True)

# Strategy for generating 3-digit exchange codes
exchange_code = st.from_regex(r"[2-9][0-9]{2}", fullmatch=True)

# Strategy for generating 4-digit subscriber numbers
subscriber_number = st.from_regex(r"[0-9]{4}", fullmatch=True)

# Strategy for phone separators
phone_separator = st.sampled_from(["-", ".", " ", "/", ""])


@st.composite
def valid_standard_email(draw):
    """Generate a valid standard email address."""
    local = draw(email_local_part)
    domain = draw(email_domain)
    tld = draw(email_tld)
    return f"{local}@{domain}.{tld}"


@st.composite
def valid_phone_10_digits(draw):
    """Generate a valid 10-digit phone number as consecutive digits."""
    area = draw(area_code)
    exchange = draw(exchange_code)
    subscriber = draw(subscriber_number)
    return f"{area}{exchange}{subscriber}"


@st.composite
def valid_phone_with_separators(draw):
    """Generate a valid phone number with separators."""
    area = draw(area_code)
    exchange = draw(exchange_code)
    subscriber = draw(subscriber_number)
    sep1 = draw(phone_separator)
    sep2 = draw(phone_separator)
    
    # Optionally add parentheses around area code
    use_parens = draw(st.booleans())
    if use_parens:
        return f"({area}){sep1}{exchange}{sep2}{subscriber}"
    return f"{area}{sep1}{exchange}{sep2}{subscriber}"


@st.composite
def valid_phone_with_country_code(draw):
    """Generate a valid phone number with country code."""
    area = draw(area_code)
    exchange = draw(exchange_code)
    subscriber = draw(subscriber_number)
    sep = draw(phone_separator)
    
    # Country code variations
    country_prefix = draw(st.sampled_from(["+1", "1", "+1 ", "1 ", "+1-", "1-"]))
    
    return f"{country_prefix}{area}{sep}{exchange}{sep}{subscriber}"


# =============================================================================
# Property 1: Valid Email Format Detection
# =============================================================================

class TestValidEmailFormatDetection:
    """
    Property 1: Valid Email Format Detection
    
    *For any* valid email address constructed with standard characters 
    (alphanumeric, dots, underscores, hyphens, plus signs in local part; 
    alphanumeric, dots, hyphens in domain; 2+ character TLD), 
    at least one Email pattern in PRESETS SHALL match it.
    
    **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.7**
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(email=valid_standard_email())
    def test_standard_email_format_detected(self, email: str):
        """
        Feature: improved-pii-redaction, Property 1: Valid Email Format Detection
        
        For any valid standard email address, at least one Email pattern
        should match it.
        
        **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.7**
        """
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Email '{email}' should be matched by at least one pattern"
        )
    
    @settings(max_examples=100)
    @given(
        local=email_local_part,
        subdomain=email_domain,
        domain=email_domain,
        tld=email_tld,
    )
    def test_email_with_subdomain_detected(
        self, local: str, subdomain: str, domain: str, tld: str
    ):
        """
        Feature: improved-pii-redaction, Property 1: Valid Email Format Detection
        
        For any email with subdomains (user@mail.domain.com), the pattern
        should match.
        
        **Validates: Requirements 1.6**
        """
        email = f"{local}@{subdomain}.{domain}.{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Email with subdomain '{email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(
        first=st.from_regex(r"[a-zA-Z][a-zA-Z0-9]{1,10}", fullmatch=True),
        last=st.from_regex(r"[a-zA-Z][a-zA-Z0-9]{1,10}", fullmatch=True),
        domain=email_domain,
        tld=email_tld,
    )
    def test_email_with_dots_in_local_part_detected(
        self, first: str, last: str, domain: str, tld: str
    ):
        """
        Feature: improved-pii-redaction, Property 1: Valid Email Format Detection
        
        For any email with dots in local part (first.last@domain.com),
        the pattern should match.
        
        **Validates: Requirements 1.3**
        """
        email = f"{first}.{last}@{domain}.{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Email with dots '{email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(
        user=st.from_regex(r"[a-zA-Z][a-zA-Z0-9]{1,10}", fullmatch=True),
        tag=st.from_regex(r"[a-zA-Z0-9]{1,5}", fullmatch=True),
        domain=email_domain,
        tld=email_tld,
    )
    def test_email_with_plus_addressing_detected(
        self, user: str, tag: str, domain: str, tld: str
    ):
        """
        Feature: improved-pii-redaction, Property 1: Valid Email Format Detection
        
        For any email with plus addressing (user+tag@domain.com),
        the pattern should match.
        
        **Validates: Requirements 1.4**
        """
        email = f"{user}+{tag}@{domain}.{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Email with plus addressing '{email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(
        user=st.from_regex(r"[a-zA-Z][a-zA-Z0-9]{1,10}", fullmatch=True),
        domain=email_domain,
        tld=email_tld,
        separator=st.sampled_from(["_", "-"]),
    )
    def test_email_with_underscore_or_hyphen_detected(
        self, user: str, domain: str, tld: str, separator: str
    ):
        """
        Feature: improved-pii-redaction, Property 1: Valid Email Format Detection
        
        For any email with underscores or hyphens (user_name@domain.com),
        the pattern should match.
        
        **Validates: Requirements 1.5**
        """
        email = f"{user}{separator}name@{domain}.{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Email with separator '{email}' should be matched"
        )


# =============================================================================
# Property 2: Obfuscated Email Detection
# =============================================================================

class TestObfuscatedEmailDetection:
    """
    Property 2: Obfuscated Email Detection
    
    *For any* valid email address that has been obfuscated by replacing 
    @ with [at], (at), or spaces around @, and/or replacing . with [dot] 
    or (dot), at least one Email pattern in PRESETS SHALL match it.
    
    **Validates: Requirements 1.8, 1.9, 1.10**
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        local=email_local_part,
        domain=email_domain,
        tld=email_tld,
    )
    def test_email_with_spaces_around_at_detected(
        self, local: str, domain: str, tld: str
    ):
        """
        Feature: improved-pii-redaction, Property 2: Obfuscated Email Detection
        
        For any email with spaces around @ (user @ domain.com),
        the pattern should match.
        
        **Validates: Requirements 1.8**
        """
        email = f"{local} @ {domain}.{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Email with spaces around @ '{email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(
        local=email_local_part,
        domain=email_domain,
        tld=email_tld,
        at_replacement=st.sampled_from(["[at]", "(at)", " at "]),
    )
    def test_email_with_obfuscated_at_detected(
        self, local: str, domain: str, tld: str, at_replacement: str
    ):
        """
        Feature: improved-pii-redaction, Property 2: Obfuscated Email Detection
        
        For any email with [at] or (at) instead of @ (user[at]domain.com),
        the pattern should match.
        
        **Validates: Requirements 1.9**
        """
        email = f"{local}{at_replacement}{domain}.{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Email with obfuscated @ '{email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(
        local=email_local_part,
        domain=email_domain,
        tld=email_tld,
        dot_replacement=st.sampled_from(["[dot]", "(dot)", " dot "]),
    )
    def test_email_with_obfuscated_dot_detected(
        self, local: str, domain: str, tld: str, dot_replacement: str
    ):
        """
        Feature: improved-pii-redaction, Property 2: Obfuscated Email Detection
        
        For any email with [dot] or (dot) instead of . (user@domain[dot]com),
        the pattern should match.
        
        **Validates: Requirements 1.10**
        """
        email = f"{local}@{domain}{dot_replacement}{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Email with obfuscated dot '{email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(
        local=email_local_part,
        domain=email_domain,
        tld=email_tld,
        at_replacement=st.sampled_from(["[at]", "(at)", " at "]),
        dot_replacement=st.sampled_from(["[dot]", "(dot)", " dot "]),
    )
    def test_fully_obfuscated_email_detected(
        self, local: str, domain: str, tld: str, 
        at_replacement: str, dot_replacement: str
    ):
        """
        Feature: improved-pii-redaction, Property 2: Obfuscated Email Detection
        
        For any fully obfuscated email (user [at] domain [dot] com),
        the pattern should match.
        
        **Validates: Requirements 1.8, 1.9, 1.10**
        """
        email = f"{local}{at_replacement}{domain}{dot_replacement}{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Fully obfuscated email '{email}' should be matched"
        )


# =============================================================================
# Property 3: Email Case Insensitivity
# =============================================================================

class TestEmailCaseInsensitivity:
    """
    Property 3: Email Case Insensitivity
    
    *For any* valid email address, transforming it to uppercase, lowercase, 
    or mixed case SHALL still result in a match by the Email patterns.
    
    **Validates: Requirements 1.11**
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(email=valid_standard_email())
    def test_uppercase_email_detected(self, email: str):
        """
        Feature: improved-pii-redaction, Property 3: Email Case Insensitivity
        
        For any email converted to uppercase, the pattern should still match.
        
        **Validates: Requirements 1.11**
        """
        upper_email = email.upper()
        patterns = get_email_patterns()
        
        assert matches_any_pattern(upper_email, patterns), (
            f"Uppercase email '{upper_email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(email=valid_standard_email())
    def test_lowercase_email_detected(self, email: str):
        """
        Feature: improved-pii-redaction, Property 3: Email Case Insensitivity
        
        For any email converted to lowercase, the pattern should still match.
        
        **Validates: Requirements 1.11**
        """
        lower_email = email.lower()
        patterns = get_email_patterns()
        
        assert matches_any_pattern(lower_email, patterns), (
            f"Lowercase email '{lower_email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(email=valid_standard_email())
    def test_mixed_case_email_detected(self, email: str):
        """
        Feature: improved-pii-redaction, Property 3: Email Case Insensitivity
        
        For any email with mixed case, the pattern should still match.
        
        **Validates: Requirements 1.11**
        """
        # Create mixed case by alternating upper/lower
        mixed_email = "".join(
            c.upper() if i % 2 == 0 else c.lower() 
            for i, c in enumerate(email)
        )
        patterns = get_email_patterns()
        
        assert matches_any_pattern(mixed_email, patterns), (
            f"Mixed case email '{mixed_email}' should be matched"
        )
    
    @settings(max_examples=100)
    @given(
        local=email_local_part,
        domain=email_domain,
        tld=email_tld,
        at_replacement=st.sampled_from(["[AT]", "(AT)", "[at]", "(at)"]),
    )
    def test_obfuscated_at_case_insensitive(
        self, local: str, domain: str, tld: str, at_replacement: str
    ):
        """
        Feature: improved-pii-redaction, Property 3: Email Case Insensitivity
        
        For any obfuscated email with [AT] or [at], the pattern should match
        regardless of case.
        
        **Validates: Requirements 1.11**
        """
        email = f"{local}{at_replacement}{domain}.{tld}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(email, patterns), (
            f"Obfuscated email with case variation '{email}' should be matched"
        )


# =============================================================================
# Property 4: Valid Phone Format Detection
# =============================================================================

class TestValidPhoneFormatDetection:
    """
    Property 4: Valid Phone Format Detection
    
    *For any* 10-digit phone number formatted with any combination of valid 
    separators (dash, dot, space, slash, or none) between the 3-3-4 digit groups, 
    optionally with parentheses around the area code, and optionally with a 
    +1 or 1 prefix, at least one Phone pattern in PRESETS SHALL match it.
    
    **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10, 2.11**
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(phone=valid_phone_10_digits())
    def test_10_consecutive_digits_detected(self, phone: str):
        """
        Feature: improved-pii-redaction, Property 4: Valid Phone Format Detection
        
        For any 10 consecutive digit phone number, the pattern should match.
        
        **Validates: Requirements 2.1**
        """
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(phone, patterns), (
            f"10-digit phone '{phone}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(phone=valid_phone_with_separators())
    def test_phone_with_separators_detected(self, phone: str):
        """
        Feature: improved-pii-redaction, Property 4: Valid Phone Format Detection
        
        For any phone number with standard separators, the pattern should match.
        
        **Validates: Requirements 2.2, 2.3, 2.4, 2.5, 2.8, 2.10, 2.11**
        """
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(phone, patterns), (
            f"Phone with separators '{phone}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(phone=valid_phone_with_country_code())
    def test_phone_with_country_code_detected(self, phone: str):
        """
        Feature: improved-pii-redaction, Property 4: Valid Phone Format Detection
        
        For any phone number with country code (+1 or 1), the pattern should match.
        
        **Validates: Requirements 2.6, 2.7**
        """
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(phone, patterns), (
            f"Phone with country code '{phone}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        area=area_code,
        exchange=exchange_code,
        subscriber=subscriber_number,
        sep1=phone_separator,
        sep2=phone_separator,
    )
    def test_phone_with_mixed_separators_detected(
        self, area: str, exchange: str, subscriber: str, sep1: str, sep2: str
    ):
        """
        Feature: improved-pii-redaction, Property 4: Valid Phone Format Detection
        
        For any phone number with mixed separators, the pattern should match.
        
        **Validates: Requirements 2.8**
        """
        phone = f"{area}{sep1}{exchange}{sep2}{subscriber}"
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(phone, patterns), (
            f"Phone with mixed separators '{phone}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        area=area_code,
        exchange=exchange_code,
        subscriber=subscriber_number,
        extra_spaces=st.integers(min_value=1, max_value=3),
    )
    def test_phone_with_extra_spaces_detected(
        self, area: str, exchange: str, subscriber: str, extra_spaces: int
    ):
        """
        Feature: improved-pii-redaction, Property 4: Valid Phone Format Detection
        
        For any phone number with extra spaces, the pattern should match.
        
        **Validates: Requirements 2.9**
        """
        spaces = " " * extra_spaces
        phone = f"({area}){spaces}{exchange}{spaces}{subscriber}"
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(phone, patterns), (
            f"Phone with extra spaces '{phone}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        area=area_code,
        exchange=exchange_code,
        subscriber=subscriber_number,
    )
    def test_phone_with_slashes_detected(
        self, area: str, exchange: str, subscriber: str
    ):
        """
        Feature: improved-pii-redaction, Property 4: Valid Phone Format Detection
        
        For any phone number with slashes, the pattern should match.
        
        **Validates: Requirements 2.10**
        """
        phone = f"{area}/{exchange}/{subscriber}"
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(phone, patterns), (
            f"Phone with slashes '{phone}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        area=area_code,
        exchange=exchange_code,
        subscriber=subscriber_number,
    )
    def test_phone_no_separator_after_parens_detected(
        self, area: str, exchange: str, subscriber: str
    ):
        """
        Feature: improved-pii-redaction, Property 4: Valid Phone Format Detection
        
        For any phone number with no separator after area code parenthesis,
        the pattern should match.
        
        **Validates: Requirements 2.11**
        """
        phone = f"({area}){exchange}-{subscriber}"
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(phone, patterns), (
            f"Phone with no separator after parens '{phone}' should be matched"
        )


# =============================================================================
# Property 5: Invalid Phone Length Rejection
# =============================================================================

class TestInvalidPhoneLengthRejection:
    """
    Property 5: Invalid Phone Length Rejection
    
    *For any* digit sequence that does not contain exactly 10 digits 
    (excluding country code), the Phone patterns SHALL NOT match it 
    as a complete phone number.
    
    **Validates: Requirements 2.12**
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        num_digits=st.integers(min_value=1, max_value=9),
    )
    def test_too_few_digits_not_matched(self, num_digits: int):
        """
        Feature: improved-pii-redaction, Property 5: Invalid Phone Length Rejection
        
        For any digit sequence with fewer than 10 digits, the pattern
        should not match it as a complete phone number.
        
        **Validates: Requirements 2.12**
        """
        # Generate a digit string of the specified length
        digits = "2" * num_digits  # Use 2s to avoid area code restrictions
        patterns = get_phone_patterns()
        
        # The pattern should not match this as a complete phone number
        # Note: We check that if there's a match, it's not the entire string
        for pattern in patterns:
            match = pattern.search(digits)
            if match:
                # If there's a match, it shouldn't be the entire string
                assert match.group() != digits, (
                    f"Pattern should not match {num_digits}-digit string '{digits}' "
                    f"as complete phone number, but matched '{match.group()}'"
                )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        num_extra_digits=st.integers(min_value=2, max_value=5),
    )
    def test_too_many_digits_not_matched_as_single(self, num_extra_digits: int):
        """
        Feature: improved-pii-redaction, Property 5: Invalid Phone Length Rejection
        
        For any digit sequence with more than 11 digits (10 + country code),
        the pattern should not match the entire sequence.
        
        **Validates: Requirements 2.12**
        """
        # Generate a digit string longer than valid phone (12+ digits)
        digits = "2" * (10 + num_extra_digits)
        patterns = get_phone_patterns()
        
        # The pattern should not match the entire string
        for pattern in patterns:
            match = pattern.search(digits)
            if match:
                # If there's a match, it shouldn't be the entire string
                assert match.group() != digits, (
                    f"Pattern should not match {len(digits)}-digit string as "
                    f"complete phone number, but matched '{match.group()}'"
                )
    
    def test_8_digit_number_not_matched(self):
        """
        Feature: improved-pii-redaction, Property 5: Invalid Phone Length Rejection
        
        8-digit numbers should not be matched as phone numbers.
        
        **Validates: Requirements 2.12**
        """
        digits = "12345678"
        patterns = get_phone_patterns()
        
        assert not matches_any_pattern(digits, patterns), (
            f"8-digit number '{digits}' should not be matched as phone"
        )
    
    def test_9_digit_number_not_matched(self):
        """
        Feature: improved-pii-redaction, Property 5: Invalid Phone Length Rejection
        
        9-digit numbers should not be matched as phone numbers.
        
        **Validates: Requirements 2.12**
        """
        digits = "123456789"
        patterns = get_phone_patterns()
        
        assert not matches_any_pattern(digits, patterns), (
            f"9-digit number '{digits}' should not be matched as phone"
        )


# =============================================================================
# Property 6: Boundary and Context Matching
# =============================================================================

class TestBoundaryAndContextMatching:
    """
    Property 6: Boundary and Context Matching
    
    *For any* valid email or phone number placed at the start of a string, 
    end of a string, or surrounded by common punctuation (parentheses, 
    brackets, quotes, commas), the corresponding patterns SHALL still match.
    
    **Validates: Requirements 3.2, 3.3**
    """
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(email=valid_standard_email())
    def test_email_at_start_of_string_matched(self, email: str):
        """
        Feature: improved-pii-redaction, Property 6: Boundary and Context Matching
        
        For any email at the start of a string, the pattern should match.
        
        **Validates: Requirements 3.2**
        """
        text = f"{email} is my email address"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(text, patterns), (
            f"Email at start of string '{text}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(email=valid_standard_email())
    def test_email_at_end_of_string_matched(self, email: str):
        """
        Feature: improved-pii-redaction, Property 6: Boundary and Context Matching
        
        For any email at the end of a string, the pattern should match.
        
        **Validates: Requirements 3.2**
        """
        text = f"Contact me at {email}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(text, patterns), (
            f"Email at end of string '{text}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        email=valid_standard_email(),
        punctuation=st.sampled_from(["(", ")", "[", "]", '"', "'", ",", ";"]),
    )
    def test_email_surrounded_by_punctuation_matched(
        self, email: str, punctuation: str
    ):
        """
        Feature: improved-pii-redaction, Property 6: Boundary and Context Matching
        
        For any email surrounded by punctuation, the pattern should match.
        
        **Validates: Requirements 3.3**
        """
        text = f"Contact: {punctuation}{email}{punctuation}"
        patterns = get_email_patterns()
        
        assert matches_any_pattern(text, patterns), (
            f"Email with punctuation '{text}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(phone=valid_phone_with_separators())
    def test_phone_at_start_of_string_matched(self, phone: str):
        """
        Feature: improved-pii-redaction, Property 6: Boundary and Context Matching
        
        For any phone at the start of a string, the pattern should match.
        
        **Validates: Requirements 3.2**
        """
        text = f"{phone} is my phone number"
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(text, patterns), (
            f"Phone at start of string '{text}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(phone=valid_phone_with_separators())
    def test_phone_at_end_of_string_matched(self, phone: str):
        """
        Feature: improved-pii-redaction, Property 6: Boundary and Context Matching
        
        For any phone at the end of a string, the pattern should match.
        
        **Validates: Requirements 3.2**
        """
        text = f"Call me at {phone}"
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(text, patterns), (
            f"Phone at end of string '{text}' should be matched"
        )
    
    @settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
    @given(
        phone=valid_phone_with_separators(),
        punctuation=st.sampled_from(["(", ")", "[", "]", '"', "'", ",", ";"]),
    )
    def test_phone_surrounded_by_punctuation_matched(
        self, phone: str, punctuation: str
    ):
        """
        Feature: improved-pii-redaction, Property 6: Boundary and Context Matching
        
        For any phone surrounded by punctuation, the pattern should match.
        
        **Validates: Requirements 3.3**
        """
        text = f"Call: {punctuation}{phone}{punctuation}"
        patterns = get_phone_patterns()
        
        assert matches_any_pattern(text, patterns), (
            f"Phone with punctuation '{text}' should be matched"
        )
