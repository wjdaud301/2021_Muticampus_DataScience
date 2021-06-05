## git의 간단한 명령어 모음

```
$ git init			# working directory를 생성/초기화
$ git add <file/dir>		# git add . 뒤에 점을 찍으면 git status의 빨간색 항목들을모두 새로 추적하여 staging area로 이동
$ git commit -m 'message'	# repository로 이동
$ git status			# untracked file, git이 버전 관리를 하고 있지 않은 파일들을 보여준다 (빨간색)
$ git log			# commit상태에 대해 log확인 <option> --oneline: 한줄로 요약
$ git restore			# add한 후 다시 working directory로 복구
$ git commit --amend		# commit message 수정
$ git config --global user.name / user.email  # git의 서명하는 것과 동일 
$ rm -rf .git 			# .git 폴더가 삭제되며 Git 로컬 저장소 지정을 해제한다.
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
   * gitignore.io 이용
     - 자신의 프로젝트에 맞는 .gitignore파일을 만든다 (소스코드 복붙)

3. `$ git init`을 한다.


4. **주의**

* **`.git/`폴더와 `.gitignore`파일과 `README.md`파일이 같은 위치에 존재하는가 확인한다!!**

5. 첫번째 커밋을 한다!

---

```
$ touch README.md .gitignore  
$ git init

* 실제로 프로젝트에 파일을 Staging area 올리고 commit하기
$ git add. 
$ git commit -m 'add .gitignore'
```



## master 와 branch

* branch의 목적 : branch의 역할을 다하고 master가 되는 것이 종착지, 역할을 다한 후 제거된다.

```
$ git checkout : branch를 상하좌우 head를 옮기는 것이 가능

$ git switch : branch를 좌우로 head를 옮기는 것 이동

$ git branch -c 'branch 이름' : branch를 생성한 후 이동

$ git branch -d 'branch 이름' : branch 제거
```



* 진행과정
  1. branch 생성을 생성하면 master시점부터 진행
  2. barach에서 할 일이 끝났다면 master로 전환 `$git switch master `
  3. master branch에서 `$git merge <branch 이름>`을 통해 병합진행
  4. `$git branch -d <branch 이름>` 명령어로 진행한 branch 삭제



* 충돌사항 (automatic merge가 되지 않는 상황)

  1. switch masters
  2. new file
  3. edit
  4. add /commit

  - branch가 commit을 하고 master와 병합하기 전  master가 commit이 일어난 상황이므로

    automatic merge가 되지 않기 때문에 수동으로 겹치는 부분을 수정해줘야 한다.

    



## remote 저장소 연동하기



#### 1) 로컬 저장소 디렉토리 생성(폴더 만들기)

* 로컬에서 프로젝트를 관리할 로컬 디렉토리 저장소를 새로 생성하고`git init` 한다



#### 2) local (directory) -> remote (repository) 연동하기

* git bash를 열어 로컬 저장소로 이동한다

* `$ git remote add <이름> <URL> ` 이름은 보통 'origin' , URL주소는 github에 생성한 repo http주소를 복사한다.

* `$ git remote -v` 를 입력하면 단축이름 origin과 원격저장소의 URL을 확인할 수 있다

* 리모트 저장소를 삭제하려면 `git remote remove`나 `git remote rm`명령을 사용한다.

  ```
  $ git remote remove origin



#### 3) Upload

* 마지막으로 로컬 저장소에 있는 파일을 원격저장소로 `push`하면 된다. 

  ```
  $git push <이름> <branch> 
  ```

* 원격 저장소로 `push`하기 위해서는 `add`와 `commit`을 해야 한다. 

  ```
  $ git status
  $ git add .
  $ git commit -m 'first'
  $ git push -u origin master



#### 4) pull & fetch

**원격 저장소에서 로컬 저장소로 소스를 가져오는 명령어로는** `pull`과 `fetch`가 있습니다. **fetch와 pull의 차이는 가져온 소소를 merge 하느냐 안하느냐의 차이**가 있습니다. `pull` 명령어는 원격 저장소의 소스를 가져오고 해당 소스가 현재 내 소스보다 더 최신 버전이라고 하면 지금의 버전을 해당 소스에 맞춰 올립니다. `merge` 명령어를 사용하는 것이지요. 하지만 fetch의 경우 단지 소스를 가져올 뿐 `merge` 하지는 않습니다.

```
$ git fetch origin
```

```
$ git pull origin master
```



#### 5) clone

clone은 `git clone <리모트 저장소 주소>`를 이용하여 사용할 수 있습니다. 이 명령어는 원격 저장소에 있는 프로젝트를 가져오는 역할을 합니다. **master 브런치를 자동으로 가져오며 origin으로 remote도 add해 줍니다.** git init 명령어로 **git 프로젝트가 아닌 곳에서도 사용할 수 있는 명령어**입니다.

```
$ git clone https://...
```

위 명령어를 실행하면 원격 저장소를 가져옵니다. 

