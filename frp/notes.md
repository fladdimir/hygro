# frp

```sh
# download binaries:
# https://github.com/fatedier/frp/releases
# amd64:
curl -O -L https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_amd64.tar.gz
# arm64:
curl -O -L https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_arm64.tar.gz

# unpack:
tar -xvzf frp_0.61.0_linux_amd64.tar.gz
```

```sh
# start with config
# server:
./frp/release/frp_0.61.0_linux_amd64/frps -c ./frp/frps.toml
# client: 
./frp/release/frp_0.61.0_linux_amd64/frpc -c ./frp/frpc.toml
```
