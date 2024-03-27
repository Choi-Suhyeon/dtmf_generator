# DTMF Generator

This is a script developed as an assignment for the Wireless Mobile Systems and Security class, generating DTMF (Dual Tone Multi-Frequency) signals.
 무선이동시스템및보안 수업에서 과제로 진행한 DTMF(Dual Tone Multi-Frequency) 신호를 발생시키는 스크립트입니다.

## USAGE GUIDELINES
입력 필드에 휴대 전화 다이얼 번호(0~9, *, #)를 입력한 후, 아래 Write 버튼을 누르거나 키보드에서 Enter를 누르면 아래와 같은 정보를 확인할 수 있습니다.
- 시간에 따른 진폭 그래프: 현재는 여러 번호를 입력한 경우 그래프들이 겹쳐져 보이게 됩니다.
- 이에 대한 주파수 그래프 : 이것 또한 마찬가지로 그래프들이 겹쳐져 보이게 됩니다. 다만, 중복하여 출력되는 그래프는 없습니다.
- 다이얼 소리 : 입력한 다이얼 번호의 소리를 출력합니다.

예시 : 123456789*# ENTER

프로그램 하단 상태바를 통해 입력에 유효하지 않은 번호가 포함되어 있었는지 여부를 확인할 수 있습니다.

## TO-DO LIST
- ~~0~9, *, # 중 하나가 주어졌을 때, 주어진 숫자(또는 문자)에 해당하는 DTMF 신호 그래프를 그리고 소리 출력.~~
- ~~가능하면, GUI로 깔끔하게 프로그램 만들기.~~
- 여러 입력이 주어졌을 때 시간 축을 기준으로 하는 파형 그래프는 출력되는 소리와 매칭되게 출력시키기.