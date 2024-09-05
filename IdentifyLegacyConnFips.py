import os

class ConnFipsApp:
    import geopandas
    import tkinter as tk
    from tkinter import messagebox
    def __init__(self):
        # grab current and legacy fips codes from shapefiles
        self.shpDir = os.path.dirname(os.path.realpath(__file__))
        self.legCountyShp = fr"{self.shpDir}\tl_2020_us_county_09.shp" # pre 2022 county geometry
        self.curCountyShp = fr"{self.shpDir}\tl_2022_us_county_09.shp" # current county geometry
        self.FipsLists = self.getFipsFromShapes()
        self.legFipsCodes = self.FipsLists[0]
        self.currentFipsCodes = self.FipsLists[1]
        # initiate window object
        self.root = self.tk.Tk()
        self.root.title("Ct FIPS Code Tool")
        # set startup size of window
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        self.rootWidth = 350
        self.rootHeight = 300
        self.root.geometry(f"{self.rootWidth}x{self.rootHeight}+{int(self.screenWidth*0.65)}+{int(self.screenHeight*0.25)}")
        # create entry field
        self.entryLabel = self.tk.Label(self.root, text="Conn FIPS Code")
        self.entryLabel.place(relx=0.025, y=0)
        self.entry = self.tk.Entry(self.root, width=5)
        self.entry.place(relx=0.1, rely=0.07)
        # create button to apply input fips code
        self.inputButton = self.tk.Button(self.root, text="Get FIPS", command=lambda: self.cnty2PlnRgn(self.entry.get()))
        self.inputButton.place(relx=0.075, rely=0.14)
        # create output widget
        self.outputText = self.tk.Text(self.root, width=10, height=10)
        self.outputText.pack(padx=20, pady=20)
        self.root.mainloop()

    def getFipsFromShapes(self):
        shpDir = os.path.dirname(os.path.realpath(__file__))
        legCountyShp = fr"{shpDir}\tl_2020_us_county_09.shp" # pre 2022 county geometry
        legGeom = self.geopandas.read_file(legCountyShp, columns=["GEOID"], ignore_geometry=True)
        legFipsCodes = [f for f in legGeom.GEOID]
        curCountyShp = fr"{shpDir}\tl_2022_us_county_09.shp" # current county geometry
        currentGeom = self.geopandas.read_file(curCountyShp, columns=["GEOID"])
        currentFipsCodes = [f for f in currentGeom.GEOID]
        return legFipsCodes, currentFipsCodes

    def cnty2PlnRgn(self, fips, negBufferVal=-0.005):
        self.outputText.delete(1.0, self.tk.END)
        if fips in self.legFipsCodes:
            inGeoData = self.geopandas.read_file(
                self.legCountyShp,
                columns = ["GEOID"],
                where=f"GEOID = '{fips}'"
                )
            negBuffer = inGeoData.buffer(negBufferVal)
            outGeoData = self.geopandas.read_file(
                self.curCountyShp,
                columns = ["GEOID"],
                mask = negBuffer
                )
        elif fips in self.currentFipsCodes:
            inGeoData = self.geopandas.read_file(
                self.curCountyShp,
                columns = ["GEOID"],
                where=f"GEOID = '{fips}'"
                )
            negBuffer = inGeoData.buffer(negBufferVal)
            outGeoData = self.geopandas.read_file(
                self.legCountyShp,
                columns = ["GEOID"],
                mask = negBuffer
                )
        else:
            self.messagebox.showerror(title="WRONG FIPS, FOOL!", message="FIPS CODE NOT FOUND")
            return

        fipsCodes = [i for i in outGeoData.GEOID]
        fipsCodes.sort(reverse=True) # will add the fips codes in reverse order so provide it backwards
        for fipsCode in fipsCodes:
            self.outputText.insert("1.0", f"{fipsCode}\n")

def main():
    app = ConnFipsApp()

if __name__ == "__main__":
    main()