import re

pattern = {
    '[audio]' : 'audio detect',
    '[movie]' : 'movie detect',
    '[image]' : 'sound detect'
}
re_com = re.compile("|".join(map(re.escape, pattern.keys())))
test_list = [
    '![audio](audiofile.mp3)',
    '![movie](movie.mp4)',
    '![image](image.jpg)',
    'nsadf',
]

#for i in test_list:
#    mo = re_com.search(i)
#    if mo  and mo.group() in pattern:
#        print(pattern[mo.group()])



#for i in test_list:
#    mo = re_com.findall(i)
#    if mo:
#        for value in mo:
#            if value in pattern:
#                print(pattern[value])


def re_func(MatchObject):
    if MatchObject.group(0) in pattern:
        print('asdfasd')
        return pattern[MatchObject.group(0)]

for i in test_list:
    result = re.sub("|".join(map(re.escape, pattern)), re_func, i)
    print(result)
