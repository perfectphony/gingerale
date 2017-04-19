from datetime import datetime

class Logger:
    def log(self, *output):
        output_concat = datetime.now().isoformat(' ')

        for o in output:
            output_concat += " " + str(o)

        #print(output_concat)

    def warn(self, *output):
        self.log("WARNING: ", output)

    def err(self, *output):
        self.log("ERROR: ", output)
