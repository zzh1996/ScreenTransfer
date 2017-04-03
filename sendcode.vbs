Dim fso,file,WshShell
Set fso = CreateObject("Scripting.FileSystemObject")
Set file = fso.OpenTextFile("show.html", 1)
Set WshShell = WScript.CreateObject("WScript.Shell")
content = file.ReadAll
WScript.Sleep 3000
for i=1 to len(content)
    dim k
    k=mid(content,i,1)
    if instr("~!+^(){}%",k)<=0 then
        WshShell.SendKeys k
        WScript.Sleep 10
    else
        WshShell.SendKeys "{"+k+"}"
        WScript.Sleep 10
    end if
next