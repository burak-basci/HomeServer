## Dreamstime

**Platform Overview and AI Policy**

Dreamstime accepts AI-generated images, but with some restrictions. You must categorize them correctly and you cannot upload realistic AI-generated human faces.

**Upload Method**

Dreamstime does not have a contributor upload API. The primary method for bulk uploads is **FTP (File Transfer Protocol)**. You can use an FTP client like FileZilla to upload your images and a corresponding CSV file for the metadata.

**FTP Details:**

*   **Host:** `upload.dreamstime.com`
*   **Username:** Your Dreamstime user ID
*   **Password:** Your Dreamstime password
*   **Port:** 21 (or leave blank)
*   **Transfer Mode:** Passive

**Metadata Requirements**

Dreamstime provides official CSV templates for metadata within the contributor's account. It is highly recommended to download and use these templates to ensure the correct format. While the exact format is not publicly documented, the CSV file will contain columns for:

*   `Filename`
*   `Title`
*   `Description`
*   `Keywords`
*   `Categories`

**Important:** You must categorize your AI-generated images under **"Illustrations and Clip Art/AI generated"**. You should also mention in the image description that it was created using AI.
