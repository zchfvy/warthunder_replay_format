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

#replay_files = [os.path.join(replay_root, '#2016.10.02 21.44.40.wrpl')]

for f in reversed(replay_files):
    fname = os.path.basename(f)
    print('')
    print('Processing File {}'.format(fname))

    wt = WtReplay.from_file(f)
    head = wt.header
    print(head.mapname)
    print(head.missionname)
    print(head.mission_name)
    print(head.time_of_day)
    print(head.weather)
    print(head.txt_data)
    print(head.mode)
    print(head.footer_pos)

    for gd in [wt.data_pregame, wt.data_postgame]:
        print(' '.join(fn.value for fn in gd.body.fields1.fields))
        print(' '.join(('*' + fn.value) for fn in gd.body.fields2.fields))
        #print('dat', gd.body.data)
        print('')
