import pygame as pg, json
from PIL import Image
import threading as thr

## Execute scripts, and read/write WID files (Why is the Data?)
class WIDWriter:
    def __init__(self):
        pass

    def write(self, file_path, sections):
        print("writeWID")
        with open(file_path, "w") as f:  # Open file in text mode for writing
            f.write("wid")  # Write magic bytes
            f.write(" ")  # Write file type (None)

            for sec_name, sec_data in sections.items():
                print(f" |-> {sec_name}")
                f.write("\x01" + sec_name + "\x03")  # Write section name
                f.write(f"\x07{sec_data['type']}\x08")
                if sec_data["type"] == "t":
                    f.write("\x04")
                    for size_val in sec_data["size"]:
                        f.write(str(size_val) + "\x05")
                    f.write("\x06")
                f.write(sec_data["data"])  # Write string data
                f.write("\x02")

            f.write("\xFF")  # Write end marker

class WIDReader:
    def __init__(self):
        pass

    def _wid_img(self, pdat, size=(10,10), show=0):
        fn = f"img.png"
        
        pixels = []
        print(len(pdat) / 6)
        for i in range(0, len(pdat), 6):
            r = int(pdat[i:i+2], 16)
            g = int(pdat[i+2:i+4], 16)
            b = int(pdat[i+4:i+6], 16)
            pixels.append((r, g, b))

        img = Image.new("RGB", size)
        img.putdata(pixels)

        img.save(fn)
        if show:
            img.show()
        return fn 
    
    def read(self, file):
        res={
            "sections": {}
        }
        secname = ""
        secval  = {
            "type": "",
            "data": ""
        }

        with open(file, "r") as f:
            magic = f.read(3).lower()
            ftype = f.read(1).lower()
            if magic == "wid":
                print("isWID")
                print(" | WidRead Console:")
                while True:
                    char = f.read(1)
                
                    if char == "\x01":
                        while True:
                            chnm = f.read(1)
                            if chnm == "\x03":
                                break
                            else:
                                secname += chnm
                            f.read(0)
                        print(f" | |-> {secname}")
                    elif char == "\x04" and secval["type"] == "t":
                        scva=0
                        while True:
                            chnm = f.read(1)
                            if chnm == "\x06":
                                secval["size"][scva] = int(secval["size"][scva])
                                break
                            elif chnm == "\x05":
                                secval["size"][scva] = int(secval["size"][scva])
                                scva+=1
                            else:
                                secval["size"][scva] += chnm
                            f.read(0)
                    elif char == "\x07":
                        secval["size"] = ["",""]
                        secval["data"] = ""
                        secval["type"] = f.read(1)
                    elif char == "\x02":
                        res["sections"][secname] = secval
                        secname = ""
                    elif char == "\xFF":
                        print("\nEndWID")
                        break
                    else:
                        if secname != "":
                            secval["data"] += char
                    f.read(0)
            else:
                print("notWID")
        return res

class SolWID:
    def __init__(self):
        self.widr  = WIDReader()
        self.widrs = WIDWriter()
    
    def _run(self, wid, file):
        scr = self.widr.read(wid)[file].split(";")
    
    def run(self, wid, file):
        t = thr.Thread(target=self._run, args=(wid, file,), name=f"SolEngine-RunnerWID")

if __name__ == "__main__":
    cl=input("method (1=read, 2=run, 3=widimg, 4=write) ")
    ar=input("WID file: ")
    if cl == "1":
        widr = WIDReader()
        print(widr.read(ar))
    elif cl == "2":
        wid = SolWID()
        wid.run(ar)
    elif cl == "3":
        file=input("Image file: ")
        widr = WIDReader()
        widr._wid_img(widr.read(ar)["sections"][file]["data"], widr.read(ar)["sections"][file]["size"],1)
    elif cl == "4":
        sections = json.loads(input("JSON sectiondata: "))

        writer = WIDWriter()
        writer.write(ar, sections)