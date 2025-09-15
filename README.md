# COOJA CLI 

## INSTALL VIA PIP
pip install git+https://github.com/ChristianPorsmose/COOJA_CLI.git


### ALL HEADLESS RUNS NEEDS A SCRITPRUNNER PLUGIN

### THE HEADLESS RUN NEEDS A TERMINATING CONDITION LIKE A MOTE LOGGING SOMETHING SPECFIC YOU LOOK FOR

#### EXAMPLE
In my motetype file i will have a log saying matrix sim is over:

```
LOG_INFO("Matrix test done\n");
```

In my scriptrunner script i will catch this with:
```
TIMEOUT(1000000); // optional total timeout

while (true) {
    if (msg != null) {
        log.log(time + ":" + id + ":" + msg + "\n"); // capture all messages
        if (msg.contains("Matrix test done1")) {
            log.testOK();  // mark test success
            break;
        }
    }
    YIELD(); // wait for next message
}
```
notice the log.testOK() this is important and must be called