import os
import re
import subprocess
import sys

exe = "lex"

def prRed(skk): print("\033[91m{}\033[00m" .format(skk))

def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))

def findEXE():
    for filename in os.listdir("."):
        if filename.startswith(exe):
            print(filename)
            return filename

def runFilesLex(folder):
    total = 0;
    corr = 0;

    exe = findEXE()

    for filename in filter(lambda f: f.endswith(".tig"), os.listdir(folder)):
        total += 1;
        print(filename)

        incorrect = False

        # run the program
        res = subprocess.run(["sml", "@SMLload=./" + exe, folder + "/" + filename], timeout = 2, capture_output = True)
        out = res.stdout.decode('utf-8').strip().splitlines()
        out_f = []
        for line in out:
            no_num_line = re.sub("\s*\d+$", "", line)
            out_f.append(no_num_line)

        expected_out_fn = "out/" + filename.replace(".tig", ".txt");

        if len(sys.argv) >= 2 and sys.argv[1] == "--out":
            with open(expected_out_fn, "w") as out_file:
                out_file.write("\n".join(out_f));
        else:
            with open(expected_out_fn, "r") as out_file:
                correct = out_file.read().strip().splitlines();
                if correct != out_f:
                    incorrect = True
                    print(out_f)
                    print("---")
                    print(correct)
        
        if "Error" in "\n".join(out) or "error" in "\n".join(out):
            incorrect = True

        if incorrect:
            prRed("\tIncorrect");
        else:
            corr = corr + 1;
            prGreen("\tCorrect");

    return (corr, total)

def runFilesNoLex(folder):
    total = 0;
    corr = 0;

    exe = findEXE()

    for filename in filter(lambda f: f.endswith(".tig"), os.listdir(folder)):
        total += 1;
        print(filename)

        incorrect = False

        # run the program
        res = subprocess.run(["sml", "@SMLload=./" + exe, folder + "/" + filename], timeout = 2, capture_output = True)
        out = res.stdout.decode('utf-8').strip().splitlines()

        correct = "Error" in "\n".join(out) or "error" in "\n".join(out)

        if incorrect:
            prRed("\tIncorrect");
        else:
            corr = corr + 1;
            prGreen("\tCorrect");

    return (corr, total)

subprocess.run(["ml-build", "sources.cm", "Main.parse", exe])
(c1, t1) = runFilesLex("./testcases/lex")

(c2, t2) = runFilesNoLex("./testcases/nolex")

print(str(c1 + c2) + "/" + str(t1 + t2))
