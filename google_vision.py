def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    image_context = vision.ImageContext(language_hints=["en-t-i0-handwrit"])
    response = client.document_text_detection(image=image, image_context=image_context)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            #print(f"\nBlock confidence: {block.confidence}\n")

            for paragraph in block.paragraphs:
                #print("Paragraph confidence: {}".format(paragraph.confidence))
                word_text = ""
                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    print(
                        "Word text: {} (confidence: {})".format(
                            word_text, word.confidence
                        )
                    )
                return word_text
                    # for symbol in word.symbols:
                    #     print(
                    #         "\tSymbol: {} (confidence: {})".format(
                    #             symbol.text, symbol.confidence
                    #         )
                    #     )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )


def detect_document_uri(uri):
    """Detects document features in the file located in Google Cloud
    Storage."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print(f"\nBlock confidence: {block.confidence}\n")

            for paragraph in block.paragraphs:
                print("Paragraph confidence: {}".format(paragraph.confidence))

                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    print(
                        "Word text: {} (confidence: {})".format(
                            word_text, word.confidence
                        )
                    )

                    for symbol in word.symbols:
                        print(
                            "\tSymbol: {} (confidence: {})".format(
                                symbol.text, symbol.confidence
                            )
                        )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

from google.cloud import vision

client_options = {"api_endpoint": "eu-vision.googleapis.com"}

client = vision.ImageAnnotatorClient(client_options=client_options)

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/said/.config/gcloud/application_default_credentials.json"

# Directory path containing the images
image_directory = './custom_data/images'

# Output file path for saving the predictions
output_file = 'predictions.txt'

# Initialize the output file
with open(output_file, 'w') as file:
    file.write('Image Name\tPredictions\n')

# Loop over all images in the directory
for filename in os.listdir(image_directory):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(image_directory, filename)
        
        # Perform text detection on the image
        try:
            predictions = detect_document(image_path)
        except Exception as e:
            print(f"Error processing image {filename}: {str(e)}")
            continue
        
        # Write the predictions to the output file
        with open(output_file, 'a') as file:
            file.write(f"{filename}\t{predictions}\n")
