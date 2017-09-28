from pure import versioned_pure_interface
import urllib

url = 'https://riswebtest.st-andrews.ac.uk/ws/api/59/'
api_key = 'f39e70b7-c2b2-48a2-8175-92ccc6978128'

test_object_id = '83957a84-2186-4c14-8e55-f961a19ec9a9'


pure = versioned_pure_interface('v59')
pure_api = pure.API(url, api_key)
download_manager = pure.DownloadManager(pure_api) 
dataset_json = pure_api.get_dataset(test_object_id)

dataset = pure.Dataset(dataset_json)

def ws_url_remap(pure_data_url):
    """ Modifies a data location url to be http and /portal rather than /ws """
    url_parts = list(urllib.parse.urlsplit(pure_data_url))
    path_parts = [p for p in url_parts[2].split('/') if p]
    url_parts[2] = "/".join(['portal'] + path_parts[1:])
    url_parts[0] = 'http'
    return urllib.parse.urlunsplit(url_parts)

remapped_urls = [(ws_url_remap(url), file_name) for url, file_name
                in dataset.documents()]

downloaded_files = [download_manager.download_file(*doc) for doc in remapped_urls] 

# Create path structure from DOI
datasets = pure_api.list_all_datasets()

# Upload data, metadata and original_metadata


