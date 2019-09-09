import os

def times(self):
    ff = self.current
    cdo_result = os.popen( "cdo showtimestamp " + ff).read()
    cdo_result = cdo_result.replace("\n", "")
    cdo_result = cdo_result.split()
    cdo_result = pd.Series( (v for v in cdo_result) )
    #return cdo_result
