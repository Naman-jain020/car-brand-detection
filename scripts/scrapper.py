"""
Simple web scraper for car images without Selenium
Uses requests and BeautifulSoup for static content scraping
"""

import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin

def scrape_flickr_simple(url, save_dir, limit=50):
    """
    Scrape images from Flickr using simple requests (no Selenium)
    
    Args:
        url: Flickr group pool URL
        save_dir: Directory to save images
        limit: Maximum number of images to scrape
    
    Returns:
        Number of images successfully scraped
    """
    # Create save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Clear existing images
    print(f"Clearing existing images from {save_dir}...")
    for file in os.listdir(save_dir):
        if file.endswith(('.jpg', '.jpeg', '.png')):
            try:
                os.remove(os.path.join(save_dir, file))
            except Exception as e:
                print(f"Could not remove {file}: {e}")
    
    # Set up headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        print(f"Fetching page: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        print(f"Parsing HTML content...")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all image elements
        img_tags = soup.find_all('img')
        print(f"Found {len(img_tags)} img tags")
        
        count = 0
        attempted = 0
        
        for img in img_tags:
            if count >= limit:
                break
            
            # Get image source from various possible attributes
            img_url = (img.get('src') or 
                      img.get('data-src') or 
                      img.get('data-defer-src'))
            
            if not img_url:
                continue
            
            # FIX: Add https: if URL starts with //
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            
            # Filter for Flickr CDN images only
            if not ('staticflickr' in img_url or 'live.staticflickr' in img_url):
                continue
            
            # Skip very small images (thumbnails, icons)
            if any(size in img_url for size in ['_t.', '_s.', '_q.']):
                continue
            
            # Try to get larger version if available
            if '_m.' in img_url:
                img_url = img_url.replace('_m.', '_b.')
            elif '_n.' in img_url:
                img_url = img_url.replace('_n.', '_b.')
            elif '_w.' in img_url:
                img_url = img_url.replace('_w.', '_b.')
            
            attempted += 1
            
            try:
                print(f"Downloading image {count + 1}/{limit}...")
                img_response = requests.get(img_url, headers=headers, timeout=10)
                img_response.raise_for_status()
                
                # Check if response is actually an image
                content_type = img_response.headers.get('content-type', '')
                if 'image' not in content_type:
                    print(f"✗ Not an image: {content_type}")
                    continue
                
                # Determine file extension
                ext = '.jpg'
                if '.png' in img_url.lower() or 'png' in content_type:
                    ext = '.png'
                elif '.jpeg' in img_url.lower():
                    ext = '.jpeg'
                
                # Save image
                img_path = os.path.join(save_dir, f'car_{count}{ext}')
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"✓ Saved: {img_path}")
                count += 1
                
                # Small delay to be respectful to the server
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"✗ Failed to download image: {e}")
                continue
            except Exception as e:
                print(f"✗ Error saving image: {e}")
                continue
        
        print(f"\n{'='*50}")
        print(f"Scraping complete!")
        print(f"Successfully scraped: {count} images")
        print(f"Attempted downloads: {attempted}")
        print(f"{'='*50}\n")
        
        return count
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        raise Exception(f"Failed to fetch page: {str(e)}")
    except Exception as e:
        print(f"Scraping error: {e}")
        raise Exception(f"Scraping failed: {str(e)}")


def scrape_from_multiple_sources(save_dir, limit=50):
    """
    Alternative: Scrape from multiple car image sources
    Can be used as a backup if Flickr scraping fails
    """
    sources = [
        "https://www.flickr.com/groups/carexpressions/pool/",
        "https://www.flickr.com/groups/carphotography/pool/",
    ]
    
    total_scraped = 0
    per_source = limit // len(sources)
    
    for source_url in sources:
        if total_scraped >= limit:
            break
        
        try:
            scraped = scrape_flickr_simple(
                url=source_url,
                save_dir=save_dir,
                limit=min(per_source, limit - total_scraped)
            )
            total_scraped += scraped
        except Exception as e:
            print(f"Failed to scrape from {source_url}: {e}")
            continue
    
    return total_scraped


if __name__ == "__main__":
    # Test the scraper
    print("Testing scraper...")
    count = scrape_flickr_simple(
        url="https://www.flickr.com/groups/carexpressions/pool/",
        save_dir="../static/raw_images",
        limit=10
    )
    print(f"Test complete. Scraped {count} images.")
