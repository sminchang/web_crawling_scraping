# 프로젝트 환경 구축 가이드

## 실행 환경 구축

### CPython 설치
1. [Python 공식 홈페이지](https://www.python.org)에서 Python 컴파일러(인터프리터)를 다운로드하여 설치합니다.
2. 설치 과정 중 `Add Python to PATH` 옵션을 체크하여 시스템 PATH에 Python을 추가합니다.

### IDE 설정
1. [Visual Studio Code](https://code.visualstudio.com)를 설치합니다.
2. VSCode의 `Extensions`에서 `Python` 확장 프로그램을 설치합니다.
3. `Run and Debug` (단축키: `Ctrl + Shift + D`)에서 `Python File` 디버거를 설치합니다.
4. `.py` 확장자로 Python 파일을 생성한 후, VSCode에서 실행합니다.

### 가상 환경 구축 및 라이브러리 설치

1. PowerShell 또는 명령 프롬프트에서 아래 명령어를 입력하여 가상 환경을 구축합니다:
   ```bash
   1-1. python -m venv .venv (.venv는 가상 환경에 대한 암묵적 작명법, 하위 폴더 생성 후 가상 환경 구축)
   1-2. ./.venv/Script/activate.bat(가상 환경 활성화)
   1-3. pip install 라이브러리명 입력 (venv를 통해 해당 프로젝트 폴더에서만 라이브러리가 설치되도록 설정할 수 있다.)
