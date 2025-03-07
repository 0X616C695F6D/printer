import logging
import time
from data_retrieval import yahoo_finance, nasa_astronomy, mit_tech
from text_processing import summarizer
from image_processing import image_handler
from pdf_generation import pdf_creator

def retry(func, *args, retries=3, delay=1, backoff=2, **kwargs):
    """
    Helper function to retry a callable on failure with exponential backoff.
    """
    current_delay = delay
    for attempt in range(retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            if attempt < retries - 1:
                time.sleep(current_delay)
                current_delay *= backoff
            else:
                raise

def main():
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info("Newspaper Generator started.")
    
    content = {}

    # Process NASA Astronomy Articles
    try:
        nasa_articles = nasa_astronomy.fetch_latest_astronomy_articles()
        
        # Combine the full content of all articles into one string.
        all_articles_content = " ".join(
            article.get('content', '').strip() 
            for article in nasa_articles if article.get('content')
        )
        # Generate a single overall summary for the concatenated content.
        overall_summary = retry(summarizer.summarize_text, all_articles_content, 300)
        # Make sure to wrap the result in a dictionary.
        content['astronomy'] = [{
            'summary': overall_summary,
            'image': None
        }]
        logger.info("Generated overall summary for all articles.")
    except Exception as e:
        logger.error(f"Failed to process astronomy articles: {e}")
        
    

    
    # Generate the final PDF.
    try:
        output_path = "newspaper.pdf"
        retry(pdf_creator.create_newspaper_pdf, content, output_path)
        logger.info(f"PDF generated successfully at {output_path}")
    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    main()
