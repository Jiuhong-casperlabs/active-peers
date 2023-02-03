
## Reason for this tool
Since the node operator can decide opening or closing 7777, 9999 ports or customizing the ports to others this tool is printing out the active nodes with both 7777 and 9999 ports opened.

## STEP1
Install requirements

```
pip install -r requirements.txt
```

## STEP2

### TESTNET
Any of the following commands
```
python activepeers.py
```
```
python activepeers.py --node-host 3.136.227.9
```
```
python activepeers.py --node-host 3.23.146.54
```

### MAINNET
Any of the following commands
```
python activepeers.py --node-host 3.14.161.135
```
```
python activepeers.py --node-host 3.12.207.193
```
```
python activepeers.py --node-host 3.142.224.108
```
