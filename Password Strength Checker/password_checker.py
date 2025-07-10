import re
from zxcvbn import zxcvbn

def count_transitions(password):
    transitions = 0
    last_type = None
    for c in password:
        if c.isupper():
            curr_type = 'U'
        elif c.islower():
            curr_type = 'L'
        elif c.isdigit():
            curr_type = 'D'
        else:
            curr_type = 'S'
        if last_type and curr_type != last_type:
            transitions += 1
        last_type = curr_type
    return transitions

def custom_score_calc(password):
    
    score = 0
    length = len(password)
    
    if length >= 8:
        score += 1

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    if has_upper and has_lower:
        score += 1

    has_digit = any(c.isdigit() for c in password)
    if has_digit:
        score += 1

    special_chars = '!@#$%^&*(),.?":{}|<>'
    has_special = any(c in special_chars for c in password)
    if has_special:
        score += 1

    return score


def custom_suggestions(password):
    suggestions = []
    length = len(password)
    if length < 8:
        suggestions.append("Use at least 8 characters.")
    if not re.search(r'[A-Z]', password):
        suggestions.append("Add uppercase letters.")
    if not re.search(r'[a-z]', password):
        suggestions.append("Add lowercase letters.")
    if not re.search(r'\d', password):
        suggestions.append("Add digits.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        suggestions.append("Add special characters.")
    return suggestions

def transitions_score(password):
    length = len(password)
    transitions = count_transitions(password)
    if length <= 6:
        if transitions >= 2:
            t_score = 2
        elif transitions == 1:
            t_score = 1
        else:
            t_score = 0
    elif length <= 12:
        if transitions >= 4:
            t_score = 2
        elif 2 <= transitions <= 3:
            t_score = 1
        else:
            t_score = 0
    else:
        if transitions >= 6:
            t_score = 2
        elif 3 <= transitions <= 5:
            t_score = 1
        else:
            t_score = 0
    return t_score, transitions

def transitions_suggestions(score):
    if score < 1:
        return ["Mix character types throughout the password for better security."]
    elif score == 1:
        return ["Increase the variety of character type changes for moderate improvement."]
    else:
        return []
    
def analyze_password(password):
    z_result = zxcvbn(password)
    z_score = z_result['score']  
    z_suggestions = z_result['feedback']['suggestions'] or []
    z_warning = z_result['feedback']['warning']
    z_cracktimesdisplay = z_result['crack_times_display']
    z_guesses = z_result['guesses']
    z_sequence = z_result['sequence']

    custom_score = custom_score_calc(password)
    custom_sugg = custom_suggestions(password)


    t_score, transitions_count = transitions_score(password)
    transitions_sugg = transitions_suggestions(t_score)

    final_score = z_score * 16 + custom_score * 7 + t_score * 4

    if 100 >= final_score > 75:
        label = "Very Strong"
    elif 75 >= final_score > 60:
        label = "Strong"
    elif 60 >= final_score > 30:
        label = "Moderate"
    else:
        label = "Weak"

    sequence_details = []
    for seq in z_sequence:
        detail = {k: v for k, v in seq.items()}
        sequence_details.append(detail)

    return {
        'z_score': z_score,
        'z_suggestions': z_suggestions,
        'custom_score': custom_score,
        'custom_suggestions': custom_sugg,
        'transitions score': t_score,
        'transitions_suggestions': transitions_sugg,
        'final_score': final_score,
        'label': label,
        'crack_time': z_cracktimesdisplay.get('online_throttling_100_per_hour', 'N/A'),
        'warning': z_warning,
        'guesses': z_guesses,
        'sequence_details': sequence_details
    }



