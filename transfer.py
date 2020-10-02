import os
import sys
import pyodbc
import arcpy
import pythonaddins

class ButtonClass1(object):
    """Implementation for TransferParcels_addin.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
        def onClick(self):

        ls_users = []
            failure = []
        success = []
        user = os.environ.get("USERNAME")

        fc = "VECTOR.SDEADMIN.Tax_Parcels"

        try:

            desc  = arcpy.Describe(fc)
            onums = desc.FIDset
            nums_list = onums.split(';')


            conn = pyodbc.connect('Driver={SQL Server};Server=th-govsql;Database=XXX;UID=XXX;PWD=XXX;Trusted_Connection=no;')
                cursor = conn.cursor()

            with arcpy.da.SearchCursor(fc, ['PARCEL_ID']) as c:
                    for row in c:
                        ls_users.append((user, int(row[0])))


            #c.reset()

            if len(nums_list) == 1 and nums_list[0] == '':
                pythonaddins.MessageBox("No parcels were selected in TAX_PARCELS", "Select Parcels", 0)
            else:

                success_message = "Parcel ID [{}] was successfully entered into Govern\n"

                for pair in ls_users:
                    try:

                        cursor.execute("""INSERT INTO PC_EXTERNAL (USR_ID, P_ID) VALUES (?,?)""", user, pair[1])
                        conn.commit()
                        success.append(success_message.format(pair[1]))
                    except pyodbc.Error as ex:
                            sqlstate = ex.args[1]
                            sqlstate = sqlstate.split(".")
                            failure.append("Insert failed on duplicate key." + sqlstate[-3] + "\n")

                pythonaddins.MessageBox("".join(success) + "".join(failure), "Results", 0)

        except:

            e = sys.exc_info()[1]
                errstring = "Error: " + e.args[0]
            pythonaddins.MessageBox(errstring, "Error Message", 0)



