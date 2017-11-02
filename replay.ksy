meta:
  id: wt_replay
  title: WarThunder Replay
  application: WarThunder
  file-extension: wrpl
  encoding: UTF-8
seq:
  - id: header
    type: header
  - id: compressed_body
    size-eos: true
types:
  header:
    seq:
      - id: magic
        contents: [0xE5, 0xAC, 0x00, 0x10]
      - id: version
        size: 1
      - id: magic
        contents: [0x89, 0x01, 0x00]
      - id: mapname
        type: str
        size: 128
      - id: missionname
        type: str
        size: 256
      - id: missiondetails
        type: missiondetails
      - id: gamedetails
        type: gamedetails
  missiondetails:
    seq:
      - id: four_unknown_bytes  # ???
        contents: [0x00, 0x00, 0x00, 0x00]
      - id: mission_name
        type: str
        size: 128
      - id: time_of_day
        type: str
        size: 128
      - id: weather
        type: str
        size: 32
      - id: unknown1
        size: 88
      - id: txt_data
        size: 128
      - id: unknown2
        size: 60
      - id: mode
        type: str
        size: 128
  gamedetails:
    seq:
      - id: bbf
        contents: [0x00, 0x42, 0x42, 0x46, 0x03, 0x00]
      - id: unknown1
        size: 8
      - id: fields1
        type: str_field_list
      - id: padding1 # is it really? some data here
        type: u1
        repeat: until
        repeat-until: _ == 0x40
      - id: fields2
        type: str_field_list
      - id: padding2 # is it really? some data here
        type: u1
        repeat: until
        repeat-until: _ == 0x46
  str_field_list:
    seq:
      - id: num_fields
        type: u1
      - id: fields
        type: len_pfx_str
        repeat: expr
        repeat-expr: num_fields
  len_pfx_str:
    seq:
      - id: sz
        type: u1
      - id: value
        type: str
        size: sz


