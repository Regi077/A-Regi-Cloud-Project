from parse_utils import parse_doc_to_chunks, extract_rules_with_llm

chunks = parse_doc_to_chunks('your_test_file.txt')
print("Chunks:", chunks)
rules = extract_rules_with_llm(chunks)
print("Rules returned:", rules)
