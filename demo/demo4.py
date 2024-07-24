import requests
import tmpsu5843_v_pb2 as tempfile_pb2
import time




# 创建消息
sku_details_request = tempfile_pb2.SkuDetailsRequest(
    field_1=17,
    field_2="com.codeway.chatapp",
    field_3="inapp",
    field_4=[
        "askai.pro.1week.t5",
        "askai.pro.freetrial.1week.t5",
        "askai.pro.lifetimeiap.t5"
    ],
    field_6=1,
    field_7=tempfile_pb2.SkuDetailsRequest.Field_7(field_7_1="6.1.0"),
    field_10=[
        tempfile_pb2.SkuDetailsRequest.Field_10(field_10_1="playBillingLibraryVersion", field_10_2="6.1.0"),
        tempfile_pb2.SkuDetailsRequest.Field_10(field_10_1="SKU_DETAILS_RESPONSE_FORMAT", field_10_2="PRODUCT_DETAILS"),
        tempfile_pb2.SkuDetailsRequest.Field_10(field_10_1="enablePendingPurchases", field_10_3=1)
    ]
)

# 序列化消息
serialized_request = sku_details_request.SerializeToString()

# 设置请求头
headers = {
    'X-DFE-Encoded-Targets': 'CAEaSuMFBdCPgQYJxAIED+cBfS+6AVYBIQojDSI3hAEODGxYvQGMAhRMWQEVWxniBQSSAjycAuESkgrgBeAfgCv4KI8VgxHqGNxrRbkI',
    'X-Ad-Id': '00000000-0000-0000-0000-000000000000',
    'x-public-android-id': 'fce52da069b9b286',
    'X-Limit-Ad-Tracking-Enabled': 'true',
    'User-Agent': 'Android-Finsky/30.6.18-21%20%5B0%5D%20%5BPR%5D%20450795914 (api=3,versionCode=83061810,sdk=31,device=HWMNA,hardware=qcom,product=MNA-L29,platformVersionRelease=12,model=MNA-LX9,buildId=HUAWEIMNA-L29,isWideScreen=0,supportedAbis=arm64-v8a;armeabi-v7a;armeabi)',
    'Connection': 'Keep-Alive',
    'X-DFE-Device-Checkin-Consistency-Token': 'ABFEt1VgSgC1s5on-g61eelrS9LPkaYpAfrQd6DDhHdB3h1WflcE_29I52g6c8FcaF6xb0dQLCbXUX-pfdjyIV0QCvbU7rURFshbCzp_XaWVTG6cL9YTcW1d1cbItMY7u-S1a1NtBs6GF3shzBStnKWLeU7pAouZDZMbi7rtSGaH_NXyUxJEnUrmT5yuweYGoTputCJ6DG5w4U8I9kKWDfWv8yEde926NigCbqiSPZYJBm1oTymePLk',
    'Authorization': 'Bearer ya29.a0AXooCgtI2AT0vclFhaFktGI9R6Jopg2Ph1eTCMrGi1_YuQZ-0n2Dxu3gZOAsplYBvALvnNSPFfgJaQzd3c1O_MAwY4cq6wQHianJIHpjmJXF9kYF-6TVLE7PmgoTTvhkiH9pt5o6ZBLPsnLsd56o-n0_qPl7C6SPXNufMgAOhywjMIPBt25mLmLX7LEgPNvfkXJdBnVoWEsCEkAwR6ntzBBoUzpK3aL0YxzHUsY0LapekGNN8YizutHt2Wq3k76SkmFtOQQ5mLx_nENdqSBWO50KS3QEyZP_rC-7MwIY4hao4wNqyecyOCpBT4LB8bw8iKgaCgYKAW8SARESFQHGX2MiBI-AXwbkAHpehYh4MSJyBA0330',
    'X-DFE-Client-Id': 'am-google',
    'X-DFE-Phenotype': 'H4sIAAAAAAAAAOOKcXb0DQ4oNzCoKNV1c0zMsywL9PVwqvBPcsr2TykJ8HUv9gx1La6I9Dcw9k7xTYtIMnasSopIq0g0SI8IdwxwDbfIygxw8U-PdPR1THML1DXNS_L0yffOinRxtLWVYgAAjtXkomAAAAA',
    'X-DFE-Device-Id': '3133b9d1b0e9f4fb',
    'X-DFE-Network-Type': '4',
    'Accept-Language': 'zh-CN',
    'X-DFE-Request-Params': 'timeoutMs=4000',
    'Content-Type': 'application/x-protobuf',
    'Accept-Encoding': 'gzip',
    'Content-Length': str(len(serialized_request)),
    'Host': 'play-fe.googleapis.com'
}
# print(f"{str(len(serialized_request))}")
# 发送请求
response = requests.post(
    url='https://play-fe.googleapis.com/fdfe/skuDetails',
    headers=headers,
    data=serialized_request
)

# 打印响应
print(response.status_code)
print(response.content)
