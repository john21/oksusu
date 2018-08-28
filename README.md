# oksusu

옥수수 KODI / PLEX 플러그인
- 참고 : https://blog.naver.com/cybersol/221205923312
- KODI용 압축파일 : https://soju6jan.github.io
- 설치 후 실행이 안될 때는 데이터 폴더 삭제후 재실행 (예: 윈도우기준)
 > + KODI : C:\Users\soju6jan\AppData\Roaming\Kodi\userdata\addon_data\plugin.video.oksusu
 > + PLEX : C:\Users\soju6jan\AppData\Local\Plex Media Server\Plug-in Support\Data\com.plexapp.plugins.oksusu

----
#### 폴더구조
#####  ```oksusu.py``` 파일은 공용파일이다. 직접 파일을 복사한 후 설치 해야한다.
  - KODI
  ```
    - plugin.video.oksusu
        resoureces
          language
            Korean
            English
          lib  (lib 폴더 생성 후 oksusu.py 복사)
  ```

  - PLEX
  ```
    - Oksusu.bundle
        Contents
          Code ( code 폴더에 oksusu.py 복사)
          Resources
  ```


----
#### ChangeLog
##### 0.2.1 (20180828)
- 일부 OS에서 실행 안되는 문제 수정
  (GetList SSL bug fix)

##### 0.2.0 (20180801)
- 옥수수 사이트 변경 대응

##### 0.1.5 (20180329)
- 사이트 개편 대응

##### 0.1.4 (20180220)
- SSL 관련 코드 변경

##### 0.1.3
- KODI : 설정 enum value도 strings.xml로 변경

##### 0.1.1
- PLEX : 음악방송 ios만 videoclip
