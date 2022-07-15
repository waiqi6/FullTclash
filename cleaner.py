import yaml
from bs4 import BeautifulSoup


class ClashCleaner:
    """
    yaml配置清洗
    """

    def __init__(self, config):
        """

        :param config: 传入一个文件对象，或者一个字符串,文件对象需指向 yaml/yml 后缀文件
        """
        self.yaml = yaml.load(config, Loader=yaml.FullLoader)

    def nodesCount(self):
        """
        获取节点数量
        :return: int
        """
        return len(self.yaml['proxies'])

    def nodesName(self):
        """
        获取节点名
        :return: list
        """
        lis = []
        for i in self.yaml['proxies']:
            lis.append(i['name'])
        return lis

    def nodesType(self):
        """
        获取节点类型
        :return: list
        """
        t = []
        for i in self.yaml['proxies']:
            t.append(i['type'])
        return t

    def proxyGroupName(self):
        """
        获取第一个"select"类型代理组的名字
        :return: str
        """
        try:
            for t in self.yaml['proxy-groups']:
                if t['type'] == 'select' and len(t['proxies']) >= self.nodesCount():
                    return t['name']
                else:
                    pass
        except Exception as e:
            print(e)


class ReCleaner:
    def __init__(self, data: dict):
        self.data = data
        self._sum = 0
        self._netflix_info = []

    def getnetflixinfo(self):
        """

        :return: list: [netflix_ip, proxy_ip, netflix_info: "解锁"，“自制”，“失败”，“N/A”]
        """
        try:
            # print(self.data['ip'])
            if self.data['ip'] is None or self.data['ip'] == "N/A":
                return ["N/A", "N/A", "N/A"]
            if self.data['netflix1'] is None:
                return ["N/A", "N/A", "N/A"]
            if self.data['netflix2'] is None:
                return ["N/A", "N/A", "N/A"]
            r1 = self.data['netflix1']
            status_code = self.data['ne_status_code1']
            if status_code == 200:
                self._sum += 1
                soup = BeautifulSoup(r1, "html.parser")
                netflix_ip_str = str(soup.find_all("script"))
                p1 = netflix_ip_str.find("requestIpAddress")
                netflix_ip_r = netflix_ip_str[p1 + 19:p1 + 60]
                p2 = netflix_ip_r.find(",")
                netflix_ip = netflix_ip_r[0:p2]
                self._netflix_info.append(netflix_ip)  # 奈飞ip
            r2 = self.data['ne_status_code2']
            if r2 == 200:
                self._sum += 1

            self._netflix_info.append(self.data['ip']['ip'])  # 请求ip

            if self._sum == 0:
                ntype = "失败"
                self._netflix_info.append(ntype)  # 类型有四种，分别是无、仅自制剧、原生解锁（大概率）、 DNS解锁
                print("当前节点情况: ", self._netflix_info)
                return self._netflix_info
            elif self._sum == 1:
                ntype = "自制"
                self._netflix_info.append(ntype)
                print("当前节点情况: ", self._netflix_info)
                return self._netflix_info
            elif self.data['ip']['ip'] == self._netflix_info[0]:
                ntype = "解锁"
                self._netflix_info.append(ntype)
                print("当前节点情况: ", self._netflix_info)
                return self._netflix_info
            else:
                ntype = "解锁"
                self._netflix_info.append(ntype)
                print("当前节点情况: ", self._netflix_info)
                return self._netflix_info
        except Exception as e:
            print(e)
            return ["N/A", "N/A", "N/A"]

    def getyoutubeinfo(self):
        """

                :return: str :解锁信息: (解锁、失败、N/A)
                """
        try:
            if 'youtube' not in self.data:
                print("采集器内无数据")
                return "N/A"
            else:
                if "is not available" in self.data['youtube']:
                    return "失败"
                elif "YouTube Music 在您所在区域无法使用" in self.data['youtube']:
                    return "失败"
                elif self.data['youtube_status_code'] == 200:
                    return "解锁"
                else:
                    return "N/A"
        except Exception as e:
            print(e)
            return "N/A"

    def getDisneyinfo(self):
        """

        :return: 解锁信息: 解锁、失败、N/A
        """
        try:
            if self.data['disney'] is None:
                return "N/A"
            else:
                return self.data['disney']
        except Exception as e:
            print(e)
            return "N/A"

    def getGping(self):
        """
        获取Google ping的延迟
        :return: str: 字符串化的延迟，保留到个位数
        """
        if 'delay' in self.data:
            return "%.0fms" % self.data['delay']
        else:
            return "0ms"
