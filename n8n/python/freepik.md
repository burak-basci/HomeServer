## Freepik

**Platform Overview and AI Policy**

Freepik is another popular platform that is very welcoming to AI-generated content. You need to become a contributor to sell your images. All AI-generated content must be properly tagged.

**Upload Method**

Similar to Adobe Stock, Freepik does not have a public API for contributor uploads. The process involves using the web interface to upload your images and then uploading a CSV file with the metadata.

**Metadata Requirements**

Freepik uses a semicolon-separated CSV file for metadata. The required and optional columns are:

| Column | Description |
| :--- | :--- |
| `File name` | The exact filename of the image (e.g., `my-image.jpg`). |
| `Title` | The title of your image. |
| `Keywords` | A comma-separated list of relevant keywords. |
| `Prompt` | (Optional) The prompt used to generate the image. |
| `Model` | (Optional) The AI model used (e.g., `Midjourney 5`). |

**Important:** To tag your images as AI-generated, you can either use the "AI button" in the upload interface or include the `_ai_generated` tag in the `Keywords` column of your CSV.
