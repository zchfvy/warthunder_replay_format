import os
import struct
import math

from wt_replay import WtReplay

WRITE_BODIES = True

rpdir = '/cygdrive/c/Program Files (x86)/Steam/steamapps/common/War Thunder/Replays'
replay_root = os.path.realpath(rpdir)

replay_files = []

for dirName, subdirList, fileList in os.walk(replay_root):
    for fname in fileList:
        name, extension = os.path.splitext(fname)
        if extension == '.wrpl':
            full_name = os.path.join(dirName, fname)
            replay_files.append(full_name)

replay_files = [os.path.join(replay_root, '#2017.11.09 01.34.49.wrpl')]


def print_fields_table(cols, rows, data):
    n_cols = len(cols)
    n_rows = len(rows)

    if len(data) < (n_cols * n_rows):
        print("Not enough data to tabulate {}/{} ({}*{})".format(
            len(data), n_cols*n_rows, n_cols, n_rows))
        return


    # Column headers:
    row_fmt = u"{:>15}" * n_cols
    # Add left most col for names
    row_fmt = u"{:>25}" + row_fmt


    print(row_fmt.format("", *cols).encode('utf-8'))
    for y in range(n_rows):
        b, e = y*n_cols, (y+1)*n_cols
        row_data = data[b:e]
        head = rows[y]
        print(row_fmt.format(head, *row_data).encode('utf-8'))

def just_tabulate(n_cols, data):
    row_fmt = u"{:>15}" * n_cols
    n_rows = int(math.floor(len(data)/n_cols))

    for y in range(n_rows):
        b, e = y*n_cols, (y+1)*n_cols
        row_data = data[b:e]
        print(row_fmt.format(*row_data))


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

    def unpack(data):
        if ord(data.flag) == 0x00:
            return struct.unpack('<i', data.val + '\x00')[0]
        if ord(data.flag) == 0x01:
            return struct.unpack('<i', data.val + '\x00')[0]
        if ord(data.flag) == 0x02:
            return struct.unpack('<i', data.val + '\x00')[0]
        #raise Exception('Unknown flag {:02x}'.format(ord(data.flag)))
        return struct.unpack('<i', data.val + '\x00')[0]

    for gd in [wt.data_pregame, wt.data_postgame]:
        print(' '.join(fn.value for fn in gd.body.fields1.fields))
        print(u' '.join(('*' + fn.value) for fn in gd.body.fields2.fields).encode('utf-8'))
        print('dat', [unpack(d) for d in gd.body.data[0:24]])
        # print(len(gd.body.fields1.fields))
        # print(len(gd.body.fields2.fields))
        # print(len(gd.body.data))
        print('')

    def str_is_int(value):
        try:
            val = int(value)
            return True
        except ValueError:
            return False


    data_body = wt.data_postgame.body
    cols = [f.value for f in data_body.fields1.fields]
    cols = [c for c in cols if c != 'nick']  # Columns seems to have 1 too many fields
    rows = [f.value for f in data_body.fields2.fields if not str_is_int(f.value) and len(f.value) > 0]
    data = [unpack(d) for d in data_body.data if ord(d.flag) != 0x02]  # don't know what the '2' flags are for
    data = data[9:]  # first 9 fields of data seem to be something else
    print_fields_table(cols, rows, data)

    just_tabulate(19, data)

    if WRITE_BODIES:
        with open(os.path.join(replay_root, fname + '.dat'), 'wb') as f:
            f.write(wt.compressed_body)
