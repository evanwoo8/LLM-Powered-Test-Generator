

def add(a, b):
    """Returns the sum of two numbers."""
    return a + b

def is_even(n):
    """Returns True if the number is even, False otherwise."""
    return n % 2 == 0

def divide(a, b):
    """Divides a by b and handles division by zero."""
    if b == 0:
        return None
    return a / b

def greet(name):
    """Returns a greeting for the given name."""
    return f"Hello, {name}!"

def fibonacci(n, memo=None):
    """
    Returns the n-th Fibonacci number using recursion with memoization.
    Raises ValueError if n is negative.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        memo[n] = n
    else:
        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]

def word_frequencies(text, min_length=1):
    """
    Returns a dictionary of word -> count for all words in the given text.
    Only includes words whose length is >= min_length.
    Case-insensitive.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    words = text.lower().split()
    freqs = {}
    for word in words:
        word = ''.join(ch for ch in word if ch.isalnum())  # strip punctuation
        if len(word) >= min_length and word:
            freqs[word] = freqs.get(word, 0) + 1
    return freqs