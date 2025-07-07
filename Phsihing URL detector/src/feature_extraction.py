import re
from urllib.parse import urlparse

def extract_features(url):
    features = {}

    features['URLLength'] = len(url)

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    features['NoOfSubDomain'] = max(domain.count('.') - 1, 0)

    ip_pattern = r'^\d{1,3}(\.\d{1,3}){3}$'
    features['IsDomainIP'] = 1 if re.match(ip_pattern, domain) else 0

    features['IsHTTPS'] = 1 if parsed.scheme == 'https' else 0

    special_chars = re.findall(r'[^a-zA-Z0-9:/?&=._-]', url)
    features['NoOfOtherSpecialCharsInURL'] = len(special_chars)

    features['NoOfQMarkInURL'] = url.count('?')

    obfuscated_chars = re.findall(r'[@%]', url)
    features['ObfuscationRatio'] = len(obfuscated_chars) / features['URLLength'] if features['URLLength'] > 0 else 0

    return features
