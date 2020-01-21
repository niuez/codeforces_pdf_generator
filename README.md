# PDF Generator for problems on Codeforces 

```
python3 main.py 1285        # generate PDF of problems on contest 1285
python3 main.py 1285 -p A B # generate PDF of problems 1285A, 1285B
```

# Docker Container

```
$ docker-compose build                   # build docker container (settting up lxml is little slow)
$ docker-compose run wkhtmltopdf /bin/sh # into container

/tmp # python3 main.py 1285 -p A         # generate PDF of problems 1285A
load codeforces problem https://codeforces.com/contest/1285/problem/A
Loading pages (1/6)
Counting pages (2/6)
Resolving links (4/6)
Loading headers and footers (5/6)
Printing pages (6/6)
Done
saved problem 1285A as pdf CF1285A.pdf
/tmp # exit                              # exit container
```

# demo

![](./demo1285.png)
