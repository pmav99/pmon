## pmon

A process monitor for linux that shows detailed RAM usage info.

``` bash
$ pmon 261071
vms       rss       pss       uss       shared    swap      rss (%)   pss (%)   uss (%)   cpu (%)
2.576G    1.122G    1.110G    1.107G    99.699M   0B        7.22      7.14      7.12      0.00
2.576G    1.122G    1.110G    1.107G    99.699M   0B        7.22      7.14      7.12      12.23
2.576G    1.122G    1.110G    1.107G    99.699M   0B        7.22      7.14      7.12      6.48
```

### Rationale

Measuring RAM usage on Linux can be
[tricky](https://web.archive.org/web/20120520221529/http://emilics.com/blog/article/mconsumption.html).
Probably the most correct way to measure it is to use
[`USS`](https://gmpy.dev/blog/2016/real-process-memory-and-environ-in-python), i.e:

> USS (Unique Set Size) is the memory which is unique to a process and which would be freed if the
> process was terminated right now.

Unfortunately, tools like `top` and `htop` do not report this metric. Nevertheless,
[psutil](https://github.com/giampaolo/psutil) does collect it, so, we use it as the backend to monitor
RAM usage.

### Install

``` bash
pipx install pmon
```

### Usage

If you only care about `USS` then you can use:

``` bash
$ pmon --ram short 261071
uss       uss (%)   cpu (%)
1.107G    7.12      0.00
1.107G    7.12      0.00
1.107G    7.12      0.00
```

If you want the full output use:

``` bash
$ pmon --ram verbose 261071
vms       rss       pss       uss       shared    text      lib       data      dirty     swap      rss (%)   pss (%)   uss (%)   cpu (%)
2.576G    1.122G    1.110G    1.107G    99.699M   4.000K    0B        1.566G    0B        0B        7.22      7.14      7.12      0.00
2.576G    1.122G    1.110G    1.107G    99.699M   4.000K    0B        1.566G    0B        0B        7.22      7.14      7.12      0.00
```

There are other options which you can explore with:

``` bash
pmon --help
```
