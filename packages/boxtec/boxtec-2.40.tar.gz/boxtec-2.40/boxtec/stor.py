class Storage:
    def __init__(self, stor, bucket_name='big-vertex-337220.appspot.com'):
        '''
        from google.cloud import storage
        '''
        self.bucket = stor.Client().get_bucket(bucket_name)

    def save(self, path, content):
        blob = self.bucket.blob(path).upload_from_string(content)

    def get(self, path):
        if self.bucket.blob(path).exists():
            return self.bucket.blob(path).download_as_text()
        else:
            return None