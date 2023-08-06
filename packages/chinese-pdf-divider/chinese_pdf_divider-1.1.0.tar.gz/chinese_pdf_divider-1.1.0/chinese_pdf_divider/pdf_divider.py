from fitz import open
import pandas as pd
from numpy import array, percentile
from re import sub
from math import ceil
from string import punctuation as punc_string
from zhon.hanzi import punctuation
import os

# 獲取當前檔案所在目錄的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))

"""主程式"""

def pdf_divider(filename, remove_b_list = False, output_path = ''):
    """
    process a pdf file

    Args:
      filename: file path (string)
      year: 西元年 (string)
    """
    doc = open(filename)
    
    whole_blocks_lst = []
    
    ## 判斷B表位置
    list_pages = []
    if remove_b_list:
        # 使用相對路徑建立完整路徑
        b_list_file_path = os.path.join(current_dir, 'gri_pointers_b_frame.csv')
        df_pointers = pd.read_csv(b_list_file_path)
        list_pointers = list(df_pointers.columns)
        start = 0
        if len(doc)-20 > 0:
          start = len(doc) - 20
        for current_page in range(start, len(doc)):
        
            page = doc.load_page(current_page)
            for pointer in list_pointers:
                if page.search_for(pointer):
                    page = str(page).split(' ')[1]
                    list_pages.append(page)
                    break
        list_pages = process_b_pages_lst(list_pages)
        print(list_pages)

    ## 遍歷非B表所在的每個 page
    for i, page in enumerate(doc):
      if str(i) not in list_pages:
        process_one_page(page, whole_blocks_lst)
    
    ## 去除 <image:...> 
    del_img_lst = []
    for block in whole_blocks_lst:
        image_count = block.count('<image:')
        for _ in range(image_count):
            star = block.find('<image:')
            end = block.find('>')
            block = block[:star] + block[end+1:]
        del_img_lst.append(block)

    ## 清理資料：刪除標點、英文、數字、換行、�
    for i, b in enumerate(del_img_lst):
        #換行
        b = b.replace('\n', '')
        #缩進
        b = b.replace('\t', '')
        #英文
        b = sub('[a-zA-Z]', '', b)
        #中英標點符號 + �, 半形&全形空格, 數字
        punc = punc_string + punctuation + '� 　0-9･●▼•◆'
        punc = sub('[，。｡]', '', punc)#保留，。方便之後再分段
        b = sub(f'[{punc}]*', '', b)
        del_img_lst[i] = b

    ## 去除空字串 & 長度小於2(含)的字串 
    del_emp_lst = []
    count = 0
    for b in del_img_lst:
        if b != '' and len(b) > 2:
            del_emp_lst.append(b)
        else:
            count += 1
    
    ## 處理 block 長度 > 512 問題 => 用標點分段
    del_over_lst = []
    
    for i, b in enumerate(del_emp_lst):
      if len(b) <= 450: #不處理 (將512改成450)
        del_over_lst.append(b)
      else: # 處理
        par_num = ceil(len(b)/400)  ####改成400 
        
        punc = ['。', '｡', '，']
        #決定用哪個標點分段
        punc_for_divide = ''
        punc_num = 0
        for p in punc:
            punc_num = b.count(p)
            if punc_num < par_num:
                continue
            punc_for_divide = p
            break
        
        #將整個 block 用 par (標點符號)分成小段
        if punc_for_divide != '':
            content_lst = []
            for _ in range(punc_num):
                period_index = b.find(punc_for_divide)
                content_lst.append(b[:period_index+1])
                b = b[period_index+1:]
            
            if b != '':
                content_lst.append(b)


            block_sen_num = ceil(punc_num/par_num) #一個block幾小段文字

            block = ""
            count = 0
            for j in range(len(content_lst)):
                block += content_lst[j]
                count += 1
                if count == block_sen_num:
                    del_over_lst.append(block)
                    block = ""
                    count = 0
            if block != '':
                del_over_lst.append(block)

    ## 處理 block 長度還是 > 512 的問題 => 直接切分
    del_over_lst_second = []
    count_2 = 0
    for i, b in enumerate(del_over_lst):

        if len(b) <= 450:
            del_over_lst_second.append(b)
        else:
            while len(b) > 450:
                count_2 += 1
                del_over_lst_second.append(b[:450])
                b = b[450:]
            del_over_lst_second.append(b)

    ## 計算 oversize(應該沒有了吧)
    oversize = 0
    for b in del_over_lst_second:
        if len(b) > 512:
            oversize += 1

    ## 處理檔案名稱
    name_start_index = filename.rfind('/')
    file_path = filename[0:name_start_index]
    filename = filename[name_start_index+1 : -4]
    
    ## 判斷 del_over_lst_second 中是否有東西(有沒有分段結果) 有->輸出 沒有->再處理
    if len(del_over_lst_second) == 0:
        print("lst is empty: ", filename)
        print(f'\n{filename} is empty')
        return f'\n{filename} is empty\n'
    else:
        ## output
        if oversize == 0:
            df = pd.DataFrame(del_over_lst_second)
            df.columns = ['Block']
            df.dropna(axis=0, how='any', inplace=True)
            output_filename = f'{filename}_divided.csv'
            if len(output_path) == 0:
                output_path = os.path.join(file_path, output_filename)
            else:
                output_path = os.path.join(output_path, output_filename)
            try:
                df.to_csv(output_path, index=False, encoding='UTF-8-Sig')
                print(f'\n{filename} finished dividing\n')
                return f'{filename} finished dividing\n'
            except UnicodeEncodeError:
                print("\nhave UnicodeEncodeError but finished dividing")
                return "UnicodeEncodeError, but finished dividing"
            except Exception as e:
                print(e)       
        else:
            print(f'package need to be modify')
            return f'{filename} oversize'

def process_b_pages_lst(b_pages_lst):
  pages_lst_len = len(b_pages_lst)
  last = -1
  for i in range(pages_lst_len-2, -1, -1):
    if int(b_pages_lst[i]) != int(b_pages_lst[last])-1:
      return b_pages_lst[i+1:]
    else:
      last = i
  return b_pages_lst

def process_one_page(page, whole_blocks_lst):
    """
    process a pdf's page
    
    Args:
      page: pdf's page
      whole_blocks_lst: pdf's blocks
    """
    text = page.get_text("blocks")
    if len(text) == 0:
        return
    text_df = pd.DataFrame(text)
    text_df.columns = ['x', 'y', 'w', 'h', 'content', 'index', 'xxx']
    text_df.drop(['w', 'h', 'index','xxx'], axis=1, inplace=True)
    text_df['x'] = round(text_df['x'])
    text_df.sort_values(by=['x'], inplace=True)
    text_df.reset_index()

    x_blocks_lst = [] # DataFrame in it
    xaxis = text_df.iloc[0]['x']
    block_index = 0 #分段的index值
    for i, x in enumerate(text_df.iloc[1:]['x'], start=1):
        if x > (xaxis + 1) or x < (xaxis - 1):
            df = text_df.iloc[block_index:i, :]
            x_blocks_lst.append(df)
            block_index = i
            xaxis = x
        else:
            xaxis = x
    
    for x_block_df in x_blocks_lst:
        x_block_len = len(x_block_df.index)
      
        if x_block_len < 5: #不用再分段(OK)
            s = ""
            for c in x_block_df['content']:
                s += c
            whole_blocks_lst.append(s)
  
        else: # 要分段
            x_block_df.sort_values(by=['y'], inplace=True)
            y_gap_list = []
            s = x_block_df.iloc[0]['content'] #第一行的content

            for i in range(1, x_block_len):
                y = x_block_df.iloc[i]['y']
                content = x_block_df.iloc[i]['content']
                gap = y - x_block_df.iloc[i-1]['y'] #跟前一行的距離

                if len(y_gap_list) <= 3: ###改<= 讓y_gap_list中有三個之後再進行下列判斷
                    y_gap_list.append(gap)
                    s += content
                    continue

                y_gap_list = array(sorted(y_gap_list))
                q1 = percentile(y_gap_list, 25)
                q3 = percentile(y_gap_list, 75)
                iqr = q3 - q1
                if iqr < 1:
                    iqr = 1
                upper_limit = q3 + iqr
                lower_limit = q1 - iqr

                if gap > upper_limit or gap < lower_limit:
                    whole_blocks_lst.append(s)
                    s = content
                    y_gap_list = []
                    list(y_gap_list).append(y)
                else:
                    s += content
                    list(y_gap_list).append(y)

            # for 迴圈跑完把剩下的段落文字加到 list 中
            if len(s) != 0:
                whole_blocks_lst.append(s)

pdf_divider('C:/Users/cherr/OneDrive/桌面/C組-資管二-110306079-林耘熙.pdf')