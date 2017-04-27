strFileURL = "https://github.com/NREL/EnergyPlus/releases/download/v8.7.0/EnergyPlus-8.7.0-78a111df4a-Windows-x86_64.exe"
strHDLocation = "C:\Users"

Set objXMLHTTP = CreateObject("MSXML2.XMLHTTP.6.0")

objXMLHTTP.open "GET", strFileURL, false
objXMLHTTP.send()

If objXMLHTTP.Status = 200 Then
	Set objADOStream = CreateObject("ADODB.Stream")
	objADOStream.Open
	objADOStream.Type = 1 'adTypeBinary

	objADOStream.Write objXMLHTTP.ResponseBody
	objADOStream.Position = 0    'Set the stream position to the start

	Set objFSO = Createobject("Scripting.FileSystemObject")
	If objFSO.Fileexists(strHDLocation) Then objFSO.DeleteFile strHDLocation
	Set objFSO = Nothing

	objADOStream.SaveToFile strHDLocation
	objADOStream.Close
	Set objADOStream = Nothing
End if

Set objXMLHTTP = Nothing

//http://stackoverflow.com/questions/17401413/msxml3-dll-access-denied