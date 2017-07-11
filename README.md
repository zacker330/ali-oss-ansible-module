An ansible module of Aliyun OSS service
---
实现在Ansible中使用Aliyun OSS服务，需要提前安装 oss2 包：`pip install oss2`

### example

```
- name: upload
  alioss:
    access_key_id: "access_key_id"
    access_key_secure: "access_key_secure"
    endpoint: "xxxxx.aliyuncs.com"
    bucket: "buckets"
    target: "upload"
    path: "./upload.yml"
    object_name:  "tmp/upload.yml"
  register: result
- name: download
  alioss:
    access_key_id: "access_key_id"
    access_key_secure: "access_key_secure"
    endpoint: "xxxxx.aliyuncs.com"
    bucket: "buckets"
    target: "download"
    path: "/tmp/download.yml"
    object_name:  "tmp/upload.yml"
  register: result
```
