---
title: Visualizing Download Progress with tqdm in Python
slug: visualizing-download-progress-with-tqdm-in-python
date: 2024-09-14
summary: Learn to visualize file download progress in Python using tqdm. This tutorial covers basic implementation, error handling, and advanced techniques for improving user experience in CLI applications.
language: en
topic: python
---

## Introduction

In the world of programming, especially when working with file downloads, it's crucial to provide users with a clear indication of the operation's progress. This not only improves the user experience but also helps avoid uncertainty about whether the program is functioning correctly. This is where the Python `tqdm` library comes into play.

The `tqdm` library is a powerful and flexible tool that allows for easy and efficient display of progress bars in the command line. In this tutorial, we'll learn how to use `tqdm` to visualize the progress of file downloads, providing a more informative and pleasant experience for users of our programs.

## Installation

Before we begin, we need to install the necessary libraries. We'll use `tqdm` for the progress bar and `requests` to make HTTP requests. You can install them using pip:

```bash
pip install tqdm requests
```

## Implementing the Download Function

Now, let's create a `download` function that downloads a file from a given URL and displays a progress bar using `tqdm`. Here's the complete code:

```python
# tqdm_download.py

import requests
from tqdm import tqdm

def download(url, dest_path):
    response = requests.get(url, stream=True, allow_redirects=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(dest_path, 'wb') as file, tqdm(
        desc=dest_path,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
```

### Detailed Explanation

Let's break down the `download` function to understand how it works:

**Importing libraries**: 


```python
import requests
from tqdm import tqdm
```

We import `requests` to make the HTTP request and `tqdm` for the progress bar.

**Function definition**:


```python
def download(url, dest_path):
```

The function takes two arguments: `url` (the URL of the file to download) and `dest_path` (the path where the file will be saved).

**Making the HTTP request**:


```python
response = requests.get(url, stream=True, allow_redirects=True)
```

We use `requests.get()` with `stream=True` to get the content in chunks and `allow_redirects=True` to follow redirects if any.

**Getting the total file size**:

  
```python
total_size = int(response.headers.get('content-length', 0))
```

We extract the total file size from the 'content-length' header of the HTTP response.

**Opening the destination file and setting up tqdm**:


```python
with open(dest_path, 'wb') as file, tqdm(
   desc=dest_path,
   total=total_size,
   unit='B',
   unit_scale=True,
   unit_divisor=1024,
) as bar:
```

We open the destination file in binary write mode and configure `tqdm` with various parameters to customize the progress bar.

**Downloading and writing the file**:


```python
for data in response.iter_content(chunk_size=1024):
    size = file.write(data)
    bar.update(size)
```

We iterate over the response content in 1024-byte chunks, write each chunk to the file, and update the progress bar.

## Using the Function

To use this function, simply call it with the URL of the file you want to download and the destination path:

```python
download('https://example.com/file.zip', 'file.zip')
```

This will download the `file.zip` file and display a progress bar in the command line:

```
file.zip:  38%|███           | 9.21M/23.9M [00:02<00:02, 5.25MB/s]
```

## Error Handling

It's important to handle possible errors during the download. Here's an improved version of the function that includes basic error handling:

```python
import requests
from tqdm import tqdm
from requests.exceptions import RequestException

def download(url, dest_path):
    try:
        response = requests.get(url, stream=True, allow_redirects=True)
        response.raise_for_status()  # Raises an exception for HTTP error status codes
        total_size = int(response.headers.get('content-length', 0))
        with open(dest_path, 'wb') as file, tqdm(
            desc=dest_path,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    except RequestException as e:
        print(f"Error during download: {e}")
    except IOError as e:
        print(f"Error writing file: {e}")
```

## Additional Examples

### Downloading Multiple Files

To download multiple files in parallel and show the progress of each, you can use `concurrent.futures` along with `tqdm`:

```python
import concurrent.futures
from tqdm import tqdm

def download_multiple(urls, dest_paths):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download, url, path) for url, path in zip(urls, dest_paths)]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Total Progress"):
            future.result()

# Usage
urls = ['https://example.com/file1.zip', 'https://example.com/file2.zip']
paths = ['file1.zip', 'file2.zip']
download_multiple(urls, paths)
```

## Alternatives

Although `tqdm` is an excellent option for showing progress, there are other alternatives:

- [progress](https://github.com/verigak/progress/): A library similar to `tqdm` with some additional features.
- [alive-progress](https://github.com/rsalmei/alive-progress): Offers animated and customizable progress bars.
- [rich](https://github.com/Textualize/rich): A library for creating rich command-line interfaces, which includes progress bars.

## Performance

The use of `tqdm` has a minimal impact on download performance. The overhead introduced by updating the progress bar is tiny compared to the file download time. However, for very small files or very fast connections, you might notice a slight decrease in speed.

## Conclusion

The `tqdm` library provides a simple and effective way to display download progress in Python. By incorporating progress bars into your download scripts, you can significantly improve the user experience and provide valuable information about the status of long-running operations.

I encourage you to experiment with `tqdm` in your own CLI projects. Try different configurations, customize the appearance of progress bars, and explore how you can integrate them into more complex applications.

## Additional Resources

- [Official tqdm documentation](https://github.com/tqdm/tqdm)
- [Requests documentation](https://docs.python-requests.org/en/latest/)
- [Python tutorial on file handling](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Python guide on concurrency](https://docs.python.org/3/library/concurrency.html)
