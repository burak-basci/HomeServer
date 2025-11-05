## Adobe Stock

**Platform Overview and AI Policy**

Adobe Stock is a major player in the stock photo industry. They accept AI-generated images, but you must have all the necessary rights to the images, and you need to flag them as "Generated with AI" during the submission process.

**Upload Method**

Adobe Stock does not have a public API for contributors to upload content. Therefore, the most effective way to automate uploads is by using a headless browser library like **Selenium** or **Playwright** to script the interactions with the contributor portal. The general workflow is:

1.  **Log in** to the Adobe Stock contributor portal.
2.  **Navigate** to the upload section.
3.  **Upload** your images.
4.  **Upload a CSV file** containing the metadata for your images.

**Metadata Requirements**

You can prepare a CSV file with the following columns to streamline the metadata submission process. The CSV file should be UTF-8 encoded.

| Column | Description |
| :--- | :--- |
| `Filename` | The exact filename of the image (e.g., `my-image.jpg`). |
| `Title` | A descriptive title for your image (5-7 words recommended). |
| `Keywords` | A comma-separated list of up to 49 keywords. |
| `Category` | The numerical ID of the category that best fits your image. |

**Adobe Stock Category IDs**

Here is the list of categories and their corresponding IDs for use in your CSV file:

| ID | Category |
| :--- | :--- |
| 1 | Animals |
| 2 | Buildings and Architecture |
| 3 | Business |
| 4 | Drinks |
| 5 | The Environment |
| 6 | States of Mind |
| 7 | Food |
| 8 | Graphic Resources |
| 9 | Hobbies and Leisure |
| 10 | Industry |
| 11 | Landscape |
| 12 | Lifestyle |
| 13 | People |
| 14 | Plants and Flowers |
| 15 | Culture and Religion |
| 16 | Science |
| 17 | Social Issues |
| 18 | Sports |
| 19 | Technology |
| 20 | Transport |
| 21 | Travel |
