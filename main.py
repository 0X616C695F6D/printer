import logging
import time
from data_retrieval import nasa_image, science_daily, nasa_astronomy
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
    
    # Grab NASA image of the day
    try:
        bw_nasa_image = nasa_image.fetch_nasa_image_of_the_day()
        if bw_nasa_image:
            content['front_image'] = [{
                'summary': '', 
                'image': bw_nasa_image
            }]
    except Exception as e:
        logger.warning(f"Couldn't get NASA image of the day: {e}")


    # Process NASA Astronomy Articles
    try:
        nasa_articles = nasa_astronomy.fetch_latest_astronomy_articles()
        
        # Combine the full content of all articles into one string.
        all_articles_content = " ".join(
            article.get('content', '').strip() 
            for article in nasa_articles if article.get('content')
        )
        # Generate a single overall summary for the concatenated content.
        overall_summary = retry(summarizer.summarize_text, all_articles_content, 250)
        
        # Trim to last complete sentence
        last_period = overall_summary.rfind(".")
        if last_period != -1: overall_summary = overall_summary[:last_period + 1]

        # Also strip trailing whitespace
        overall_summary = overall_summary.strip()

        content['NASA & SPACE'] = [{
            'summary': overall_summary,
            'image': None
        }]
        logger.info("Generated NASA summary column")
    except Exception as e:
        logger.error(f"Failed to process astronomy articles: {e}")
        
    # Process Science Daily Articles
    try:
        latest_engineering_news = science_daily.fetch_latest_engineering_articles()
        
        # Generate summary
        overall_summary = retry(summarizer.summarize_text, latest_engineering_news['content'], 250)
        
        # Trim to last complete sentence
        last_period = overall_summary.rfind(".")
        if last_period != -1:
            overall_summary = overall_summary[:last_period + 1]

        # Also strip trailing whitespace
        overall_summary = overall_summary.strip()
        
        content['EVERYDAY SCIENCE'] = [{
            'summary': overall_summary,
            'image': None
        }]
        logger.info("Generated ScienceDaily summary column.")
    except Exception as e:
        logger.error(f"Failed to process science daily: {e}")
        
    # Generate the final PDF.
    try:
        output_path = "newspaper.pdf"
        retry(pdf_creator.create_newspaper_pdf, content, output_path)
        logger.info(f"PDF generated successfully at {output_path}")
    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}")

if __name__ == "__main__":
    main()
