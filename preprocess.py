import os
import csv
import glob
import sys

def m_scrolls(scrolls):
    sc_ant = 0
    sc_down = 0
    sc_down_d = 0
    sc_up = 0
    sc_up_d = 0
    for sc in scrolls:
        if sc > sc_ant:
            sc_down+=1
            sc_down_d+=sc-sc_ant
        elif sc_ant > sc:
            sc_up+=1
            sc_up_d+=sc_ant-sc
        sc_ant = sc

    return (sc_up_d, sc_up, sc_down_d, sc_down)

def process(data):
    print('ID ', data[0][0])
    n_secs = (int(data[-1][3])-int(data[0][3]))/3
    f_third = int(n_secs + int(data[0][3]))
    s_third = int(f_third + n_secs)

    thirds = [(0,f_third), (f_third+1,s_third), (s_third+1,int(data[-1][3]))]

    errs= [0,0,0]

    ics=[0,0,0]

    scrolls = [[],[],[]]

    cur_cit = ''
    cur_hot = ''
    ant_t_dias=-8
    ant_t_com=-8

    counter=0

    for (f,t) in thirds:
        print(f, t)
        data_filter = [r for r in data if int(r[3])>=f and int(r[3])<=t]
        for row in data_filter:
            if row[1]=='Scroll':
                scrolls[counter].append(int(row[2]))
            elif row[1]=='CheckCiudad' and cur_cit!=row[2]:
                cur_cit=row[2]
                ics[counter]+=1
                ant_t_dias=-8
                ant_t_com=-8
            elif row[1]=='CheckHotel' and cur_hot!=row[2]:
                cur_hot=row[2]
                ics[counter]+=1
                ant_t_dias=-8
                ant_t_com=-8
            elif row[1]=='ChangeDias':
                if (int(row[3])-ant_t_dias)>=8:
                    ics[counter]+=1
                ant_t_dias=int(row[3])
                ant_t_com=-8
            elif row[1]=='ChangeComida':
                if (int(row[3])-ant_t_com)>=8:
                    ics[counter]+=1
                ant_t_com=int(row[3])
                ant_t_dias=-8
            elif row[1].startswith('ERROR'):
                cur_cit = ''
                cur_hot = ''
                ant_t_dias=-8
                ant_t_com=-8
                errs[counter]+=1
        counter+=1

    up_d = [0,0,0]
    up = [0,0,0]
    down_d = [0,0,0]
    down = [0,0,0]

    for (index,scroll) in enumerate(scrolls):
        (up_d[index], up[index], down_d[index],down[index]) = m_scrolls(scroll)


    return (int(n_secs*3), errs[0], ics[0],up_d[0], up[0], down_d[0], down[0], errs[1], ics[1], up_d[1], up[1], down_d[1], down[1], errs[2], ics[2], up_d[2], up[2], down_d[2], down[2])

def ret_song(data):
    path_song = data[0][2]
    l = path_song.split('/')
    song= l[-1][:-4]
    return song

def put_musical_info(musical_info, songs_names):
    result=[]
    for song in songs_names:
        for info in musical_info:
            if info[0]==song[0]:
                result.append(info)
    return result


def put_tag(tags, songs_names):
    result=[]
    for song in songs_names:
        for info in tags:
            if info[1]==song[0]:
                result.append(info)
    return result

if __name__ == '__main__':
    filename = 'tags.csv'
    with open(filename, "r") as f:
        so = csv.reader(f, delimiter=',')
        musical_info = []
        for row in so:
            musical_info.append(row)

    filename = 'songs_names.csv'
    with open(filename, "r") as f:
        so = csv.reader(f, delimiter=',')
        songs_names = []
        for row in so:
            songs_names.append(row)

        result = put_tag(musical_info, songs_names)
        # print(' '.join(map(str,result)))
    with open('some.csv', 'w', newline='') as f:
        writer = csv.writer(f, quotechar="'")
        for row in result:
            writer.writerow(row)
