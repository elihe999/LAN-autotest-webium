ControlFocus("��","","Edit1")
;ʶ��windows����
WinWait("[CLASS:#32770]","",10)
;���ڵȴ�ʮ��
ControlSetText("��", "", "Edit1", $CmdLine[1])
;���������������Ҫ�ϴ��ĵ�ַ
Sleep(2000)
ControlClick("��", "","Button1");
;���[�򿪡���ť