from diff_match_patch import diff_match_patch

def add_missing_words(text_a, text_b):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(text_a, text_b)
    print(diffs)
    added_words = set()
    for diff in diffs:
        if diff[0] == -1:  # Check for deletion in text_b
            deleted_words = diff[1].split()
            if len(deleted_words) >= 3:  # Check if three consecutive words are deleted
                added_words.update(deleted_words)

    new_text_b = text_b.split()
    for i, word in enumerate(text_a.split()):
        if word in added_words:
            new_text_b.insert(i, word)

    return ' '.join(new_text_b)


text_a = "he she text This is a sample text to compare."
text_b = "text to test."

new_text_b = add_missing_words(text_a, text_b)
print(new_text_b)
