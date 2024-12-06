import json
import os
from typing import List, Dict, Any
import requests
from valyu_pipeline.types.upload_types import UploadUrls
import concurrent.futures
import time
from tqdm import tqdm
import re

class PDFProcessor:
    """
    Main class for processing PDFs through the Valyu AI pipeline.
    """
    
    def __init__(
        self,
        base_url: str = "https://demo.api.valyu.network"
    ):
        """
        Initialize the PDF processor.

        Args:
            api: API endpoint
        """
        self.base_url = base_url
        
        # Get API key from environment variable
        self.api_key = os.environ.get('VALYU_API_KEY')
        if not self.api_key:
            raise ValueError("VALYU_API_KEY must be set in environment variable")
        

    def start_job(self, folder_path: str, output_dir: str = "results") -> Dict[str, Dict[str, Any]]:
        """
        Run all PDFs in a folder through the Valyu data pipeline.
        
        Args:
            folder_path: Path to folder containing PDFs
            output_dir: Directory to store results (default: "results")
        """
        # Get list of all PDFs in folder
        file_paths = self._get_file_paths(folder_path)

        # 1. Get presigned URL for folder upload
        try:
            upload_urls = self._get_upload_urls(file_paths)
        except ValueError as e:
            raise ValueError(f"Error getting upload URLs: {e}")

        # 2. Upload folder of PDFs
        try:
            self._upload_pdfs(upload_urls, folder_path, file_paths)
        except ValueError as e:
            raise ValueError(f"Error uploading PDFs: {e}")

        # 3. Start the job
        try:
            self._start_job(upload_urls.job_id)
        except ValueError as e:
            raise ValueError(f"Error starting job: {e}")

        # 4. Poll job status until complete
        results = self._poll_job_status(upload_urls.job_id, len(file_paths))
        
        # 5. Download results
        self._download_results(results, output_dir)
        
        return results

    def _poll_job_status(self, job_id: str, total_pdfs: int) -> Dict[str, Dict[str, Any]]:
        """
        Poll job status until completion, displaying progress bars.
        Shows progress for both PDFs and pages through OCR and image detection.
        """
        # Create progress bars for PDFs
        pdf_ocr_pbar = tqdm(total=total_pdfs, desc="OCR (PDFs)")
        pdf_img_pbar = tqdm(total=total_pdfs, desc="Image Extraction (PDFs)")
        
        # We'll initialize page progress bars once we know the total
        page_ocr_pbar = None
        page_img_pbar = None
        
        last_ocr_pdfs = 0
        last_ocr_pages = 0
        last_img_pdfs = 0
        last_img_pages = 0
        final_processing_message_printed = False

        while True:
            try:
                response = requests.post(
                    f"{self.base_url}/v1/jobs/status",
                    headers={"x-api-key": self.api_key},
                    json={"job_id": job_id}
                )
                response.raise_for_status()
                data = response.json()

                # Initialize or update page progress bars if we have total pages
                if 'status.total_pages' in data:
                    total_pages = int(data['status.total_pages'])
                    if total_pages > 0:  # Only initialize if we have a real page count
                        if page_ocr_pbar is None:
                            page_ocr_pbar = tqdm(total=total_pages, desc="OCR (pages)")
                            page_img_pbar = tqdm(total=total_pages, desc="Image Extraction (pages)")
                        else:
                            # Update total if it changed
                            page_ocr_pbar.total = total_pages
                            page_img_pbar.total = total_pages
                
                # Update PDF progress bars
                if 'status.ocr_completed_pdfs' in data:
                    ocr_pdfs = int(data['status.ocr_completed_pdfs'])
                    pdf_ocr_pbar.update(ocr_pdfs - last_ocr_pdfs)
                    last_ocr_pdfs = ocr_pdfs

                if 'status.image_completed_pdfs' in data:
                    img_pdfs = int(data['status.image_completed_pdfs'])
                    pdf_img_pbar.update(img_pdfs - last_img_pdfs)
                    last_img_pdfs = img_pdfs

                # Update page progress bars
                if page_ocr_pbar is not None:
                    if 'status.ocr_completed_pages' in data:
                        ocr_pages = int(data['status.ocr_completed_pages'])
                        page_ocr_pbar.update(ocr_pages - last_ocr_pages)
                        last_ocr_pages = ocr_pages

                        # Check if OCR pages progress bar is full and print "Final processing..." only once
                        if ocr_pages == total_pages and not final_processing_message_printed:
                            print("\nFinal processing...")
                            final_processing_message_printed = True

                    if 'status.image_completed_pages' in data:
                        img_pages = int(data['status.image_completed_pages'])
                        page_img_pbar.update(img_pages - last_img_pages)
                        last_img_pages = img_pages

                # Check for completion and results
                if ('status.processing_completed' in data and 
                    data['status.processing_completed'] and 
                    'status.presigned_urls' in data):
                    
                    # Close all progress bars
                    pdf_ocr_pbar.close()
                    pdf_img_pbar.close()
                    if page_ocr_pbar:
                        page_ocr_pbar.close()
                    if page_img_pbar:
                        page_img_pbar.close()
                    
                    # Parse the presigned URLs directly from the response
                    presigned_urls = {}
                    raw_urls = data['status.presigned_urls']
                    for pdf_name, url_data in raw_urls.items():
                        # Handle null values for image_url
                        image_url = url_data.get('image_url')
                        if isinstance(image_url, dict) and image_url.get('NULL') is True:
                            image_url = None
                        
                        # Get text URL directly
                        text_url = url_data.get('text_url')

                        markdown_url = url_data.get('markdown_url', None)
                        
                        presigned_urls[pdf_name] = {
                            'image_url': image_url,
                            'text_url': text_url,
                            'markdown_url': markdown_url
                        }
                    return presigned_urls

                # Check for errors
                if 'status.error' in data:
                    raise ValueError(f"Job failed: {data['status.error']}")

            except requests.exceptions.RequestException as e:
                raise ValueError(f"Error polling job status: {e}")
            except ValueError as e:
                # Handle potential conversion errors
                raise ValueError(f"Error processing status values: {e}")

            time.sleep(1)  # Poll every second

    def _get_file_paths(self, folder_path: str) -> Dict[str, str]:
        """
        Get list of all PDFs in folder with sanitized filenames.
        Returns a dictionary mapping sanitized names to original names.
        """
        def sanitize_filename(filename: str) -> str:
            # Replace spaces and special characters with underscores
            # Keep alphanumeric chars, dots, and underscores
            sanitized = re.sub(r'[^\w\-\.]', '_', filename)
            return sanitized
        
        return {sanitize_filename(f): f for f in os.listdir(folder_path) if f.endswith('.pdf')}

    def _get_upload_urls(self, file_paths: List[str]) -> UploadUrls:
        """
        # Retrieve presigned URLs for uploading PDF files to the Valyu API via a POST request. 
        # The returned URLs allow direct uploads to cloud storage without exposing the API key.

        Args:
            file_paths (List[str]): List of PDF file paths to upload.

        Returns:
            UploadUrls: Contains presigned URLs and job ID.

        Raises:
            ValueError: If the API request fails or the response is unexpected.
        """
        try:
            response = requests.post(
                f"{self.base_url}/v1/files/upload",
                headers={"x-api-key": self.api_key},
                json={"files": file_paths}
            )
            response.raise_for_status()  # Raise an error for bad responses
            upload_urls = response.json()
            return UploadUrls(**upload_urls)
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except Exception as err:
            raise ValueError(f"An error occurred: {err}")  # Handle other errors

    def _upload_pdfs(self, upload_urls: UploadUrls, folder_path: str, file_paths: Dict[str, str]) -> None:
        """
        Upload PDFs to the Valyu API using the presigned URLs.
        """
        def upload_file(sanitized_path: str) -> None:
            original_path = file_paths[sanitized_path]
            with open(f"{folder_path}/{original_path}", 'rb') as file:
                response = requests.put(upload_urls.presigned_urls[sanitized_path], data=file)
                response.raise_for_status()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(upload_file, file_paths.keys())

    def _start_job(self, job_id: str) -> None:
        """
        Initiates a job using the provided job ID.

        Args:
            job_id (str): The ID of the job to start.

        Raises:
            ValueError: If the API request fails or the response is not successful.
        """
        try:
            response = requests.post(
                f"{self.base_url}/v1/jobs/start",
                headers={"x-api-key": self.api_key},
                json={"job_id": job_id}
            )
            response.raise_for_status()  # Raise an error for bad responses
        except requests.exceptions.HTTPError as http_err:
            raise ValueError(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except Exception as err:
            raise ValueError(f"An error occurred: {err}")  # Handle other errors

    def _download_results(self, presigned_urls: Dict[str, Dict[str, str]], output_dir: str = "results") -> None:
        """
        Download files from presigned URLs and store them in the results directory.
        
        Args:
            presigned_urls: Dictionary of PDF names and their presigned URLs
            output_dir: Directory to store the downloaded files (default: "results")
        """
        # Create results directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        print("\nSaving results...")
        for pdf_name, urls in presigned_urls.items():
            # Create subdirectory for each PDF
            pdf_dir = os.path.join(output_dir, pdf_name.replace('.pdf', ''))
            os.makedirs(pdf_dir, exist_ok=True)
            
            # Download text results
            if urls['text_url']:
                text_path = os.path.join(pdf_dir, 'text.txt')
                response = requests.get(urls['text_url'])
                response.raise_for_status()
                with open(text_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Saved text for {pdf_name}")
                
            # Download image results if they exist
            if urls['image_url']:
                image_path = os.path.join(pdf_dir, 'images.parquet')
                response = requests.get(urls['image_url'])
                response.raise_for_status()
                with open(image_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Saved images for {pdf_name}")

            if urls['markdown_url']:
                markdown_path = os.path.join(pdf_dir, 'markdown.md')
                response = requests.get(urls['markdown_url'])
                response.raise_for_status()
                with open(markdown_path, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Saved markdown for {pdf_name}")

