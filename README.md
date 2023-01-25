A console-based python ping tool, inspired by NirSoft [PingInfoView](https://www.nirsoft.net/utils/multiple_ping_tool.html)


This is a rough, hacked together version that has pretty poor performance - but gets the job done. 


```
┏━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ Alive ┃ IP Addr        ┃ Hostname               ┃ Last 10  ┃ Loss ┃ Received ┃ Sent ┃ Last RTT ┃ Mean RTT ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ UP    │ 1.1.1.1        │ one.one.one.one        │ ✅✅✅✅ │ 0.0% │ 4        │ 4    │ 81.58    │ 62.73    │
│ UP    │ 8.8.8.8        │ dns.google             │ ✅✅✅✅ │ 0.0% │ 4        │ 4    │ 45.54    │ 52.21    │
│ UP    │ 208.67.222.222 │ resolver1.opendns.com  │ ✅✅✅✅ │ 0.0% │ 4        │ 4    │ 45.88    │ 50.81    │
│ UP    │ 4.2.2.2        │ b.resolvers.level3.net │ ✅✅✅✅ │ 0.0% │ 4        │ 4    │ 38.34    │ 51.52    │
│ UP    │ 192.0.43.10    │ 43-10.any.icann.org    │ ✅✅✅✅ │ 0.0% │ 4        │ 4    │ 61.8     │ 65.8     │
│ UP    │ 18.160.225.13  │ canireachthe.net       │ ✅✅✅✅ │ 0.0% │ 4        │ 4    │ 44.39    │ 47.31    │
│ UP    │ 127.0.0.1      │ localhost              │ ✅✅✅✅ │ 0.0% │ 4        │ 4    │ 0.17     │ 0.16     │
│ UP    │ 74.6.231.21    │ yahoo.com              │ ✅✅✅✅ │ 0.0% │ 4        │ 4    │ 60.48    │ 67.85    │
└───────┴────────────────┴────────────────────────┴──────────┴──────┴──────────┴──────┴──────────┴──────────┘
```

TODO: 
- async ping
- host - description format 
- better data structure (SQLite)?
- ~~text file input~~
- ~~IP/DNS lookup~~
- ~~set ping interval via cli~~
