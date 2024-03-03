from difflib import SequenceMatcher


def text_diff(text1, text2):
    """
    Compare two texts and print the differences, ignoring whitespace and line breaks.
    """
    # Preprocess texts to remove whitespace and line breaks
    text1_stripped = ''.join(text1.split())
    text2_stripped = ''.join(text2.split())

    print(text2_stripped)

    # Perform comparison
    matcher = SequenceMatcher(None, text1_stripped, text2_stripped)
    offset = 0
    diff_result = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            print('Replace "{}" from {} to {} with "{}" from {} to {}'.format(
                text1[i1 + offset:i2 + offset], i1 + offset, i2 + offset, text2[j1:j2], j1, j2))
            offset += len(text2[j1:j2]) - len(text1[i1 + offset:i2 + offset])
            diff_result.append(('replace', text1[i1:i2], text2[j1:j2]))
        elif tag == 'delete':
            print('Delete "{}" from {} to {}'.format(text1[i1 + offset:i2 + offset], i1 + offset, i2 + offset))
            offset -= len(text1[i1 + offset:i2 + offset])
            diff_result.append(('delete', text1[i1:i2]))
        elif tag == 'insert':
            print('Insert "{}" from {} to {}'.format(text2[j1:j2], i1 + offset, i2 + offset))
            offset += len(text2[j1:j2])
            diff_result.append(('insert', text2[j1:j2]))
        elif tag == 'equal':
            pass

    return diff_result

def add_deleted_text(text1, text2):
    """
    Add back the deleted text from text1 into text2.
    """
    diff_result = text_diff(text1, text2)
    offset = 0
    reconstructed_text = text2
    for diff_type, text in diff_result:
        if diff_type == 'delete':
            reconstructed_text = reconstructed_text[:offset] + text + reconstructed_text[offset:]
        elif diff_type == 'equal' or diff_type == 'replace':
            offset += len(text)
    return reconstructed_text
# Example usage:
text1 = "Python is an interpreted high-level \n prog ramming lan guage"
text2 = "Python is a programming language"
reconstructed_text = add_deleted_text(text1, text2)
print(reconstructed_text)