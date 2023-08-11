# %%
# !pip install pyass

# %%
import pyass
import pandas as pd

# %%
def read_ass_file(file_path):
    with open(file_path,'r',encoding='utf-8') as ass_file:
        ass_text=ass_file.read()
    return  ass_text
def process_ass_text(ass_text):
    lines=ass_text.splitlines()
    is_line=[]
    for line in lines:
        is_line.append(line.startswith("Dialogue:"))

    filtered_lines=[line for line,mask in zip(lines,is_line) if mask]
    return filtered_lines
    



# %%
# E:\projects\corpus generator\subtitles example

# %%
def time_to_seconds(time_str):
    h, m, s = time_str.split(':')
    seconds = int(h) * 3600 + int(m) * 60 + float(s)
    return seconds
def find_overlap(interval1_start, interval1_end, interval2_start, interval2_end):
    return max(interval1_start, interval2_start) <= min(interval1_end, interval2_end)
    
def seconds_to_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:.2f}"




import os
import time


englishFiles=[]
directory = r"E:\projects\corpus generator\subtitles example"
file_extension = "US.ass"
count=0
infiniteloop_prevention=0
while(count<149):
    fileNumber=0
    for filename in os.listdir(directory):
        fileNumber+=1
        if len(str(count<3)):
            file_extension=f"- {count:02d}.enUS.ass"
        else:
            file_extension=f"- {count}.enUS.ass"
        if filename.endswith(file_extension):
            file_path = os.path.join(directory, filename)
            englishFiles.append(file_path)
            count=count+1
            infiniteloop_prevention=0
            continue
        infiniteloop_prevention=infiniteloop_prevention+1
        if fileNumber>148:
            break
        if infiniteloop_prevention>150:
            infiniteloop_prevention=0
            count=count+1
            break
        



englishFiles

len(englishFiles)


directory = r"E:\projects\corpus generator\subtitles example"
arabicFiles=[]
count=0
infiniteloop_prevention=0
while (count<149):
    fileNumber=0
    for fileName in os.listdir(directory):
        fileNumber+=1
        # print("file number is: ",fileNumber)
        file_extension=f"{count:03d} [BD 1080p][HEVC x265 10bit][MST].ass"
        # print("file_extension is: ",file_extension)
        if fileName.endswith(file_extension):
            # print("file name is: ", fileName)
            file_path = os.path.join(directory, fileName)
            # print(file_path)
            arabicFiles.append(file_path)
            count= count+1
            infiniteloop_prevention=0
            break
        infiniteloop_prevention=infiniteloop_prevention+1
        if infiniteloop_prevention>300:
            infiniteloop_prevention=0
            count=count+1
            break
            



# %%
# arabicFiles

# %%


# %%
column_names=["English","Arabic","TimeOfIntersection"]
corpusDf=pd.DataFrame(columns=column_names)
corpusDf

# %%
count=0
for arabicFile,engFile in zip(arabicFiles,englishFiles):
    count+=1
    arabicFile=read_ass_file(arabicFile)
    arabicProcessedfile=process_ass_text(arabicFile)
    engFile=read_ass_file(engFile)
    engProcessedFile=process_ass_text(engFile)
    print("Processed files: ",count)
    # print(engProcessedFile)
    new_row={}
    for engLine in engProcessedFile:
        SplittedEngLine=engLine.split(",")
        interval1_start=time_to_seconds(SplittedEngLine[1])
        interval1_end=time_to_seconds(SplittedEngLine[2])
        for ArabicLine in arabicProcessedfile:
            SplittedAraLine=ArabicLine.split(",")
            interval2_start=time_to_seconds(SplittedAraLine[1])
            interval2_end=time_to_seconds(SplittedAraLine[2])
            if find_overlap(interval1_start,interval1_end,interval2_start,interval2_end):
                new_row['English']=SplittedEngLine[-1]
                new_row['Arabic']=SplittedAraLine[-1]
                intersection_start = max(interval1_start, interval2_start)
                intersection_end = min(interval1_end, interval2_end)
                new_row['TimeOfIntersection']=intersection_end-intersection_start
                # print(new_row)
                newDF=pd.DataFrame([new_row])
                corpusDf=pd.concat([corpusDf,newDF],ignore_index=True)

# %%
corpusDf.to_excel("parallelCorpus.xlsx") 

# %%



