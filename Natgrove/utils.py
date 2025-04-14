from storages.backends.s3boto3 import S3Boto3Storage

StaticRootS3BotoStorage = lambda: S3Boto3Storage(location='static-afi')
MediaRootS3BotoStorage  = lambda: S3Boto3Storage(location='media', default_acl = 'private', file_overwrite = False,
                                                 custom_domain = False,
                                                 querystring_auth = True)
