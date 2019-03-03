class Pagination(object):
    """
    自定制分页器
    """
    def __init__(self,totalCount,currentPage,pageItemNumber=3,maxPagerNumber=7):
        self.total_count = totalCount             #全部数据
        try:
            c = int(currentPage)                  #当前页
            if c <= 0:
                c = 1
            self.current_page = c
        except Exception as e:
            self.current_page = 1
        self.page_item_num = pageItemNumber       #每页显示的条目
        self.max_pager_num = maxPagerNumber       #最多显示多少页码
#切片（范围）
    def start(self):
        return (self.current_page-1)*self.page_item_num
    def end(self):
        return  self.current_page*self.page_item_num

#显示有多少页数
    @property       #调用时不用()
    def num_pages(self):
        a,b=divmod(self.total_count,self.page_item_num)
        if b==0:
            return a
        return a+1

#显示页码
    def pager_num_range(self):
        #self.current_page              #当前页
        # self.max_pager_num            #最多页码数量
        # self.num_pages                #总页数
        if self.num_pages < self.max_pager_num:     #条件1：当总页数小于要显示的页码时      *
            return range(1,self.num_pages+1)
                                                    # 条件2：当总页数大于要显示的页码时     **
        part = int(self.max_pager_num/2)            #中间页码                               **
        if self.current_page <= part:               #当前所在的页码小于中间页码，显示1-11页 **
            return range(1,self.max_pager_num+1)
        if (self.current_page + part) > self.num_pages:     #条件3：当页码到总页数时，不能再增加页码   ***
            return range(self.num_pages-self.max_pager_num+1,self.num_pages+1)
        return range(self.current_page-part,self.current_page+part+1) #当前所在页码大于中间页码，需要改变页码 **

#前端显示分页
    def page_str(self,base_url):
        page_list=[]
#首页
        first="<li><a href='%s?p=1'>首页</a></li>" % base_url
        page_list.append(first)
#上一页
        if self.current_page == 1:
            pre_page="<li><a href='javascript:;'>上一页</a></li>"
        else:
            pre_page="<li><a href='%s?p=%s'>上一页</a></li>"%(base_url,self.current_page-1)
        page_list.append(pre_page)
#页码
        for i in self.pager_num_range():
            if i == self.current_page:
                temp = "<li><a style='width:41.58px;color:white;background-color:#337AB7;' href='%s?p=%s'>%s</a></li>" % (base_url,i,i)
            else:
                temp = "<li><a style='width:41.58px;' href='%s?p=%s'>%s</a></li>" % (base_url,i,i)
            page_list.append(temp)
#下一页
        if self.current_page == self.num_pages:
            next_page = "<li><a href='javascript:;'>下一页</a></li>"
        else:
            next_page="<li><a href='%s?p=%s'>下一页</a></li>" % (base_url,self.current_page+1)
        page_list.append(next_page)
# 尾页
        first = "<li><a href='%s?p=%s'>尾页</a></li>" % (base_url,self.num_pages)
        page_list.append(first)
        return ''.join(page_list)