from dagster import In, OpExecutionContext, op, Out

from .resources import QcloudCosResource


@op(description="上传照片到COS",
    required_resource_keys={'qcloud_cos'},
    ins={
        "key": In(str, description="上传文件KEY"),
        "file": In(bytes, description="文件字节数据"),
        "expired": In(int, default_value=0, description="预签名下载链接的过期时间，0 为不获取，默认为 0"),
        "bucket": In(str, default_value='', description="bucket_id，默认为资源设置的bucket_id")},
    out={
        "etag": Out(str, description='ETag'),
        "presigned_url": Out(str, description='预签名的下载链接')
    })
def op_upload_file(context: OpExecutionContext, key, file: bytes, expired:int, bucket:str):
    qcloud_cos:QcloudCosResource = context.resources.qcloud_cos
    response = qcloud_cos.put_object(Bucket=qcloud_cos.BucketId, Body=file, Key=key)
    bucket = bucket if bucket else qcloud_cos.get_pre_bucket()

    if expired:
        filename = key.split('/')[-1]
        url = qcloud_cos.get_presigned_url(
            bucket=bucket,
            Key=key,
            Method='GET',
            Expired=expired,
            Headers={'response-content-disposition':f'attachment; filename={filename}'}
        )
    else:
        url = ''
    return response['ETag'], url
