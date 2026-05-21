### SSH 트러블슈팅


#### 1. 증상 확인
```bash
ssh -i key.pem ubuntu@PUBLIC_IP
```

로그에서 중요한 부분은 다음과 같다.

```text
WARNING: UNPROTECTED PRIVATE KEY FILE!
Permissions 0644 for 'awsu.pem' are too open.
This private key will be ignored.
Load key "key.pem": bad permissions
Permission denied (publickey).
```

`The authenticity of host ... can't be established` 메시지는 처음 접속하는 서버를 known hosts에 등록할지 묻는 정상 확인 절차다. 실제 오류는 개인 키 파일 권한이 너무 열려 있어서 SSH 클라이언트가 키를 사용하지 않는 것이다.

#### 2. 원인 가설

가설:`key.pem` 파일 권한이 `0644`라서 다른 사용자도 읽을 수 있는 상태다.

SSH 개인 키는 민감한 인증 정보이므로 소유자만 읽을 수 있어야 한다. 권한이 너무 넓으면 SSH가 보안상 위험하다고 판단하고 키를 무시한다.

#### 3. 검증

```bash
ls -l key.pem
```

예상 문제 상태:

```text
-rw-r--r--  key.pem
```

`rw-r--r--`는 소유자뿐 아니라 그룹/다른 사용자도 읽을 수 있다는 의미

#### 4. 조치

```bash
chmod 400 key.pem
ssh -i key.pem ubuntu@PUBLIC_IP
```

권한 변경 후 기대 상태:

```text
-r--------  key.pem
```

`chmod 400`은 키 소유자만 읽을 수 있게 제한



#### SSL 인증서 트러블슈팅


```bash
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Requesting a certificate for awsu.duckdns.org

Certbot failed to authenticate some domains (authenticator: nginx). The Certificate Authority reported these problems:
  Domain: awsu.duckdns.org
  Type:   dns
  Detail: During secondary validation: DNS problem: query timed out looking up A for awsu.duckdns.org; no valid AAAA records found for awsu.duckdns.org

Hint: The Certificate Authority failed to verify the temporary nginx configuration changes made by Certbot. Ensure the listed domains point to this nginx server and that it is accessible from the internet.

Some challenges have failed.
Ask for help or search for solutions at https://community.letsencrypt.org. See the logfile /var/log/letsencrypt/letsencrypt.log or re-run Certbot with -v for more details.
```

### 해결책
* `인스턴스 생성`
* `새 도메인`
* `HTTPS 접속 확인`