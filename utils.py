import chardet


def detect_encoding(filename: str) -> str:
    detector = chardet.UniversalDetector()
    with open(filename, 'rb') as f:
        for i in f:
            detector.feed(i)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']
