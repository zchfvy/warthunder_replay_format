import os

from wt_replay import WtReplay

rpdir = '/cygdrive/c/Program Files (x86)/Steam/steamapps/common/War Thunder/Replays'
replay_root = os.path.realpath(rpdir)

replay_files = []

for dirName, subdirList, fileList in os.walk(replay_root):
    for fname in fileList:
        name, extension = os.path.splitext(fname)
        if extension == '.wrpl':
            full_name = os.path.join(dirName, fname)
            replay_files.append(full_name)

for f in reversed(replay_files):
    fname = os.path.basename(f)
    print('')
    print('Processing File {}'.format(fname))

    wt = WtReplay.from_file(f)
    print(wt.header.mapname)
    print(wt.header.missionname)

    md = wt.header.missiondetails
    print(md.mission_name)
    print(md.time_of_day)
    print(md.weather)
    print(md.txt_data)
    print(md.mode)
    print(md.replay_len)

    gd = wt.header.gamedetails
    print(' '.join(fn.value for fn in gd.fields1.fields))
    print(' '.join(fn.value for fn in gd.fields2.fields))
