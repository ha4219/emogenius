# [emogenius](https://github.com/ha4219/emogenius)

![emogenius](https://github.com/ha4219/emogenius/blob/dev/assets/readme/0.png?raw=true)

## Contents

- [Title](#-title)
- [Description](#-description)
- [Team](#-team)
- [Install](#-install)
- [Run](#-run)
- [Task](#-task)
- [Release](#-release)
- [License](#-license)
- [Reference](#-reference)

## 🎉 Title

- [emogenius](https://chrome.google.com/webstore/detail/emogenius/heddhmefcmbkfoojdngpojbhkkglgcdg?hl=ko&authuser=0)


## 📖 Description
![summary](https://github.com/ha4219/emogenius/blob/dev/assets/readme/summary.png?raw=true)
- 한국어 문장을 감정 별로 분류해 그에 맞는 Emoji를 추천한다.



## 😀 Team

- [정동하](https://github.com/ha4219)


## 🎯 Install
![deploy_](https://github.com/ha4219/emogenius/blob/dev/assets/readme/1.png?raw=true)

[Chrome_extension ](https://chrome.google.com/webstore/detail/emogenius/heddhmefcmbkfoojdngpojbhkkglgcdg?hl=ko&authuser=0)
- v1.0.0은 에러가 있는 상태입니다. 따라서 현재 다시 심사 중이기 때문에 아래 방법으로 받아주시면 감사합니다.(22.05.29)
- v1.0.2 배포 심사 완료됐습니다. 따라서 위에 링크를 통해 실행해주세요!(22.05.31)

### 직접 설치
1. [emogenius donwload link](https://github.com/ha4219/emogenius/releases/download/1.0.2/emogenius.zip)를 통해 해당 파일을 다운받고 압축을 풉니다.
2. chrome://extensions/로 이동합니다.
3. 오른쪽 상단에서 개발자 모드를 사용 설정합니다.
<img src="https://github.com/ha4219/emogenius/blob/dev/assets/readme/2.png?raw=true" style="display: block;  width: 200px; height: 70px;"/>

4. "압축해제된 확장 프로그램을 로드합니다"를 클릭합니다.
<img src="https://github.com/ha4219/emogenius/blob/dev/assets/readme/3.png?raw=true" style="display: block;"/>

5. 앱 또는 확장 프로그램 폴더를 찾아 선택합니다.

6. Chrome 다음에서 새 탭을 열고 앱을 클릭한 다음 다음 앱 또는 확장 프로그램을 클릭합니다. 올바르게 로드되고 작동하는지 확인합니다.
<img src="https://github.com/ha4219/emogenius/blob/dev/assets/readme/4.png?raw=true" style="display: block; width: 400px; height: 200px;"/>


## 🚘 Run

![run_gif](https://github.com/ha4219/emogenius/blob/dev/assets/readme/run.gif?raw=true)

- 문장을 드래그한 후 단축키를 눌러주세요!
 
- `Window`: Ctrl+Shift+U
- `Mac`: Command+U 

- 단축키 변경은 chrome 확장 프로그램에서 좌측 상단 메뉴바를 클릭 한 후 단축키를 누르면 변경할 수 있습니다.
<img src="https://github.com/ha4219/emogenius/blob/dev/assets/readme/5.png?raw=true" style="display: block;"/>

## ✅ Task
- [x] Fine Tuning KoBERT 
- [x] Deploy Flask server 
- [x] Make Chrome Extension
- [ ] Server Dockerfile 작성
- [ ] Server 이전

## 🌋 Release
- v1.0.0 (22.05.29)
  - 초기 앱 릴리즈
- v1.0.2 (22.05.29)
  - 알맞지 않는 Emoji 버그 수정
  - 필요 없는 permission 제거
  - (22.05.31) chrome_extension 배포 완료
  - (22.06.02) chrome_extension 설명 추가

## 📄 License
`KoBERT` 프로그램이 `Apache-2.0`를 따르기에 그대로 사용했습니다. 잘못 올렸을 경우 알려주세요. 수정하겠습니다.

## 👍 Reference

- [감성 대화 말뭉치](https://aihub.or.kr/aidata/7978)
- [SKTBrain/KoBERT](https://github.com/SKTBrain/KoBERT)
- [emojidb](https://emojidb.org/)
