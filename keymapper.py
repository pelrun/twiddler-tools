import sys
from construct import *

class ModifierAdapter(Adapter):
  def __init__(self, subcon):
    Adapter.__init__(self, subcon)
    self.modmap = [
      "<Left Ctrl>",
      "<Left Shift>",
      "<Left Alt>",
      "<Left GUI>",
      "<Right Ctrl>",
      "<Right Shift>",
      "<Right Alt>",
      "<Right GUI>",
    ]
  def _encode(self, obj, context):
    return 0
  def _decode(self, obj, context):
    if obj == 0xFF:
      return "<Macro>"
    mods = []
    for bit in range(8):
      if obj & (1<<bit):
        mods.append(self.modmap[bit])
    return ":".join(mods)

class ChordAdapter(Adapter):
  def _encode(self, obj, context):
    (modifiers, keys) = obj.split()
    x = Container()
    x.NUM = 'N' in modifiers;
    x.SHIFT = 'S' in modifiers;
    x.ALT = 'A' in modifiers;
    x.CTRL = 'C' in modifiers;
    (x.r1, x.r2, x.r3, x.r4) = list(keys);
    return x
  def _decode(self, obj, context):
    chord = ""
    if obj["NUM"]:
      chord += 'N'
    if obj["ALT"]:
      chord += 'A'
    if obj["CTRL"]:
      chord += 'C'
    if obj["SHIFT"]:
      chord += 'S'
    if chord == "":
      chord = 'O'
    return chord+" "+obj["r1"]+obj["r2"]+obj["r3"]+obj["r4"]

class UsbScanCodeAdapter(Adapter):
  def __init__(self, subcon):
    Adapter.__init__(self, subcon)
    self.usbmap = {
      0x04 : "a",
      0x05 : "b",
      0x06 : "c",
      0x07 : "d",
      0x08 : "e",
      0x09 : "f",
      0x0A : "g",
      0x0B : "h",
      0x0C : "i",
      0x0D : "j",
      0x0E : "k",
      0x0F : "l",
      0x10 : "m",
      0x11 : "n",
      0x12 : "o",
      0x13 : "p",
      0x14 : "q",
      0x15 : "r",
      0x16 : "s",
      0x17 : "t",
      0x18 : "u",
      0x19 : "v",
      0x1A : "w",
      0x1B : "x",
      0x1C : "y",
      0x1D : "z",
      0x1E : "1",
      0x1F : "2",
      0x20 : "3",
      0x21 : "4",
      0x22 : "5",
      0x23 : "6",
      0x24 : "7",
      0x25 : "8",
      0x26 : "9",
      0x27 : "0",
      0x28 : "<Return>",
      0x29 : "<Escape>",
      0x2A : "<Backspace>",
      0x2B : "<Tab>",
      0x2C : " ",
      0x2D : "-",
      0x2E : "=",
      0x2F : "[",
      0x30 : "]",
      0x31 : "\\",
      0x33 : ";",
      0x34 : "'",
      0x35 : "`",
      0x36 : ",",
      0x37 : ".",
      0x38 : "/",
      0x39 : "<CapsLock>",
      0x3A : "<F1>",
      0x3B : "<F2>",
      0x3C : "<F3>",
      0x3D : "<F4>",
      0x3E : "<F5>",
      0x3F : "<F6>",
      0x40 : "<F7>",
      0x41 : "<F8>",
      0x42 : "<F9>",
      0x43 : "<F10>",
      0x44 : "<F11>",
      0x45 : "<F12>",
      0x46 : "<PrintScreen>",
      0x47 : "<ScrollLock>",
      0x48 : "<Break>",
      0x48 : "<Pause>",
      0x49 : "<Insert>",
      0x4A : "<Home>",
      0x4B : "<PageUp>",
      0x4C : "<Delete>",
      0x4D : "<End>",
      0x4E : "<PageDown>",
      0x4F : "<RightArrow>",
      0x50 : "<LeftArrow>",
      0x51 : "<DownArrow>",
      0x52 : "<UpArrow>",
      0x53 : "<NumLock>",
      0x54 : "<KP/>",
      0x55 : "<KP*>",
      0x56 : "<KP->",
      0x57 : "<KP+>",
      0x58 : "<KPEnter>",
      0x59 : "<KP1>",
      0x5A : "<KP2>",
      0x5B : "<KP3>",
      0x5C : "<KP4>",
      0x5D : "<KP5>",
      0x5E : "<KP6>",
      0x5F : "<KP7>",
      0x60 : "<KP8>",
      0x61 : "<KP9>",
      0x62 : "<KP0>",
      0x63 : "<KP.>",
      0x65 : "<Application>",
      0x67 : "<KP=>",
      0x68 : "<F13>",
      0x69 : "<F14>",
      0x6A : "<F15>",
      0x6B : "<F16>",
      0x6C : "<F17>",
      0x6D : "<F18>",
      0x6E : "<F19>",
      0x6F : "<F20>",
      0x70 : "<F21>",
      0x71 : "<F22>",
      0x72 : "<F23>",
      0x73 : "<F24>",
      0xE0 : "<Left Control>",
      0xE1 : "<Left Shift>",
      0xE2 : "<Left Alt>",
      0xE3 : "<Left GUI>",
      0xE4 : "<Right Control>",
      0xE5 : "<Right Shift>",
      0xE6 : "<Right Alt>",
      0xE7 : "<Right GUI>",
      0xFB : "<Enable Mouse>",
      0xFC : "<Disable Mouse>",
      0xFD : "<Upgrade Mode>",
      0xFE : "<Toggle Mass Storage>",
  }
  
  def _encode(self, obj, context):
    return 0
  def _decode(self, obj, context):
    if obj in self.usbmap:
      return self.usbmap[obj]
    else:
      return obj

# Twiddler configurator format

class Twiddler21():
  def __init__(self):
    
    self.header = Struct("header",
      ULInt8("version"),
      ULInt16("key_table_ptr"),
      ULInt16("mouse_table_ptr"),
      ULInt16("macro_table_ptr"),
    )

    self.config = Struct("config",
      ULInt16("mouse_timeout"),
      ULInt16("tap_threshold"),
      ULInt8("mouse_speed_initial"),
      ULInt8("mouse_speed_fast"),
      ULInt8("mouse_acceleration"),
      ULInt8("key_repeat_delay"),
      FlagsEnum(ULInt8("flags"),
        key_repeat_enable = 0x01,
        mass_storage_enable = 0x02,
      ),
    )

    self.row = Enum(BitField("row",3),
      O = 0,
      R = 1,
      M = 2,
      L = 4,
    )

    self.chord = ChordAdapter(BitStruct("chord",
      Rename("r2",self.row),
      Flag("ALT"),
      Rename("r1",self.row),
      Flag("NUM"),
      Rename("r4",self.row),
      Flag("SHIFT"),
      Rename("r3",self.row),
      Flag("CTRL"),
    ))

    self.key_code = Struct("key_code",
      ModifierAdapter(ULInt8("modifier")),
      IfThenElse("scancode", lambda ctx: ctx['modifier'] != '<Macro>',
        UsbScanCodeAdapter(ULInt8("scancode")),
        ULInt8("macro_index"),
      )
    )

    self.key_table = Struct("key_table",
      self.chord,
      Embed(self.key_code),
    )

    self.mouse_table = Struct("mouse_table",
      self.chord,
      FlagsEnum(ULInt8("mouse_action"),
        left_click = 1,
        right_click = 2,
        middle_click = 4,
        toggle = 8,
        ctrl = 16,
        shift = 32,
        alt = 64,
        double_click = 128,
      ),
    )

    self.macro_table = Struct("macro_table",
      ULInt16("length"),
      Array(lambda ctx: ctx.length/2-1, self.key_code),
    )

    self.keymap = Struct("keymap",
      Embed(self.header),
      self.config,
      Array(lambda ctx: (ctx.mouse_table_ptr-ctx.key_table_ptr)/4, self.key_table),
      Array(lambda ctx: (ctx.macro_table_ptr-ctx.mouse_table_ptr)/3, self.mouse_table),
      GreedyRange(self.macro_table),
    )

  def parse(self, obj):
    return self.keymap.parse(obj)
    
# Twiddler eeprom format

#ptr_table = Array(1024, ULInt16("ptr"))

class EepromChordAdapter(Adapter):
  def _encode(self, obj, context):
    x = Container()
    (x.modifier, keys) = obj.split()    
    (x.r1, x.r2, x.r3, x.r4) = list(keys);
    return x
  
  def _decode(self, obj, context):
    return obj["modifier"]+" "+obj["r1"]+obj["r2"]+obj["r3"]+obj["r4"]

class MouseChordAdapter(Adapter):
  def _encode(self, obj, context):
    x = Container()
    (modifier, keys) = obj.split()
    (x.r1, x.r2, x.r3, x.r4) = list(keys)
    return x
  
  def _decode(self, obj, context):
    return 'O '+obj["r1"]+obj["r2"]+obj["r3"]+obj["r4"]
    
row = Enum(BitField("row",2),
  O = 0,
  L = 1,
  M = 2,
  R = 3,
)

modifier = Enum(BitField("modifier",2),
  O = 0,
  S = 1,
  N = 2,
  NA = 3,
)

chord = EepromChordAdapter(BitStruct("chord",
  Padding(6),
  modifier,
  Rename("r4",row),
  Rename("r3",row),
  Rename("r2",row),
  Rename("r1",row),
))

mouse_chord = MouseChordAdapter(BitStruct("chord",
  Rename("r4",row),
  Rename("r3",row),
  Rename("r2",row),
  Rename("r1",row),
))

config = Struct("config",
  ULInt8("key_repeat_delay"),
  ULInt8("key_repeat_rate"),
  UBInt16("mouse_timeout"),
  ULInt8("mouse_double_delay"),
  ULInt8("mouse_key_delay"),
  ULInt8("mouse_debounce"),
  Rename("mouse_on_key", chord),
  Rename("mouse_off_key", chord),
  FlagsEnum(ULInt8("flags"),
    exit_mouse_on_click = 0x01,
  ),
  Padding(4),
)

mouse_table = Struct("mouse_table",
  mouse_chord,
  FlagsEnum(ULInt8("mouse_action"),
    left_click = 1,
    right_click = 2,
    middle_click = 4,
    double_click = 8,
    shift = 16,
    ctrl = 32,
    alt = 64,
    toggle = 128,
  ),
)

custom_scan_entry = Struct("custom_scan_entry",
  Anchor("ptr"),
  EmbeddedBitStruct(
    Flag("text"),
    BitField("length",7),
  ),
  String("string", lambda ctx: ctx.length),
)

custom_scan_table = Struct("custom_scan_table",
  GreedyRange(custom_scan_entry),
)

eeprom = Struct("eeprom",
  Padding(2048),
  config,
  Anchor("_start_mouse"),
  Range(0,16,mouse_table),
  Anchor("_end_mouse"),
  Padding(lambda ctx: 32 - (ctx._end_mouse-ctx._start_mouse)),
  Embed(custom_scan_table),
  Anchor("_end_data"),
  Padding(lambda ctx: 0x2000 - ctx._end_data),
)

romkeymap = {
  "a":0x61,
  "b":0x62,
  "c":0x63,
  "d":0x64,
  "e":0x65,
  "f":0x66,
  "g":0x67,
  "h":0x68,
  "i":0x69,
  "j":0x6a,
  "k":0x6b,
  "l":0x6c,
  "m":0x6d,
  "n":0x6e,
  "o":0x6f,
  "p":0x70,
  "q":0x71,
  "r":0x72,
  "s":0x73,
  "t":0x74,
  "u":0x75,
  "v":0x76,
  "w":0x77,
  "x":0x78,
  "y":0x79,
  "z":0x7a,
  "A":0x41,
  "B":0x42,
  "C":0x43,
  "D":0x44,
  "E":0x45,
  "F":0x46,
  "G":0x47,
  "H":0x48,
  "I":0x49,
  "J":0x4a,
  "K":0x4b,
  "L":0x4c,
  "M":0x4d,
  "N":0x4e,
  "O":0x4f,
  "P":0x50,
  "Q":0x51,
  "R":0x52,
  "S":0x53,
  "T":0x54,
  "U":0x55,
  "V":0x56,
  "W":0x57,
  "X":0x58,
  "Y":0x59,
  "Z":0x5a,
  "1":0x31,
  "2":0x32,
  "3":0x33,
  "4":0x34,
  "5":0x35,
  "6":0x36,
  "7":0x37,
  "8":0x38,
  "9":0x39,
  "0":0x30,
  "<Return>":0x0d,
  "<Escape>":0x1b,
  "<Backspace>":0x08,
  "<Tab>":0x09,
  "<Right Shift><Tab>":0x0a,
  " ":0x20,
  "-":0x2d,
  "=":0x3d,
  "[":0x5b,
  "]":0x5d,
  "\\":0x5c,
  ";":0x3b,
  "'":0x27,
  "`":0x60,
  ",":0x2c,
  ".":0x2e,
  "/":0x2f,
  "<CapsLock>":0x18,
  "<F1>":0x80,
  "<F2>":0x81,
  "<F3>":0x82,
  "<F4>":0x83,
  "<F5>":0x84,
  "<F6>":0x85,
  "<F7>":0x86,
  "<F8>":0x87,
  "<F9>":0x88,
  "<F10>":0x89,
  "<F11>":0x8a,
  "<F12>":0x8b,
  "<Right Shift><F1>":0xb0,
  "<Right Shift><F2>":0xb1,
  "<Right Shift><F3>":0xb2,
  "<Right Shift><F4>":0xb3,
  "<Right Shift><F5>":0xb4,
  "<Right Shift><F6>":0xb5,
  "<Right Shift><F7>":0xb6,
  "<Right Shift><F8>":0xb7,
  "<Right Shift><F9>":0xb8,
  "<Right Shift><F10>":0xb9,
  "<Right Shift><F11>":0xba,
  "<Right Shift><F12>":0xbb,
  "<PrintScreen>":0x1c,
  "<ScrollLock>":0x1a,
  "<Break>":0x1f,
  "<Pause>":0x1d,
#  "<Insert>":0x01,
  "<Delete>":0x01,
  "<Home>":0x02,
  "<PageUp>":0x04,
#  "<Delete>":0x7f,
  "<End>":0x03,
  "<PageDown>":0x05,
  "<RightArrow>":0x0c,
  "<LeftArrow>":0x0b,
  "<DownArrow>":0x07,
  "<UpArrow>":0x06,
  "<Right Shift><Home>":0x90,
  "<Right Shift><End>":0x91,
  "<Right Shift><PageUp>":0x92,
  "<Right Shift><PageDown>":0x93,
  "<Right Shift><UpArrow>":0x94,
  "<Right Shift><DownArrow>":0x95,
  "<Right Shift><LeftArrow>":0x96,
  "<Right Shift><RightArrow>":0x97,
  "<NumLock>":0x19,
  "<Application>":0x8e,
  "<Left Control>":0xe,
  "<Left Shift>":0x1e,
  "<Left Alt>":0xf,
  "<Left GUI>":0x8c,
  "<Right Control>":0xbd,
  "<Right Shift>":0xbe,
  "<Right Alt>":0xbc,
  "<Right GUI>":0x8d,
  "the":0x10,
  "of":0x11,
  "to":0x12,
  "ed":0x13,
  "and":0x14,
  "in":0x15,
  "ion":0x16,
  "ing":0x17,
  "<Right Shift>1":0x21,
  "<Right Shift>2":0x40,
  "<Right Shift>3":0x23,
  "<Right Shift>4":0x24,
  "<Right Shift>5":0x25,
  "<Right Shift>6":0x5e,
  "<Right Shift>7":0x26,
  "<Right Shift>8":0x2a,
  "<Right Shift>9":0x28,
  "<Right Shift>0":0x29,
  "<Right Shift>-":0x5f,
  "<Right Shift>=":0x2b,
  "<Right Shift>[":0x7b,
  "<Right Shift>]":0x7d,
  "<Right Shift>;":0x3a,
  "<Right Shift>'":0x22,
  "<Right Shift>,":0x3c,
  "<Right Shift>.":0x3e,
  "<Right Shift>/":0x3f,
  "<Right Shift>`":0x7e,
  "<Right Shift>\\":0x7c,
}

if __name__ == "__main__":
  twid21 = Twiddler21()
  with open(sys.argv[1],'rb') as f:
    data = f.read()
    keymap21=twid21.parse(data)

#    print keymap21.key_table

#  configdefault = b'\x64\x14\x01\x2c\x14\x0a\x52\x03\xaa\x03\x55\x00\x00\x00\x00\x00\x01\x04\x02\x02\x03\x01\x04\x0c\x08\x0a\x0c\x09\x10\x41\x20\x11\x30\x21\x40\x19\x80\x84\xc0\x81\x00\x00\x00\x00\x00\x00\x00\x00'
#  print config.parse(configdefault)
  
  myconfig = keymap21.config
  myconfig.key_repeat_rate = 20
  myconfig.mouse_double_delay = 20
  myconfig.mouse_key_delay = 10
  myconfig.mouse_debounce = 0x52
  myconfig.mouse_on_key = 'NA MMMM'
  myconfig.mouse_off_key = 'NA LLLL'
  myconfig.flags.exit_mouse_on_click = True
  configblock = config.build(myconfig)
  print config.parse(configblock)
  
  macros=[Container(ptr=None, text=True, length=len(z), string=z) for z in ["".join([x.scancode for x in y]) for y in [x.key_code for x in keymap21.macro_table]]]
  eepromblock=eeprom.build(Container(config=myconfig, mouse_table=keymap21.mouse_table, custom_scan_entry=macros, _end_data=None, _start_mouse=None, _end_mouse=None))
  macro_ptrs=[x['ptr'] for x in eeprom.parse(eepromblock).custom_scan_entry]

  eepromarray=bytearray(eepromblock)
  keycodemap={'O':0, 'L':1, 'M':2, 'R':3 }
  modifiermap={'O':0, 'S':1, 'N':2, 'NA':3 }
  keycodes=[]
  for x in keymap21.key_table:
    (modifier, keychord) = x.chord.split()  
    keycodes.append((modifier, keychord, x.modifier, x.scancode))
    if 'a'<=x.scancode<='z':
      nx = ('S', keychord, x.modifier, x.scancode.upper())
      keycodes.append(nx)
    if x.scancode == '<Tab>':
      keycodes.append(('S', keychord, x.modifier, '<Right Shift>'+x.scancode))

  for x in keycodes:
    if 'NS' in x[0]:
      # not a valid modifier for v2 model
      continue
    scancodeptr = 0
    keys = [keycodemap[y] for y in list(x[1])]
    scancodeptr = (modifiermap[x[0]] << 9) + (keys[3]<<7) + (keys[2]<<5) + (keys[1]<<3) + (keys[0]<<1)
    if (eepromarray[scancodeptr] != 0 and eepromarray[scancodeptr+1] != 0):
      print "Conflict! ",x
      continue
    keypress=str(x[2])+str(x[3])
    if (x[2]=="<Macro>"):
      print (x[0]+' '+x[1], macros[x[3]].string, hex(scancodeptr), hex(macro_ptrs[x[3]]))
      eepromarray[scancodeptr]=macro_ptrs[x[3]]>>8
      eepromarray[scancodeptr+1]=macro_ptrs[x[3]]&0xFF
    elif keypress in romkeymap:
      romkey = romkeymap[keypress] 
      eepromarray[scancodeptr]=0
      eepromarray[scancodeptr+1]=romkey&0xFF
      print (x[0]+' '+x[1], keypress, hex(scancodeptr), hex(romkey))
    else:
      print "Skipped ",x

  # checksum
  checksum = 0x10000 - (sum(eepromarray[2:-1]) & 0xFFFF)
  eepromarray[0]=(checksum>>8)&0xFF
  eepromarray[1]=checksum&0xFF

  with open("upload.bin",'wb') as f:
    #f.write("PTwiddler")
    for x in xrange(0,len(eepromarray),32):
      f.write('L'+str(eepromarray[x:x+32]))
    f.write("D")

  with open("buspirate.txt", 'w') as f:
    for x in xrange(0,len(eepromarray),32):
      f.write('[0xa0 '+str(x>>8)+' '+str(x&0xff)+' ')
      for y in eepromarray[x:x+32]:
        f.write(str(y)+' ')
      f.write("]\n")
      f.write('[0xa0 '+str(x>>8)+' '+str(x&0xff)+' [0xa1 r:32]\n')

  with open("keymap.bin",'wb') as f:
    f.write(str(eepromarray))
