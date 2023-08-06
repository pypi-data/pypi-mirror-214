import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_host(host: str,
             Cookie: str,
             hostid: list,
             triggerid: str = "0",
             fromtime: str = "now-30d",
             totime: str = "now"):

    filter_hostids = ""
    for id in hostid:
        filter_hostids += "&filter_hostids%5B%5D="+id
    if fromtime != "now-30d":
        fromtime = fromtime+"%2000%3A00%3A00"
    if totime != "now":
        totime = totime+"%2000%3A00%3A59"
    url = "https://"+host+"/report2.php?mode=0&from="+fromtime+"&to="+totime+filter_hostids+"&filter_set=1" 
    get_url_data = "https://"+host+"/report2.php?mode=0&from="+fromtime+"&to="+totime+filter_hostids+"&filter_set=1" #13794
    # get_url_data = "https://"+host+"/report2.php?mode=1&from=now-30d&to=now&filter_groupid=0&filter_templateid=0&tpl_triggerid="+str(triggerid)+"&hostgroupid="+str(hostgroupid)+"&filter_set=1"
    headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "th-TH,th;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": Cookie,
            "Host": host,
            "Referer": get_url_data,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
            }
    r = requests.get(url,headers=headers)
    
    data_html_split = str(str(r.text).split('class="list-table"')[1])

    data_html = str(data_html_split.split('<th>Graph</th></tr></thead>')[1])

    data = data_html.split("Show</a>")
    resutl_data = []
    data_max_page = 1

    for x in data:
        data_per_host = {
            "hostname":"",
            "value":"0.0000",
        }
        x = str(x).replace('LinkBranchVRF','ping loss')
        x = str(x).replace('LinkNode','ping loss')
        dataperhost = str(x).split('ping loss')
        if len(dataperhost) == 2:
            data_per_host["hostname"] = str(dataperhost[0].split('<tr><td>')[1]).split('</td><td><a')[0]
            for data_percen in str(dataperhost[1]).split('</td><td>'):
                if data_percen[:5] == "<span":
                    if data_percen.split('"')[1] == "green":
                        data_per_host["value"] = str(str(data_percen).split('">')[1]).split('</')[0][:-1]
        else:
            data_page = str(dataperhost[0]).split('"')
            for a in data_page:
                if a[:10] == "Go to page":
                    data_max_page = int(str(a.split(",")[0]).split('Go to page')[1])
        if data_per_host['hostname'] != "":
            resutl_data.append(data_per_host)
    if data_max_page == 1:
        return resutl_data,data_max_page
    if data_max_page == 10:
        return [],0
    #############################################################################################
    resutl_data = []
    for num_page in range(data_max_page):
        url = "https://"+host+"/report2.php?page="+str(num_page+1)
        get_url_data = "https://"+host+"/report2.php?mode=0&from=now-30d&to=now"+filter_hostids+"&filter_set=1"
        headers={
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "th-TH,th;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": Cookie,
                "Host": host,
                "Referer": get_url_data,
                "Upgrade-Insecure-Requests": "1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
                }

        r = requests.get(url,headers=headers)


        data_html_split = str(str(r.text).split('class="list-table"')[1])

        data_html = str(data_html_split.split('<th>Graph</th></tr></thead>')[1])


        data = data_html.split("Show</a>")

        data_max_page = 1

        for x in data:
            data_per_host = {
                "hostname":"",
                "value":"0.0000",
            }
            x = str(x).replace('LinkBranchVRF','ping loss')
            x = str(x).replace('LinkNode','ping loss')
            dataperhost = str(x).split('ping loss')
            if len(dataperhost) == 2:
                data_per_host["hostname"] = str(dataperhost[0].split('<tr><td>')[1]).split('</td><td><a')[0]
                for data_percen in str(dataperhost[1]).split('</td><td>'):
                    if data_percen[:5] == "<span":
                        if data_percen.split('"')[1] == "green":
                            data_per_host["value"] = str(str(data_percen).split('">')[1]).split('</')[0][:-1]
                resutl_data.append(data_per_host)
            else:
                data_page = str(dataperhost[0]).split('"')
                for a in data_page:
                    if a[:10] == "Go to page":
                        data_max_page = int(str(a.split(",")[0]).split('Go to page')[1])
    return resutl_data,data_max_page


def get_group(host,Cookie,triggerid,hostgroupid):
    #https://smartmonitor.inet.co.th/report2.php?mode=1&from=now-30d&to=now&filter_groupid=0&filter_templateid=0&tpl_triggerid=0&hostgroupid=23&filter_set=1&filter_set=1
    url = "https://"+host+"/report2.php?mode=1&from=now-30d&to=now&filter_groupid=0&filter_templateid=0&tpl_triggerid=0&hostgroupid="+str(hostgroupid)+"&filter_set=1&filter_set=1"
    get_url_data = "https://"+host+"/report2.php?mode=1&from=now-30d&to=now&filter_groupid=0&filter_templateid=0&tpl_triggerid="+str(triggerid)+"&hostgroupid="+str(hostgroupid)+"&filter_set=1"
    headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "th-TH,th;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": Cookie,
            "Host": host,
            "Referer": get_url_data,
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
            }

    r = requests.get(url,headers=headers)

    data_html_split = str(str(r.text).split('class="list-table"')[1])

    data_html = str(data_html_split.split('<th>Graph</th></tr></thead>')[1])

    data = data_html.split("Show</a>")
    resutl_data = []
    data_max_page = 1

    for x in data:
        data_per_host = {
            "hostname":"",
            "value":"0.0000",
        }
        dataperhost = str(x).split('ping loss')
        if len(dataperhost) == 2:
            data_per_host["hostname"] = str(dataperhost[0].split('<tr><td>')[1]).split('</td><td><a')[0]
            for data_percen in str(dataperhost[1]).split('</td><td>'):
                if data_percen[:5] == "<span":
                    if data_percen.split('"')[1] == "green":
                        data_per_host["value"] = str(str(data_percen).split('">')[1]).split('</')[0][:-1]
        else:
            data_page = str(dataperhost[0]).split('"')
            for a in data_page:
                if a[:10] == "Go to page":
                    data_max_page = int(str(a.split(",")[0]).split('Go to page')[1])
        resutl_data.append(data_per_host)
    

    #############################################################################################

    resutl_data = []
    for num_page in range(data_max_page):
        url = "https://"+host+"/report2.php?page="+str(num_page+1)
        get_url_data = "https://"+host+"/report2.php?mode=1&from=now-30d&to=now&filter_groupid=0&filter_templateid=0&tpl_triggerid="+str(triggerid)+"&hostgroupid="+str(hostgroupid)+"&filter_set=1"
        headers={
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "th-TH,th;q=0.9",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": Cookie,
                "Host": host,
                "Referer": get_url_data,
                "Upgrade-Insecure-Requests": "1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
                }

        r = requests.get(url,headers=headers)

        data_html_split = str(str(r.text).split('class="list-table"')[1])

        data_html = str(data_html_split.split('<th>Graph</th></tr></thead>')[1])

        data = data_html.split("Show</a>")
        data_max_page = 1

        for x in data:
            data_per_host = {
                "hostname":"",
                "value":"0.0000",
            }
            dataperhost = str(x).split('ping loss')
            if len(dataperhost) == 2:
                data_per_host["hostname"] = str(dataperhost[0].split('<tr><td>')[1]).split('</td><td><a')[0]
                for data_percen in str(dataperhost[1]).split('</td><td>'):
                    if data_percen[:5] == "<span":
                        if data_percen.split('"')[1] == "green":
                            data_per_host["value"] = str(str(data_percen).split('">')[1]).split('</')[0][:-1]
                resutl_data.append(data_per_host)
            else:
                data_page = str(dataperhost[0]).split('"')
                for a in data_page:
                    if a[:10] == "Go to page":
                        data_max_page = int(str(a.split(",")[0]).split('Go to page')[1])
    return resutl_data,data_max_page

