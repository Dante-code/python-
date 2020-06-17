# -*-coding:gb2312-*-

from selenium import webdriver
import selenium


def buildTojson(info: str, name):
    '''
    :param info: һ���ַ������Ի��з��ָ����ڲ���:�ֿ�
    :param name: һ���б�[��ʦ�����������]
    :return: ����һ����װ�õ��ֵ�
    '''
    form = '������' + name[0] + ','
    form += 'ְ�ƣ�'
    form += info.replace('\n', ',') + ','
    form += '�������' + name[1]
    return form


def getinfo(webdriver):
    '''
    ѡ����ʦ��ҳ��������ʦ������Ϣ�ı�ǩ
    :return: ����һ��web-element ����
    '''
    try:
        info = webdriver.find_element_by_css_selector('.t_jbxx_nr')
    except selenium.common.exceptions.NoSuchElementException:
        try:
            info = webdriver.find_element_by_css_selector('.jjside')
        except selenium.common.exceptions.NoSuchElementException:
            try:
                info = webdriver.find_element_by_css_selector('.jbxx')
            except selenium.common.exceptions.NoSuchElementException:
                info = webdriver.find_element_by_css_selector('.gdt')
    return info


def load_csc(d):
    ls = []
    for line in d:
        ls.append(line.split(','))
    # del ls[28], ls[56], ls[280]  #��������쳣
    # ���label�Ͷ�ά�ֵ��б�dic
    label = []
    dic = []
    for line in ls:
        temp = {}
        for i in line:
            try:
                temp[i.split('��')[0]] = i.split('��')[1]
                if i.split('��')[0] not in label:
                    label.append(i.split('��')[0])
            except:
                continue
        dic.append(temp)

        # ����д���б�dic
    with open('��Ժ��ʦ��Ϣ.csv', 'w+', encoding='ANSI') as fw:
        fw.write(','.join(label) + '\n')  # ����
        for line in dic:
            temp = ''
            for key in label:
                temp += line.get(key, '��') + ','  # ÿһ��
            fw.write(temp[:-1] + '\n')

    with open('�������ߵ�ǰʮλ��ʦ.csv', 'w+', encoding='ANSI') as fw:
        fw.write(','.join(label) + '\n')
        topTen = sorted(dic, key=lambda info: int(info['�����']), reverse=True)
        for line in topTen[:10]:
            temp = ''
            for key in label:
                temp += line.get(key, '��') + ','
            fw.write(temp[:-1] + '\n')

def main():

    wd = webdriver.Chrome('chromedriver.exe')

    # --------------- ʵ��������ַ
    wd.get(
        'https://faculty.xidian.edu.cn/xyjslb.jsp?urltype=tsites.CollegeTeacherList&wbtreeid=1001&st=0&id=1583&lang=zh_CN#collegeteacher')
    # ---------------

    # --------------- ����ר����ַ
    # wd.get(
    #     'https://faculty.xidian.edu.cn/xyjslb.jsp?totalpage=16&PAGENUM=16&urltype=tsites.CollegeTeacherList&wbtreeid=1001&st=0&id=1583&lang=zh_CN'
    # )
    # ---------------
    wd.implicitly_wait(10)  # ��ʽ�ȴ�10s

    d = []  # ����һ���б��б�ÿһ���һ���ֵ�
    '''
    d: ���д��ȥ���ֵ�
    '''
    try:
        while True:
            elementsa = wd.find_elements_by_css_selector('.sypics')  # �õ�a��ǩ
            elementsname = wd.find_elements_by_css_selector('.name')  # �õ�span��ǩ
            print(len(elementsa))  # �����ǰҳ����ʦ����

            for name, ele in zip(elementsname, elementsa):
                nametext = name.text
                ele.click()  # �㿪�˳����ӣ�����һ���´���
                wd.switch_to.window(wd.window_handles[-1])  # ����a��ǩ��������ָ����Ǹ�ҳ�洰��
                info = getinfo(wd)  # �õ�������Ϣ�ı�ǩ

                form = buildTojson(info.text, nametext.split('\n'))
                d.append(form)

                wd.close()  # ����ʦ����ҳ��ҳ�����
                wd.switch_to.window(wd.window_handles[0])  # �ַ���ԭ����ҳ��

            # ��һҳ
            wd.get(wd.find_elements_by_css_selector('.Next')[0].get_attribute('href'))
            # �������һҳʱ��ֱ��ͨ���������exceptȻ��д��json�ļ�

    except Exception as error:
        # �Ѵ�������������п���
        print(error)
        # �ر�ҳ��
        wd.close()

    #�ر���������
    load_csc(d)
    wd.quit()
    wd.stop_client()

