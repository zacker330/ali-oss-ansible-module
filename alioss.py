#!/usr/bin/python
DOCUMENTATION = '''
---
module: alioss
short_description: upload and download aliyun oss object
'''

EXAMPLES = '''
- name: upload
  alioss:
    access_key_id: "{{ access_key_id }}"
    access_key_secure: "{{ access_key_secure }}"
    endpoint: "xxxxx.aliyuncs.com"
    bucket: "buckets"
    target: "upload"
    path: "./upload.yml"
    object_name:  "tmp/upload.yml"
  register: result
- name: download
  alioss:
    access_key_id: "{{ access_key_id }}"
    access_key_secure: "{{ access_key_secure }}"
    endpoint: "xxxxx.aliyuncs.com"
    bucket: "buckets"
    target: "download"
    path: "/tmp/download.yml"
    object_name:  "tmp/upload.yml"
  register: result
'''


from ansible.module_utils.basic import *
import oss2
import os,sys


def alioss_upload(data):

    try:
        oss_key = data['access_key_id']
        oss_AccessKeySecret = data['access_key_secure']
        endpoint = data['endpoint']
        path = data['path']
        bucket = data['bucket']
        object_name = data['object_name']

        auth = oss2.Auth(oss_key,oss_AccessKeySecret)
        bucket = oss2.Bucket(auth, endpoint, bucket)
        fp = open(path, 'r')
        bucket.put_object(object_name, fp)

    except BaseException as e:
        return False, {'response': e}
    else:
        return True, {"response": "upload success"}


def alioss_download(data):
    try:
        oss_key = data['access_key_id']
        oss_AccessKeySecret = data['access_key_secure']
        endpoint = data['endpoint']
        bucket = data['bucket']
        path = data['path']
        object_name = data['object_name']

        auth = oss2.Auth(oss_key,oss_AccessKeySecret)
        bucket = oss2.Bucket(auth, endpoint, bucket)

        f = open(path,"w")
        f.write(bucket.get_object(object_name).read())
        f.close()
    except BaseException as e:
        return False, {'response': e}
    else:
        return True, {"response": "download success"}



def main():
    fields = {
            "access_key_id": {"required": True, "type": "str"},
            "access_key_secure": {"required": True, "type": "str" },
            "endpoint": {"required": True, "type": "str"},
            "bucket": {"required": True, "type": "str"},
            "target": {
                "default": "upload",
                "choices": ['upload', 'download'],
                "type": 'str'
            },
            "path": {"required": True, "type": "str"},
            "object_name":  {"required": True, "type": "str"}
    }
    choice_map = {
          "upload": alioss_upload,
          "download": alioss_download,
    }


    module = AnsibleModule(argument_spec=fields)
    has_changed, result = choice_map.get(module.params['target'])(module.params)
    module.exit_json(changed=has_changed, meta=result)



if __name__ == '__main__':
    main()
