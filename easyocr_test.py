"""
    Installation::

    Get files from:
        - https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/english_g2.zip             (83MB)
        - https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip    (15MB)

    Unzip to ~/.EasyOCR/model directory
"""

import easyocr

DEBUG: bool = False

def debug_print(string: str):
    global DEBUG

    if DEBUG:
        print(string)

def main():
    # Text lines may be broken. we will try to re-assemble.
    # Bounding boxes for each line may or may not contain capitol letters and/or special chars.
    # In general the upper coordinate between two related strings may be about 30% of the text height.
    # i.e. if Lower case was 30 bits in height, upper/special char may be 40 chars.
    #      therefore the upp coordinates for the two may be, lets say, 250 and 275
    #      being within the threshold, we would connect the two strings as related.
    # This is a bit of a guessing game, and may result in non-related strings being joined.
    # But in general, if the difference between two adjoining bounding boxes is within
    # this threshold, it is a good probability that they should be joined.
    # Default, start with 0.3 --> 30% of bounding box height for given text blocks.
    bounding_box_threshold = 0.3

    reader = easyocr.Reader(['en'],  model_storage_directory='/Users/amoringello/.EasyOCR/model', download_enabled=False)
    result = reader.readtext('images/pycharm_screenshot.png', paragraph=False)

    text_lines: list[str] = []
    bbox_prior: list[list[int]] = [[0, 0], [0, 0], [0, 0], [0, 0]]

    current_line_text: str = ''
    for bbox, text, prob in result:
        # Bounding Box is co-ords in clockwise manner:
        #   [(Upper Left X,Y), (Upper Right X,Y), (Lower Right X,Y), (Lower Left X,Y)]
        (ul, ur, lr, lf) = bbox
        (ul_prior, ur_prior, lr_prior, lf_prior) = bbox_prior
        current_line_threshold: float = (lf[1] - ul[1]) * bounding_box_threshold
        # Check Y coord of ul vs ul_prior
        if abs(ul[1] - ul_prior[1]) < current_line_threshold:
            # within threshold, connect text segments with a space as a single line
            current_line_text += f' {text}'
            debug_print(f'Connected: {current_line_text}')
        else:
            # not within threshold, starting new text segment (line)
            text_lines.append(current_line_text)
            current_line_text = text
            debug_print(f'New Line: {current_line_text}')

        # Regardless of threshold, store bounding box as new prior
        bbox_prior = bbox

        # If current bbox is within threshold of prior line, add to current_line_text

    for line in text_lines:
        print(line)

if __name__ == "__main__":
    main()