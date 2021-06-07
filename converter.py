import os
import sys
import traceback


def parsesong(songname):
    print(os.path.splitext(os.path.basename(songname))[0] + ".json")

    FNFTEMP = """{"song":{"player2":"dad","player1":"bf","speed":SPEED,"needsVoices":true,"sectionLengths":[],"song":"SONGNAME","notes":SECTIONS,"bpm":BPM,"sections":0},"bpm":BPM,"sections":SECTIONCOUNT,"notes":SECTIONS}"""
    SECTIONTEMP = """{"mustHitSection":false,"typeOfSection":0,"lengthInSteps":16,"sectionNotes":NOTES}"""

    MAXLEN = 200

    song = {}
    sections = []
    bpm = 0
    totalsections = 0

    adjust = 100

    with open(songname) as f:
        data = "".join(f.readlines()).split(";")

        # print(len(data))

        for statement in data:
            if "#" in statement:
                statement = statement.strip().split("#")[1]

                key = statement.split(":")[0]
                if key == "NOTES":
                    key = statement.split(":")[0].strip() + ":" + statement.split(":")[1].strip() + ":" + \
                          statement.split(":")[2].strip() + ":" + statement.split(":")[3].strip()
                    value = statement.split(":")[4].strip() + ":" + statement.split(":")[5].strip() + ":" + \
                            statement.split(":")[6].strip()
                    song[key] = value
                else:
                    value = ":".join(statement.split(":")[1:])
                    song[key] = value

                # if len(value) > MAXLEN:
                #     print(key + " is " + value[:MAXLEN] + ".....")
                # else:
                #     print(key + " is " + value)

        # print(song["NOTES:dance-double::Easy"].split(":")[2])

        bpm = float(song["BPMS"].split("=")[1])

        sectionlist = song["NOTES:dance-double::Easy"].split(":")[2].split(",")

        for sectioncount, section in enumerate(sectionlist):
            sections.append([])
            for beatcount, notes in enumerate(section.split("\n")):
                sectionsplit = len(section.split("\n"))
                for notecount, note in enumerate(notes):
                    # print("NOTE")
                    # print(note)
                    if note == "1":
                        timing = (60 / bpm) * (sectioncount * 4 + (beatcount * 4) / len(notes)) * 1000 - adjust
                        direction = notecount

                        # direction = notecount + 4
                        # if direction > 7:
                        #     direction -= 8

                        sections[sectioncount].append([timing, direction, 0])
                    if note == "2":
                        timing = (60 / bpm) * (sectioncount * 4 + (beatcount * 4) / len(notes)) * 1000 - adjust
                        duration = 0
                        direction = notecount

                        # direction = notecount + 4
                        # if direction > 7:
                        #     direction -= 8

                        count = beatcount
                        count1 = 0

                        # print(notecount)

                        while True:
                            count += 1

                            # print("PRECOUNT")
                            # print("sectionlist:" + sectionlist[sectioncount + count1])
                            # print("sectionlistlen:" + str(len(sectionlist[sectioncount + count1].split("\n"))))
                            # print("count:" + str(count))

                            if count >= len(sectionlist[sectioncount + count1].split("\n")):
                                count = 0
                                count1 += 1

                            # print("COUNT")
                            # print("count:" + str(count))
                            # print("beatcount+count:" + str(count))
                            # print("count1:" + str(count1))

                            # print(sectionlist)
                            # print(sectionlist[sectioncount + count1].split("\n"))
                            # print(sectionlist[sectioncount + count1].split("\n")[count])
                            if len(sectionlist[sectioncount + count1].split("\n")[count]) == 8:
                                duration += 1

                                threecheck = sectionlist[sectioncount + count1].split("\n")[count][notecount]

                                # print("THREECHECK")
                                # print("threecheck:" + threecheck)
                                # print("len:" + str(len(threecheck)))
                                # print("type:" + str(type(threecheck)))
                                # print(threecheck == "3")
                                if threecheck == "3":
                                    break

                        sections[sectioncount].append(
                            [timing, direction, (60 / bpm) * (duration * 4) / len(notes) * 1000])
            totalsections = sectioncount

    sectionsout = []
    for sectioncount, section in enumerate(sections):
        sectionsout.append(SECTIONTEMP.replace("NOTES", str(section)))
        # print(sectionsout[sectioncount])

    # print(sectionsout)

    speed = (0.3 / 80) * (bpm - 100) + 1

    with open(os.path.dirname(sys.argv[0]) + "/" + os.path.splitext(os.path.basename(songname))[0] + ".json", "w") as f:
        f.write(FNFTEMP.replace("SONGNAME", "Bopeebo").replace("BPM", str(int(bpm))).replace("SECTIONCOUNT", str(
            totalsections)).replace("SPEED", str(speed)).replace("SECTIONS", str(sectionsout).replace("'", "")))


def main():
    if len(sys.argv) > 1:
        for songname in sys.argv:
            # print(os.path.splitext(os.path.basename(songname))[0])
            # print(os.path.splitext(os.path.basename(songname))[1])
            if os.path.splitext(os.path.basename(songname))[1] == ".sm" or os.path.splitext(os.path.basename(songname))[1] == ".ssc":
                try:
                    parsesong(songname)
                except:
                    traceback.print_exc()
                    input("Press return to continue.")
    else:
        print("DEBUG MODE")
        path = input("Enter path of file:")

        try:
            parsesong(path)
        except:
            traceback.print_exc()
            input("Press return to continue.")


main()
