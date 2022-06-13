# EISS (전자메시지 면역보안 시스템)

# 🛡️ EML 파싱 및 악성여부 판단 Core

백엔드 메일 서버에서 직접 EML 파일을 추출하여 첨부파일 파싱후 악성/스팸 여부를 판단합니다.  
파싱된 특징들은 ML모델을 거쳐 악성/정상 여부를 판단하게 됩니다. [ML 모델 분석](https://github.com/Ho1guma/EML/tree/main/model)


## :pushpin: 주요 특징

- 메일 정책에 따른 광고/프로모션 메일 판별
- 단축 url 판별
- 인공지능 기반 첨부파일 시그니처 정적 분석
- 샌드박스 기반 첨부파일 동적 분석


## 🧑‍🤝‍🧑 함께한 사람들

- [@Anti9uA](https://github.com/Anti9uA) | [@geujeog](https://github.com/geujeog) | [@Ho1guma](https://github.com/Ho1guma)


## :framed_picture: 흐름도

![image](https://user-images.githubusercontent.com/52993882/167449740-aca5955c-963b-4fa8-9519-98b4ab98a7cf.png)
