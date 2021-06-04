## git의 간단한 명령어 모음

```
$git init                   # working directory
$git add<file/dir>          # staging area로 이동
$git commit -m 'message'    # repository로 이동
$git status					# git 상태확인
$git log					# commit상태에 대해 log확인
$git restore				# add한 후 다시 working directory로 복구
```

   





## 간편한 마크다운 에디터: Typora

* #### Typora 사용법

  1. ##### 제목

     \#의 개수에 따라 다양한 크기의 제목을 설정 할 수 있다. (단축키: ctrl + 숫자 1~6)

  2. ##### 코드

     \~~~ 혹은 ```을 입력하면 코드블록 기능을 쓸 수 있다.

     \```입력 후 글자를 쓰면 그 코드블록의 제목이 된다. java, c, python등의 언어를 입력하면 그 언어에 맞게 코드블록의 내용이 하이라이팅 되서 나온다.

     단순히 강조하고 싶을때는 `강조할 단어`를 쓰면 된다.

  3. ##### 수평선

     ---를 입력하면 수평선을 넣을 수 있다.

     

  4. ##### 스크롤 이동

     화면 왼쪽 아래에 있는 동그라미 표시를 누르면 사이드바가 뜬다. (사이드바의 내용은 변경 가능)

     개략으로 해 두면 제목들이 표시되는데, 이 제목들을 클릭하면 제목간 빠른 이동이 가능하다.

     

  5. ##### 하이라이팅 표시

     ** , __ : 진하게. ** **진하게** **

     *, __ : 기울이기. _ *기울이기* _

     *** , ___: 진하게+ 기울이기.

     == : 형광펜(환경설정 필요). ==

     형광펜

     ==   





## pycharm에서 terminal git으로 연동

1. Ctrl + Alt + s를 눌러 pycharm setting열기
2. Terminal -> Shell path -> git/bin/bash.exe 으로 변경
3.  window(cmd) -> git bash terminal로 변경     



## Project pre-TODO list

- #### git과 pycharm을 연동하여 관리하기 (불필요한 파일 없애기)



1. 프로젝트 폴더(디렉토리)를 만든다.

2. `.gitignore`와 `README.md`파일을 생성한다.

   * **`.gitignore` 파일은 .git의 파일 관리에서 무시할 내용을, `README.md` 는  프로젝트의 소개 및 정리 내용을 담는다. **

3. `$ git init`을 한다.

   ```
   $ touch README.md .gitignore && git init
   
   * 실제로 프로젝트에 파일을 Staging area 올리고 commit하기
   $ git add. 
   $ git commit -m 'add .gitignore'
   ```

   

4. **주의**

   * **`.git/`폴더와 `.gitignore`파일과 `README.md`파일이 같은 위치에 존재하는가!!**

5. 첫번째 커밋을 한다!



* gitignore.io
  - 자신의 프로젝트에 맞는 .gitignore파일을 만든다 (소스코드 복붙)
