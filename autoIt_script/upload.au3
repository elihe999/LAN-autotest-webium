ControlFocus("打开","","Edit1")
;识别windows窗口
WinWait("[CLASS:#32770]","",10)
;窗口等待十秒
ControlSetText("打开", "", "Edit1", $CmdLine[1])
;想输入框中输入需要上传的地址
Sleep(2000)
ControlClick("打开", "","Button1");
;点击[打开】按钮