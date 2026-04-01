## GitHub SSH Key 설정
| 항목 | SSH | HTTPS |
|:----:|:------:|:--------:|
| **인증 방식** | 공개키/개인키 | 사용자명/토큰 |
| **보안성** | 높음 | 일반 |
| **매번 인증** | 불필요 | 필요 |
---

### SSH Key 생성
```zsh
$ ssh-keygen -t ed25519 -C "username@gmail.com"

Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/claude/.ssh/id_ed25519): 
Created directory '/home/claude/.ssh'.
Enter passphrase for "/home/claude/.ssh/id_ed25519" (empty for no passphrase): 
Enter same passphrase again: 
```

### SSH Key 생성
```zsh
$ cat ~/.ssh/id_ed25519.pub
```

### GitHub에 공개 키 등록
```zsh
Settings → SSH and GPG keys → New SSH key

Title: 이름 입력 (예: "My Laptop")
Key: 복사한 공개 키 붙여넣기(ssh-ed25519 ~ )
Add SSH key 클릭
```

### 연결 확인
```zsh
$ ssh -T git@github.com

Hi username! You've successfully authenticated...
```

### Git 클론
```zsh
$ git clone git@github.com:username/repository.git
```