class NMEA0183parser():
    def __init__(self, rbuff):
        self.buff = rbuff

        self.RMC_latitude = 0
        self.RMC_longitude = 0
        self.speedRMC = 0

        self.directionDegreeVTG = 0
        self.speedVTG = 0

        self.GGA_latitude = 0
        self.GGA_longitude = 0
        self.GGA_status = 0

        self.parse()

    def parse(self):
        nemaMessage = self.buff.split('\r\n') #0x0A=LF

        for message in nemaMessage:
            if "RMC" in message:
                self.parsingRMC(message)
            elif "VTG" in message:
                self.parsingVTG(message)
            elif "GGA" in message:
                self.parsingGGA(message)

    def parsingGGA(self, message):
        try:
            dataSetGGA = message.split(',')

            if not "0" in dataSetGGA[6]:
                self.GGA_status = dataSetGGA[6]

                GGA_lat = dataSetGGA[2]
                self.GGA_latitude = float(GGA_lat[0:2]) + float(GGA_lat[2:9]) / 60.0

                GGA_lon = dataSetGGA[4]
                self.GGA_longitude = float(GGA_lon[0:3]) + float(GGA_lon[3:10]) / 60.0
        except:
            print("예외 발생!")

    def parsingRMC(self, message):
        try:
            dataSetRMC = message.split(',')

            if "A" in dataSetRMC[2]:
                RMC_lat = dataSetRMC[3]
                self.RMC_latitude = float(RMC_lat[0:2]) + float(RMC_lat[2:9])/60.0

                RMC_lon = dataSetRMC[5]
                self.RMC_longitude = float(RMC_lon[0:3]) + float(RMC_lon[3:10])/60.0

                self.speedRMC = round(float(dataSetRMC[7]), 4) * 1.852 #/ *km/h * /
                # print(self.speedRMC)
        except:
            print("예외 발생!")

    def parsingVTG(self, message):
        try:
            dataSetVTG = message.split(',')

            if "A" in dataSetVTG[8]:
                self.directionDegreeVTG = float(dataSetVTG[1])

                self.speedVTG = float(dataSetVTG[6])
        except:
            print("예외 발생!")

    def getValidLatitude(self):
        # print("RMC_latitude " + str(self.RMC_latitude))
        # print("GGA_latitude " + str(self.GGA_latitude))
        if self.GGA_latitude>0:
            return self.GGA_latitude
        elif self.RMC_latitude>0:
            return self.RMC_latitude
        else:
            return 0

    def getValidLongitude(self):
        # print("RMC_longitude " + str(self.RMC_longitude))
        # print("GGA_longitude " + str(self.GGA_longitude))

        if self.GGA_longitude>0:
            return self.GGA_longitude
        elif self.RMC_longitude>0:
            return self.RMC_longitude
        else:
            return 0

    def getGGAStatus(self):
        if self.GGA_status == 2:
            print("DGPS")
        elif self.GGA_status == 5:
            print("float GPS")
        else:
            print("not GPS")