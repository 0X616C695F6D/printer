import os
import unittest
from pdf_generation import pdf_creator
from PIL import Image as PILImage

class TestPDFCreator(unittest.TestCase):
    def test_create_newspaper_pdf(self):
        # Create dummy content with a sample PIL image.
        dummy_image = PILImage.new('RGB', (100, 100), color='blue')
        content = {
            'stock': {
                'headline': "Stock Market Soars",
                'summary': "Major indices hit record highs in today's trading session.",
                'image': dummy_image,
            },
            'astronomy': {
                'headline': "Astronomy Breakthrough",
                'summary': "Scientists discover a new exoplanet with unique characteristics.",
                'image': dummy_image,
            },
            'tech': {
                'headline': "Tech Innovation",
                'summary': "A leading company unveils its latest AI-powered product.",
                'image': dummy_image,
            }
        }
        output_path = "test_newspaper.pdf"
        
        # Generate the PDF.
        pdf_creator.create_newspaper_pdf(content, output_path)
        
        # Verify that the PDF file was created and has content.
        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)
        
        # Clean up after test.
        os.remove(output_path)

if __name__ == '__main__':
    unittest.main()

