from colorama import Back, Style
import re

def CensorInput(comment):
    """
    Censor inappropriate content in user comments
    Returns: (is_appropriate, censored_comment, found_words)
    - is_appropriate: Boolean, True if comment is clean
    - censored_comment: Original comment with inappropriate words censored
    - found_words: List of inappropriate words found (empty if clean)
    """
    curse_words = {
        'fuck': ['fck', 'fuk', 'fvck', 'f*ck', 'f**k'],
        'shit': ['sht', 'sh*t', 's**t', 'sh1t'],
        'pussy': ['puss', 'p*ssy', 'p**sy'],
        'sex': ['s3x', 's*x', 'seks'],
        'ass': ['a$$', 'a**', 'as$'],
        'bitch': ['b*tch', 'b**ch', 'bi*ch'],
        'dick': ['d*ck', 'd**k', 'd1ck'],
        'cunt': ['c*nt', 'c**t']
    }

    # Convert to lowercase for case-insensitive matching
    comment_lower = comment.lower()
    found_words = []
    censored_comment = comment

    # Build comprehensive pattern for all curse words and variations
    all_patterns = []
    for word, variations in curse_words.items():
        all_variations = [word] + variations
        # Match whole words with common variations
        pattern = r'\b(' + '|'.join(re.escape(v) for v in all_variations) + r')\b'
        all_patterns.append(pattern)

    # Combine all patterns into one
    master_pattern = '|'.join(all_patterns)

    # Find all matches
    matches = re.finditer(master_pattern, comment_lower)

    for match in matches:
        found_word = match.group()
        found_words.append(found_word)
        # Censor the word in original comment (preserving case)
        start, end = match.span()
        original_word = comment[start:end]
        censored_word = original_word[0] + '*' * (len(original_word) - 1)
        censored_comment = censored_comment.replace(original_word, censored_word)

    is_appropriate = len(found_words) == 0

    return is_appropriate, censored_comment, found_words

# Example usage in CBV:
"""
from django.views.generic import CreateView
from .models import Comment

class CommentCreateView(CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        comment_text = form.cleaned_data['content']

        # Use the censor function
        is_appropriate, censored_content, found_words = censor_comment(comment_text)

        if not is_appropriate:
            # Add error message
            form.add_error('content', f'Comment contains inappropriate words: {", ".join(found_words)}')
            return self.form_invalid(form)

        # Save with censored content if you want automatic censoring
        form.instance.content = censored_content
        return super().form_valid(form)
"""

# Quick test
if __name__ == '__main__':
    test_comments = [
        "This is a nice comment",
        "What the fuck are you doing?",
        "This is some bullshit",
        "Have a nice day!",
        "You're a b*tch for saying that"
    ]

    for comment in test_comments:
        appropriate, censored, found = CensorInput(comment)
        print(f"Original: {comment}")
        print(f"Appropriate: {appropriate}")
        print(f"Censored: {censored}")
        print(f"Found: {found}")
        print("-" * 50)