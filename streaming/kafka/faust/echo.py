#!python
# Test app to that tests PyShark by echo'ing packets to stdout

import faust, pyshark

app = faust.App('shark-test', broker='kafka://192.168.122.73:9092',
        value_serializer = "raw")
t = app.topic('sharks', value_type=str)

@app.agent(t)
async def greet(packets):
    for g in packets:
        c = pyshark.InMemCapture()
        p = c.parse_packet(g)
        print(p)
        c.close()

if __name__ == '__main__':
    app.main()
