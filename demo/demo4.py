import requests,pandas as pd

url = 'https://www.dianxiaomi.com/crawl/edit.htm?id=110345270305925386'
headers = {
    'Cookie': 'Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1716378074; dxm_i=MTYwNTczNSFhVDB4TmpBMU56TTEhMDY5MzcyMjY2NjNmY2M1OTk0OTUxMTJiOWM3YmJkNDA; dxm_t=MTcxNjM3ODMzNyFkRDB4TnpFMk16YzRNek0zIWZiMTNjNGU1NmVmZmE1NWMxODE2MjExZjZkZWQwZWUz; dxm_c=ZElNcVRJbTchWXoxa1NVMXhWRWx0TnchZDNiYjBjOTA5NjMxNmFkMGUxM2QyNzc2NTY2ZjMyOTI; dxm_w=MDA4MGY0MDZlOGJhZTkzZTljNDQ0NmJmMThjMTgwNzYhZHowd01EZ3daalF3Tm1VNFltRmxPVE5sT1dNME5EUTJZbVl4T0dNeE9EQTNOZyE4NjU5NjY3MTc0MDcyZTU0MWE0M2VhNjU4NDJlZWE4MQ; dxm_s=CQTHABXXVcJMjXAa4k2mug3wj-PAfJ2FcoNaWT1XP2U; _dxm_ad_client_id=A166A34BC8B6DDD9E2F8DB07B91C19FE7; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1716378364; JSESSIONID=37465EDB78B1A218FAA57C9295E59C1B',
    'Referer': 'https://www.dianxiaomi.com/crawl/edit.htm?id=110345270305925386',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

rsp = requests.get(url, headers=headers)

print(rsp.text)

# with open("text.html", "w") as f:
#     f.write(r.text)
